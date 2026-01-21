#& Imports

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, QDate
from PyQt6.QtWidgets import (
    QWidget, QHeaderView, QTableWidgetItem, QCheckBox, 
    QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt

from Database import database as db

import logging

logger = logging.getLogger(__name__)

#* Path to ui file for attendance entry
PATH_TO_UI = "Application/GUI/UI/attendance_entry.ui"

class AttendanceEntry(QWidget):
    
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
        
        #* Set default date to today
        self.date_selection.setDate(QDate.currentDate())
        
        logger.info("AttendanceEntry initialized")

    #* Setup the attendance table with proper columns    
    def _setup_table(self):
        
        headers = [self.tr("Student ID"),
                   self.tr("Full Name"),
                   self.tr("Group"),
                   self.tr("Section"),
                   self.tr("Present")]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        #* Stretch columns except the last one (checkbox)
        header = self.table.horizontalHeader()
        for i in range(len(headers) - 1):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(len(headers) - 1, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(len(headers) - 1, 100)
        
        #* Hide row numbers
        self.table.verticalHeader().setVisible(False)
        
        #* Select rows only
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.NoSelection)
        
        logger.debug("Attendance table configured")

    #* Populate all dropdown menus with data
    def _populate_dropdowns(self):

        #* Populate sections
        sections = db.get_all_sections()
        self.section_selection.addItem(self.tr("All Sections"))
        for section_id, section_name in sections:
            self.section_selection.addItem(section_name, userData=section_id)
        
        #* Populate groups
        groups = db.get_all_groups()
        self.group_selection.addItem(self.tr("All Groups"))
        for group_id, group_name in groups:
            self.group_selection.addItem(group_name, userData=group_id)
        
        #* Populate activities
        activities = db.get_all_activities()
        self.activity_selection.addItem(self.tr("Select Activity"))
        for activity_id, activity_type, course_name in activities:
            display = f"{activity_type} - {course_name}"
            self.activity_selection.addItem(display, userData=activity_id)
        
        logger.debug(f"Loaded {len(sections)} sections, {len(groups)} groups, {len(activities)} activities")

    #* Connect all signals to their handlers
    def _connect_signals(self):

        self.back.clicked.connect(self.go_back.emit)
        
        #* Connect filter changes to reload students
        self.section_selection.currentIndexChanged.connect(self._load_students)
        self.group_selection.currentIndexChanged.connect(self._load_students)
        
        #* Connect action buttons
        self.mark_all.clicked.connect(self._mark_all_present)
        self.save.clicked.connect(self._save_attendance)
        
        logger.debug("All signals connected")

    #* Load students based on selected section and group
    def _load_students(self):
 
        #* Get selected filters
        section_index = self.section_selection.currentIndex()
        group_index = self.group_selection.currentIndex()
        
        section_id = None
        group_id = None
        
        if section_index > 0:  #* Skip "All Sections"
            section_id = self.section_selection.currentData()
        
        if group_index > 0:  #* Skip "All Groups"
            group_id = self.group_selection.currentData()
        
        #* Load students from database
        try:
            self.students_data = db.get_students_by_filters(section_id, group_id)
            self._display_students()
            logger.info(f"Loaded {len(self.students_data)} students (Section: {section_id}, Group: {group_id})")
        except Exception as e:
            logger.error(f"Error loading students: {e}")
            QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to load students:") + f" {e}")

    #* Display students in the table with attendance checkboxes
    def _display_students(self):
        #* Block signals during setup
        self.table.blockSignals(True)
        
        #* Clear existing rows
        self.table.setRowCount(0)
        
        for row_idx, student in enumerate(self.students_data):
            student_id, last_name, first_name, group_id, section_id = student
            
            self.table.insertRow(row_idx)
            
            #* Student ID
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(student_id)))
            
            #* Full Name
            full_name = f"{first_name} {last_name}"
            self.table.setItem(row_idx, 1, QTableWidgetItem(full_name))
            
            #* Group
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(group_id)))
            
            #* Section
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(section_id)))
            
            #* Present checkbox (centered)
            checkbox = QCheckBox()
            checkbox.setChecked(False)  #* Default to absent
            
            #* Create a widget to center the checkbox
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            
            self.table.setCellWidget(row_idx, 4, checkbox_widget)
        
        #* Unblock signals
        self.table.blockSignals(False)
        
        logger.debug(f"Displayed {len(self.students_data)} students in table")

    #* Mark all students as present
    def _mark_all_present(self):
 
        for row in range(self.table.rowCount()):
            checkbox_widget = self.table.cellWidget(row, 4)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(True)
        
        logger.info("Marked all students as present")

    #* Save attendance records to database   
    def _save_attendance(self):
        #* Validate activity selection
        if self.activity_selection.currentIndex() == 0:
            QMessageBox.warning(self, self.tr("Validation Error"), self.tr("Please select an activity"))
            return
        
        activity_id = self.activity_selection.currentData()
        attendance_date = self.date_selection.date().toString("yyyy-MM-dd")
        
        #* Collect attendance data
        attendance_records = []
        
        for row in range(self.table.rowCount()):
            student_id = self.table.item(row, 0).text()
            
            #* Get checkbox state
            checkbox_widget = self.table.cellWidget(row, 4)
            checkbox = checkbox_widget.findChild(QCheckBox)
            status = "present" if checkbox.isChecked() else "absent"
            
            attendance_records.append({
                'student_id': student_id,
                'activity_id': activity_id,
                'date': attendance_date,
                'status': status
            })
        
        logger.info(f"Attempting to save {len(attendance_records)} attendance records")
        
        #* Save to database
        try:
            success = db.save_bulk_attendance(attendance_records)
            
            if success:
                QMessageBox.information(
                    self, 
                    self.tr("Success"), 
                    self.tr("Attendance saved successfully for") + f"{len(attendance_records)}" +self.tr("students!")
                )
                logger.info(f"Saved attendance for activity {activity_id} on {attendance_date}")
                
                #* Clear the form
                self._clear_form()
            else:
                QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to save attendance,database returned False"))
                logger.error("Database returned False for save_bulk_attendance")
                
        except Exception as e:
            logger.error(f"Error saving attendance: {e}")
            QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to save attendance:") +f" {e}")

    #* Clear the form after successful save
    def _clear_form(self):

        #* Reset filters
        self.section_selection.setCurrentIndex(0)
        self.group_selection.setCurrentIndex(0)
        self.activity_selection.setCurrentIndex(0)
        
        #* Clear table
        self.table.setRowCount(0)
        self.students_data = []
        
        #* Reset date to today
        self.date_selection.setDate(QDate.currentDate())
        
        logger.debug("Form cleared")