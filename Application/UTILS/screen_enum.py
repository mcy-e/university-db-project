
#& Imports

from enum import IntEnum

class Screens(IntEnum):
    HOME = 0
    
    #* CRUD Menu & 13 CRUD Screens
    CRUD_MENU = 1
    STUDENT_CRUD = 2
    INSTRUCTOR_CRUD = 3
    COURSE_CRUD = 4
    DEPARTMENT_CRUD = 5
    ROOM_CRUD = 6
    RESERVATION_CRUD = 7
    ENROLLMENT_CRUD = 8
    MARK_CRUD = 9
    ACTIVITY_CRUD = 10
    EXAM_CRUD = 11
    ATTENDANCE_CRUD = 12
    
    #* Academic Menu & 2 Screens
    ACADEMIC_MENU = 13
    ASSIGN_INSTRUCTOR = 14
    MANAGE_RESERVATIONS = 15
    
    #* Performance Menu & 2 Screens
    PERFORMANCE_MENU = 16
    MARKS_ENTRY = 17
    ATTENDANCE_ENTRY = 18
    
    #* Results Viewer
    RESULTS_VIEWER = 19
    
    #* Queries Viewer
    QUERY_VIEWER = 20
    
    #* Audit Viewer
    AUDIT_VIEWER = 21

    #* Settings
    SETTINGS_SCREEN=22