#& Imports

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

import logging

logger = logging.getLogger(__name__)

#* Path to ui file for CRUD menu screen

from config import get_resource_path
import os
PATH_TO_UI = get_resource_path(os.path.join("GUI", "UI", "crud_menu_screen.ui"))


class CRUDMenuScreen(QWidget):
    
    #* Create Signals
    navigate_to_student_crud = pyqtSignal()
    navigate_to_instructor_crud = pyqtSignal()
    navigate_to_course_crud = pyqtSignal()
    navigate_to_department_crud = pyqtSignal()
    navigate_to_room_crud = pyqtSignal()
    navigate_to_reservation_crud = pyqtSignal()
    navigate_to_enrollment_crud = pyqtSignal()
    navigate_to_mark_crud = pyqtSignal()
    navigate_to_activity_crud = pyqtSignal()
    navigate_to_exam_crud = pyqtSignal()
    navigate_to_attendance_crud = pyqtSignal()
    go_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi(PATH_TO_UI, self)
        
        #* Connect signals
        self.back_btn.clicked.connect(self.go_back.emit)
        self.student_crud_btn.clicked.connect(self.navigate_to_student_crud.emit)
        self.instructor_crud_btn.clicked.connect(self.navigate_to_instructor_crud.emit)
        self.course_crud_btn.clicked.connect(self.navigate_to_course_crud.emit)
        self.department_crud_btn.clicked.connect(self.navigate_to_department_crud.emit)
        self.room_crud_btn.clicked.connect(self.navigate_to_room_crud.emit)
        self.reservation_crud_btn.clicked.connect(self.navigate_to_reservation_crud.emit)
        self.enrollment_crud_btn.clicked.connect(self.navigate_to_enrollment_crud.emit)
        self.mark_crud_btn.clicked.connect(self.navigate_to_mark_crud.emit)
        self.activity_crud_btn.clicked.connect(self.navigate_to_activity_crud.emit)
        self.exam_crud_btn.clicked.connect(self.navigate_to_exam_crud.emit)
        self.attendance_crud_btn.clicked.connect(self.navigate_to_attendance_crud.emit)
        
        logger.info("CRUDMenuScreen initialized")