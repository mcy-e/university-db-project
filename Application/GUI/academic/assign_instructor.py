
#& Imports

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QWidget, QHeaderView, QLabel, QLineEdit,
    QGridLayout, QTableWidgetItem, QListWidgetItem
)

from datetime import datetime

import logging

logger = logging.getLogger(__name__)

#* Path to ui file for instructor assignment
PATH_TO_UI = "Application/GUI/UI/IC_Assignments.ui"

from Database import database as db

class InstructorListItem(QListWidgetItem):
    
    #*Custom list item that stores instructor data
    def __init__(self, instructor_id, full_name, department_id):
        super().__init__(full_name)
        self.instructor_id = instructor_id
        self.department_id = department_id
        self.full_name = full_name

class CourseListItem(QListWidgetItem):
    #* Custom list item that stores course data
    def __init__(self, course_id, course_name, department_id):
        super().__init__(course_name)
        self.course_id = course_id
        self.department_id = department_id
        self.course_name = course_name

class AssignInstructor(QWidget):
    
    go_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi(PATH_TO_UI, self)

        self.instructor_data = []  #* Store tuple data
        self.course_data = []      #* Store tuple data
        self.headers = [self.tr("Instructor ID"),
                        self.tr("Instructor"),
                        self.tr("Course ID"),
                        self.tr("Course"),
                        self.tr("Department ID"),
                        self.tr("Date Assigned")]
        
        self._load_data()
        self._connect_signals()
        self._setup_table()
        self._populate_lists()
        self._populate_assignment_table()

    def _load_data(self):
        #*Load data from database
        self.instructor_data = db.get_instructor_list_with_ids()
        self.course_data = db.get_course_list_with_ids()
        self.assignment_data = db.get_all_instructor_course_assignments()

    def _connect_signals(self):
        self.back_btn.clicked.connect(self.go_back.emit)
        self.assign_btn.clicked.connect(self._assign_instructor)
        self.remove.clicked.connect(self._remove_assignment)
        self.search_instructor.textChanged.connect(self._search_instructor)
        self.search_course.textChanged.connect(self._search_course)

    def _setup_table(self):
        #* Setup assignment table
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setRowCount(0)
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)
        logger.info(f"Table initialized with {len(self.headers)} columns")

    def _populate_lists(self):
        #* Populate instructor and course lists
        self.instructor_list.clear()
        for instructor_id, full_name, dept_id in self.instructor_data:
            item = InstructorListItem(instructor_id, full_name, dept_id)
            self.instructor_list.addItem(item)
        
        self.course_list.clear()
        for course_id, course_name, dept_id in self.course_data:
            item = CourseListItem(course_id, course_name, dept_id)
            self.course_list.addItem(item)
        
        logger.info(f"Populated {self.instructor_list.count()} instructors and {self.course_list.count()} courses")

    def _populate_assignment_table(self):
        #* Populate current assignments table
        self.table.setRowCount(0)
        
        for row_idx, row_data in enumerate(self.assignment_data):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_idx, col_idx, item)
        
        logger.info(f"Assignment table populated with {self.table.rowCount()} rows")

    def _assign_instructor(self):
        #* Assign selected instructor to selected course
        instructor_item = self.instructor_list.currentItem()
        course_item = self.course_list.currentItem()

        if not (instructor_item and course_item):
            logger.debug("Missing selection for instructor or course")
            return

        #* Get data from custom items
        instructor_id = instructor_item.instructor_id
        instructor_name = instructor_item.full_name
        course_id = course_item.course_id
        course_name = course_item.course_name
        department_id = course_item.department_id  
        assignment_date = datetime.now().strftime("%Y-%m-%d")

        try:
            success = db.assign_instructor_to_course(instructor_id, course_id, department_id, assignment_date)
            
            if not success:
                logger.error("Database failed to assign instructor")
                return
            
            #* Add row to table
            new_row = [instructor_id, instructor_name, course_id, course_name, department_id, assignment_date]
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(new_row):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
            
            #* Clear selections
            self.instructor_list.clearSelection()
            self.instructor_list.setCurrentItem(None)
            self.course_list.clearSelection()
            self.course_list.setCurrentItem(None)
            
            logger.info(f"Assigned {instructor_name} to {course_name}")
            
        except Exception as e:
            logger.error(f"Error assigning instructor: {e}")

    def _remove_assignment(self):
        #* Remove selected assignment
        row = self.table.currentRow()
        
        if row < 0:
            logger.debug("No row selected for removal")
            return
        
        #* Get IDs before removing
        instructor_id = self.table.item(row, 0).text()
        course_id = self.table.item(row, 2).text()
        department_id = self.table.item(row, 4).text()
        
        try:
            success = db.remove_instructor_from_course(instructor_id, course_id, department_id)
            
            if not success:
                logger.error("Database failed to remove assignment")
                return
            
            #* Remove from UI
            self.table.removeRow(row)
            self.table.clearSelection()
            
            logger.info(f"Removed assignment for instructor {instructor_id} from course {course_id}")
            
        except Exception as e:
            logger.error(f"Error removing assignment: {e}")

    def _search_instructor(self):
        #* Filter instructor list based on search text
        search_text = self.search_instructor.text().strip().lower()
        
        if not search_text:
            #* Show all
            for i in range(self.instructor_list.count()):
                self.instructor_list.item(i).setHidden(False)
            logger.debug("Instructor search cleared")
            return
        
        #* Filter non-matching
        visible_count = 0
        for i in range(self.instructor_list.count()):
            item = self.instructor_list.item(i)
            matches = search_text in item.text().lower()
            item.setHidden(not matches)
            if matches:
                visible_count += 1
        
        logger.info(f"Instructor search: {visible_count} matches for '{search_text}'")

    def _search_course(self):
        
        #* Filter course list based on search text
        search_text = self.search_course.text().strip().lower()
        
        if not search_text:
            #* Show all
            for i in range(self.course_list.count()):
                self.course_list.item(i).setHidden(False)
            logger.debug("Course search cleared")
            return
        
        #* Filter non-matching
        visible_count = 0
        for i in range(self.course_list.count()):
            item = self.course_list.item(i)
            matches = search_text in item.text().lower()
            item.setHidden(not matches)
            if matches:
                visible_count += 1
        
        logger.info(f"Course search: {visible_count} matches for '{search_text}'")