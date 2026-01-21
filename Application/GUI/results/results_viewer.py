#& Imports

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QHeaderView, QTableWidgetItem, QMessageBox
)

from Database import database as db

from GUI.styling import styling_loader as sl


import logging

logger = logging.getLogger(__name__)

#* Path to ui file for results viewer
PATH_TO_UI = "Application/GUI/UI/results_viewer.ui"

class ResultViewer(QWidget):

    go_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi(PATH_TO_UI, self)
        
        #* Setup UI components
        self._setup_table()
        self._populate_dropdowns()
        self._connect_signals()
        
        logger.info("ResultViewer initialized")
    
    #* Setup the results table with proper columns
    def _setup_table(self):
         
        headers = [self.tr("Student ID"),
                    self.tr("Full Name"),
                    self.tr("Mark"),
                    self.tr("Status")]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        #* Stretch all columns
        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        
        #* Hide row numbers
        self.table.verticalHeader().setVisible(False)
        
        logger.debug("Results table configured")

    #* Populate all dropdown menus with data
    def _populate_dropdowns(self):
        
        #* Populate semesters
        semesters = db.get_semesters_list()
        self.semester_selection.addItem(self.tr("Select Semester"))
        for semester in semesters:
            self.semester_selection.addItem(semester)
        
        #* Populate courses
        courses = db.get_all_courses()
        self.course_selection.addItem(self.tr("Select Course"))
        for course_id, dept_id, course_name, description in courses:
            display = f"{course_name} (Dept {dept_id})"
            self.course_selection.addItem(display, userData=course_id)
        
        logger.debug(f"Loaded {len(semesters)} semesters, {len(courses)} courses")

    #* Connect all signals
    def _connect_signals(self):
        
        self.back.clicked.connect(self.go_back.emit)
        self.semester_selection.currentIndexChanged.connect(self._load_results)
        self.course_selection.currentIndexChanged.connect(self._load_results)
        self.export_pdf.clicked.connect(self._export_to_pdf)
        
        logger.debug("All signals connected")

    #* Load results based on selected semester and course
    def _load_results(self):
        
        semester_index = self.semester_selection.currentIndex()
        course_index = self.course_selection.currentIndex()
        
        if semester_index == 0 or course_index == 0:
            self.table.setRowCount(0)
            return
        
        semester = self.semester_selection.currentText()
        course_id = self.course_selection.currentData()
        
        try:
            results = db.get_student_results(semester, course_id)
            self._display_results(results)
            logger.info(f"Loaded {len(results)} results")
        except Exception as e:
            logger.error(f"Error loading results: {e}")
            QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to load results:") + f" {e}")

    #* Display results in the table 
    def _display_results(self, results):
        
        self.table.setRowCount(0)
        
        for row_idx, result in enumerate(results):
            student_id, full_name, mark, status = result
            
            self.table.insertRow(row_idx)
            
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(student_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(full_name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(mark)))
            self.table.setItem(row_idx, 3, QTableWidgetItem(status))
        
        logger.debug(f"Displayed {len(results)} results in table")

    #* Export results to PDF
    def _export_to_pdf(self):
 
        QMessageBox.information(self, self.tr("Export"), self.tr("PDF export functionality coming soon!"))
        logger.info("PDF export requested")