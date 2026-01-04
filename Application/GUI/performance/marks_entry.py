#& Imports

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QHeaderView, QTableWidgetItem, QLineEdit,
    QMessageBox
)
from PyQt6.QtCore import Qt

from Database import database as db

import logging

logger = logging.getLogger(__name__)

#* Path to ui file for marks entry
PATH_TO_UI = "Application/GUI/UI/marks_entry.ui"

class MarksEntry(QWidget):
    
    go_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi(PATH_TO_UI, self)
        
        #* Store loaded students data
        self.students_data = []
        
        #* Setup UI components
        self._setup_table()
        self._populate_dropdowns()
        self._connect_signals()
        
        logger.info("MarksEntry initialized")

    #* Setup the marks entry table with proper columns
    def _setup_table(self):

        headers = ["Student ID", "Full Name", "Current Mark", "New Mark"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        #* Stretch all columns
        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        
        #* Hide row numbers
        self.table.verticalHeader().setVisible(False)
        
        #* Select rows only
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.NoSelection)
        
        logger.debug("Marks table configured")

    #* Populate all dropdown menus with data
    def _populate_dropdowns(self):

        #* Populate courses
        courses = db.get_all_courses()
        self.course_selection.addItem("Select Course")
        for course_id, dept_id, course_name, description in courses:
            display = f"{course_name} (Dept {dept_id})"
            self.course_selection.addItem(display, userData=course_id)
        
        #* Populate exams/activities (initially empty until course is selected)
        self.exam_selection.addItem("Select Exam/Activity")
        
        logger.debug(f"Loaded {len(courses)} courses")

    #* Connect all signals to their handlers 
    def _connect_signals(self):
        self.back.clicked.connect(self.go_back.emit)
        
        #* Connect course selection to load exams
        self.course_selection.currentIndexChanged.connect(self._load_exams)
        
        #* Connect exam selection to load students
        self.exam_selection.currentIndexChanged.connect(self._load_students)
        
        #* Connect save button
        self.save.clicked.connect(self._save_marks)
        
        logger.debug("All signals connected")

    #* Load exams/activities for selected course
    def _load_exams(self):

        course_index = self.course_selection.currentIndex()
        
        if course_index == 0:  #* "Select Course" option
            self.exam_selection.clear()
            self.exam_selection.addItem("Select Exam/Activity")
            self.table.setRowCount(0)
            return
        
        course_id = self.course_selection.currentData()
        
        #* Load exams for this course
        try:
            exams = db.get_exams_by_course(course_id)
            
            self.exam_selection.clear()
            self.exam_selection.addItem("Select Exam/Activity")
            
            for exam_id, exam_type, duration, dept_id in exams:
                display = f"{exam_type} ({duration} min)"
                self.exam_selection.addItem(display, userData=exam_id)
            
            logger.info(f"Loaded {len(exams)} exams for course {course_id}")
            
        except Exception as e:
            logger.error(f"Error loading exams: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load exams: {e}")

    #* Load students enrolled in selected course with their marks
    def _load_students(self):
        exam_index = self.exam_selection.currentIndex()
        
        if exam_index == 0:  #* "Select Exam/Activity" option
            self.table.setRowCount(0)
            return
        
        course_id = self.course_selection.currentData()
        exam_id = self.exam_selection.currentData()
        
        #* Load students and their marks
        try:
            self.students_data = db.get_students_with_marks(course_id, exam_id)
            self._display_students()
            logger.info(f"Loaded {len(self.students_data)} students for course {course_id}, exam {exam_id}")
        except Exception as e:
            logger.error(f"Error loading students: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load students: {e}")

    #* Display students in the table with editable mark fields
    def _display_students(self):
        #* Block signals during setup
        self.table.blockSignals(True)
        
        #* Clear existing rows
        self.table.setRowCount(0)
        
        for row_idx, student in enumerate(self.students_data):
            student_id, last_name, first_name, current_mark = student
            
            self.table.insertRow(row_idx)
            
            #* Student ID (read-only)
            id_item = QTableWidgetItem(str(student_id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row_idx, 0, id_item)
            
            #* Full Name (read-only)
            full_name = f"{first_name} {last_name}"
            name_item = QTableWidgetItem(full_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row_idx, 1, name_item)
            
            #* Current Mark (read-only)
            current_mark_display = str(current_mark) if current_mark is not None else "N/A"
            mark_item = QTableWidgetItem(current_mark_display)
            mark_item.setFlags(mark_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row_idx, 2, mark_item)
            
            #* New Mark (editable line edit)
            mark_input = QLineEdit()
            mark_input.setPlaceholderText("Enter mark (0-20)")
            if current_mark is not None:
                mark_input.setText(str(current_mark))
            
            #* Add validation - only allow numbers and decimal point
            mark_input.setMaxLength(5)
            
            self.table.setCellWidget(row_idx, 3, mark_input)
        
        #* Unblock signals
        self.table.blockSignals(False)
        
        logger.debug(f"Displayed {len(self.students_data)} students in table")

    #* Save all marks to database
    def _save_marks(self):

        #* Validate selections
        if self.course_selection.currentIndex() == 0:
            QMessageBox.warning(self, "Validation Error", "Please select a course")
            return
        
        if self.exam_selection.currentIndex() == 0:
            QMessageBox.warning(self, "Validation Error", "Please select an exam/activity")
            return
        
        course_id = self.course_selection.currentData()
        exam_id = self.exam_selection.currentData()
        
        #* Collect marks data
        marks_records = []
        invalid_marks = []
        
        for row in range(self.table.rowCount()):
            student_id = self.table.item(row, 0).text()
            
            #* Get mark input widget
            mark_widget = self.table.cellWidget(row, 3)
            if isinstance(mark_widget, QLineEdit):
                mark_text = mark_widget.text().strip()
                
                #* Skip if empty
                if not mark_text:
                    continue
                
                #* Validate mark value
                try:
                    mark_value = float(mark_text)
                    
                    if mark_value < 0 or mark_value > 20:
                        invalid_marks.append(f"Row {row + 1}: Mark must be between 0 and 20")
                        continue
                    
                    marks_records.append({
                        'student_id': student_id,
                        'course_id': course_id,
                        'exam_id': exam_id,
                        'mark_value': mark_value
                    })
                    
                except ValueError:
                    invalid_marks.append(f"Row {row + 1}: Invalid mark format")
        
        #* Show validation errors if any
        if invalid_marks:
            error_msg = "Invalid marks found:\n" + "\n".join(invalid_marks)
            QMessageBox.warning(self, "Validation Error", error_msg)
            return
        
        if not marks_records:
            QMessageBox.warning(self, "No Data", "No marks to save")
            return
        
        logger.info(f"Attempting to save {len(marks_records)} marks")
        
        #* Save to database
        try:
            success = db.save_bulk_marks(marks_records)
            
            if success:
                QMessageBox.information(
                    self, 
                    "Success", 
                    f"Marks saved successfully for {len(marks_records)} students!"
                )
                logger.info(f"Saved marks for course {course_id}, exam {exam_id}")
                
                #* Reload students to show updated marks
                self._load_students()
            else:
                QMessageBox.critical(self, "Error", "Failed to save marks - Database returned False")
                logger.error("Database returned False for save_bulk_marks")
                
        except Exception as e:
            logger.error(f"Error saving marks: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save marks: {e}")