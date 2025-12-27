"""
    Application.GUI.main_window
    Contains main window layout with:
    Navigation grid (6 buttons)
    Top bar (menu + title)
    Settings button

"""

#& imports
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from GUI.screens.home_screen import HomeScreen
from GUI.screens.crud_menu_screen import CRUDMenuScreen
from GUI.crud.student_crud import StudentCRUD
from UTILS.screen_enum import Screens

import logging

logger = logging.getLogger(__name__)

#* Main Window class
class MainWindow (QMainWindow):
    def __init__(self):
        super().__init__()
        #* Window Title
        self.setWindowTitle("UniversityManagement")
        
        #* Window Min Size
        self.setMinimumSize(600, 600)
        self.stacked_widget = QStackedWidget()
        
        #* Create home screen
        self.home_screen = HomeScreen()
        
        #* Create CRUD Menu Screen
        self.crud_menu=CRUDMenuScreen()

        #* Create Student Crud screen
        self.student_crud=StudentCRUD()

        #* Add to stack
        self.stacked_widget.addWidget(self.home_screen) 
        self.stacked_widget.addWidget(self.crud_menu) 
        self.stacked_widget.addWidget(self.student_crud) 
         
        
        #* Connect signals
        self._connect_home_signals()

        self._connect_back_buttons()

        #* Set as central widget
        self.setCentralWidget(self.stacked_widget)
    
    def _connect_back_buttons(self):

        #? Connect all back navigation buttons
        
        back_map = {
            self.crud_menu.go_back: (Screens.HOME,"Home Screen Back"),
            self.student_crud.go_back: (Screens.CRUD_MENU,"CRUD Menu Back"),
        }

        for signal, (screen, log_msg) in back_map.items():
            signal.connect(lambda s=screen, m=log_msg: self._navigate(s, m))
        

   
    def _connect_home_signals(self):

        #? Connect all home screen navigation buttons

        navigation_map = {
            self.home_screen.navigate_to_crud: (Screens.CRUD_MENU, "CRUD menu"),
            self.home_screen.navigate_to_academic: (None, "Academic menu"),
            self.home_screen.navigate_to_performance: (None, "Performance menu"),
            self.home_screen.navigate_to_results: (None, "Results menu"),
            self.home_screen.navigate_to_queries: (None, "Queries menu"),
            self.home_screen.navigate_to_audit: (None, "Audit menu"),
            self.home_screen.navigate_to_settings: (None, "Settings"),
            self.home_screen.open_side_bar: (None, "Side Bar"),
            self.crud_menu.navigate_to_student_crud:(Screens.STUDENT_CRUD,"Student CRUD Screen"),
            self.crud_menu.navigate_to_instructor_crud: (None, "Instructor CRUD Screen"),
            self.crud_menu.navigate_to_course_crud: (None, "Course CRUD Screen"),
            self.crud_menu.navigate_to_department_crud: (None, "Department CRUD Screen"),
            self.crud_menu.navigate_to_room_crud: (None, "Room CRUD Screen"),
            self.crud_menu.navigate_to_reservation_crud: (None, "Reservation CRUD Screen"),
            self.crud_menu.navigate_to_enrollment_crud: (None, "Enrollment CRUD Screen"),
            self.crud_menu.navigate_to_mark_crud: (None, "Mark CRUD Screen"),
            self.crud_menu.navigate_to_section_crud: (None, "Section CRUD Screen"),
            self.crud_menu.navigate_to_group_crud: (None, "Group CRUD Screen"),
            self.crud_menu.navigate_to_activity_crud: (None, "Activity CRUD Screen"),
            self.crud_menu.navigate_to_exam_crud: (None, "Exam CRUD Screen"),
            self.crud_menu.navigate_to_attendance_crud: (None, "Attendance CRUD Screen"),

        }
        
        for signal, (screen, log_msg) in navigation_map.items():
            signal.connect(lambda s=screen, m=log_msg: self._navigate(s, m))

    def _navigate(self, screen_index, log_message):
        
        #? Navigate and Generate Log Message

        logger.debug(f"Opening {log_message}...")
        if screen_index is not None:
            self.stacked_widget.setCurrentIndex(screen_index)