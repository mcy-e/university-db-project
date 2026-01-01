"""
    Application.GUI.main_window
    Contains main window layout with:
    Navigation grid (6 buttons)
    Top bar (menu + title)
    Settings button

"""

#& Imports

#? PyQt6 imports
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QStackedWidget

#? Widgets imports
from GUI.screens import *
from GUI.academic import *
from GUI.audit import AuditViewer
from GUI.crud import *
from GUI.performance import *
from GUI.queries import QueryViewer
from GUI.results import ResultViewer

#? Screens Imports
from UTILS.screen_enum import Screens

#? logger
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

        #* Create Crud screens

        self.activity_crud=ActivityCRUD()
        self.attendance_crud=AttendanceCRUD()

        self.course_crud=CourseCRUD()

        self.department_crud=DepartmentCRUD()

        self.enrollment_crud=EnrollmentCRUD()
        self.exam_crud=ExamCRUD()

        self.instructor_crud=InstructorCRUD()

        self.mark_crud=MarkCRUD()

        self.room_crud=RoomCRUD()
        self.reservation_crud=ReservationCRUD()

        self.student_crud=StudentCRUD()

        #* Create Academic Menu screen
        self.academic_menu=AcademicMenu()

        #* Create Assign Instructor screen
        self.assign_instructor=AssignInstructor()

        #* Create room reservation screen
        self.manage_reservation=ManageReservation()

        #* Create Performance Menu screen
        self.performance_menu=PerformanceMenu()

        #* Create Mark Entry screen
        self.marks_entry=MarksEntry()
        
        #* Create Attendance Entry screen
        self.attendance_entry=AttendanceEntry()

        #* Create Result Viewer screen
        self.result_viewer=ResultViewer()

        #* Create Query Viewer screen
        self.query_viewer=QueryViewer()

        #* Create Audit Viewer screen
        self.audit_viewer=AuditViewer()

        #* Add to stack
        self.stacked_widget.addWidget(self.home_screen) 
        self.stacked_widget.addWidget(self.crud_menu) 
        self.stacked_widget.addWidget(self.student_crud) 
        self.stacked_widget.addWidget(self.instructor_crud)
        self.stacked_widget.addWidget(self.course_crud)
        self.stacked_widget.addWidget(self.department_crud)
        self.stacked_widget.addWidget(self.room_crud)
        self.stacked_widget.addWidget(self.reservation_crud)
        self.stacked_widget.addWidget(self.enrollment_crud)
        self.stacked_widget.addWidget(self.mark_crud)
        self.stacked_widget.addWidget(self.activity_crud)
        self.stacked_widget.addWidget(self.exam_crud)
        self.stacked_widget.addWidget(self.attendance_crud)
        self.stacked_widget.addWidget(self.academic_menu)
        self.stacked_widget.addWidget(self.assign_instructor)
        self.stacked_widget.addWidget(self.manage_reservation)
        self.stacked_widget.addWidget(self.performance_menu)
        self.stacked_widget.addWidget(self.marks_entry)
        self.stacked_widget.addWidget(self.attendance_entry)
        self.stacked_widget.addWidget(self.result_viewer)
        self.stacked_widget.addWidget(self.query_viewer)
        self.stacked_widget.addWidget(self.audit_viewer)
    
        

        #* Connect signals
        self._connect_home_signals()

        self._connect_back_buttons()

        #* Set as central widget
        self.setCentralWidget(self.stacked_widget)
    
    def _connect_back_buttons(self):

        #? Connect all back navigation buttons
        
        back_map = {
            self.crud_menu.go_back: (Screens.HOME,"Home Screen Back"),
            self.academic_menu.go_back: (Screens.HOME,"Home Screen Back"),
            self.performance_menu.go_back: (Screens.HOME,"Home Screen Back"),
            self.result_viewer.go_back: (Screens.HOME,"Home Screen Back"),
            self.query_viewer.go_back: (Screens.HOME,"Home Screen Back"),
            self.audit_viewer.go_back: (Screens.HOME,"Home Screen Back"),
            
            self.student_crud.go_back: (Screens.CRUD_MENU,"CRUD Menu Back"),
            self.instructor_crud.go_back: (Screens.CRUD_MENU,"CRUD Menu Back"),
            self.course_crud.go_back: (Screens.CRUD_MENU,"CRUD Menu Back"),    
            self.department_crud.go_back: (Screens.CRUD_MENU,"CRUD Menu Back"),
            self.room_crud.go_back: (Screens.CRUD_MENU,"CRUD Menu Back"), 
            self.reservation_crud.go_back: (Screens.CRUD_MENU,"CRUD Menu Back"),
            self.enrollment_crud.go_back: (Screens.CRUD_MENU,"CRUD Menu Back"),
            self.mark_crud.go_back: (Screens.CRUD_MENU,"CRUD Menu Back"),
            self.activity_crud.go_back: (Screens.CRUD_MENU,"CRUD Menu Back"),
            self.exam_crud.go_back: (Screens.CRUD_MENU,"CRUD Menu Back"),
            self.attendance_crud.go_back: (Screens.CRUD_MENU,"CRUD Menu Back"),
            self.assign_instructor.go_back : (Screens.ACADEMIC_MENU, "ACADEMIC Menu Back"),
            self.manage_reservation.go_back : (Screens.ACADEMIC_MENU, "ACADEMIC Menu Back"),
            self.attendance_entry.go_back : (Screens.PERFORMANCE_MENU, "PERFORMANCE Menu Back"),
            self.marks_entry.go_back : (Screens.PERFORMANCE_MENU, "PERFORMANCE Menu Back")
        }

        for signal, (screen, log_msg) in back_map.items():
            signal.connect(lambda s=screen, m=log_msg: self._navigate(s, m))
        

   
    def _connect_home_signals(self):

        #? Connect all home screen navigation buttons

        navigation_map = {

            #* Home menu navigation dict
            self.home_screen.navigate_to_crud: (Screens.CRUD_MENU, "CRUD menu"),
            self.home_screen.navigate_to_academic: (Screens.ACADEMIC_MENU, "Academic menu"),
            self.home_screen.navigate_to_performance: (Screens.PERFORMANCE_MENU, "Performance menu"),
            self.home_screen.navigate_to_results: (Screens.RESULTS_VIEWER, "Results Viewer"),
            self.home_screen.navigate_to_queries: (Screens.QUERY_VIEWER, "Queries Viewer"),
            self.home_screen.navigate_to_audit: (Screens.AUDIT_VIEWER, "Audit Viewer"),
            self.home_screen.navigate_to_settings: (None, "Settings"),
            self.home_screen.open_side_bar: (None, "Side Bar"),

            #* Crud menu navigation dict
            self.crud_menu.navigate_to_student_crud:(Screens.STUDENT_CRUD,"Student CRUD Screen"),
            self.crud_menu.navigate_to_instructor_crud: (Screens.INSTRUCTOR_CRUD, "Instructor CRUD Screen"),
            self.crud_menu.navigate_to_course_crud: (Screens.COURSE_CRUD, "Course CRUD Screen"),
            self.crud_menu.navigate_to_department_crud: (Screens.DEPARTMENT_CRUD, "Department CRUD Screen"),
            self.crud_menu.navigate_to_room_crud: (Screens.ROOM_CRUD, "Room CRUD Screen"),
            self.crud_menu.navigate_to_reservation_crud: (Screens.RESERVATION_CRUD, "Reservation CRUD Screen"),
            self.crud_menu.navigate_to_enrollment_crud: (Screens.ENROLLMENT_CRUD, "Enrollment CRUD Screen"),
            self.crud_menu.navigate_to_mark_crud: (Screens.MARK_CRUD, "Mark CRUD Screen"),
            self.crud_menu.navigate_to_activity_crud: (Screens.ACTIVITY_CRUD, "Activity CRUD Screen"),
            self.crud_menu.navigate_to_exam_crud: (Screens.ACADEMIC_MENU, "Exam CRUD Screen"),
            self.crud_menu.navigate_to_attendance_crud: (Screens.ATTENDANCE_CRUD, "Attendance CRUD Screen"),
            
            #* Academic menu navigation dict
            self.academic_menu.navigate_to_assign_instructor: (Screens.ASSIGN_INSTRUCTOR,"Assign Instructor Screen"),
            self.academic_menu.navigate_to_manage_reservation: (Screens.MANAGE_RESERVATIONS,"Manage Reservations Screen"),
            
            #* Performance menu navigation dict
            self.performance_menu.navigate_to_attendance : (Screens.ATTENDANCE_ENTRY,"Attendance Entry Screen"),
            self.performance_menu.navigate_to_marks : (Screens.MARKS_ENTRY,"Marks Entry Screen"),
        }
        
        for signal, (screen, log_msg) in navigation_map.items():
            signal.connect(lambda s=screen, m=log_msg: self._navigate(s, m))

    def _navigate(self, screen_index, log_message):
        
        #? Navigate and Generate Log Message

        logger.debug(f"Opening {log_message}...")
        if screen_index is not None:
            self.stacked_widget.setCurrentIndex(screen_index)