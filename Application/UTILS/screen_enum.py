
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
    SECTION_CRUD = 10
    GROUP_CRUD = 11
    ACTIVITY_CRUD = 12
    EXAM_CRUD = 13
    ATTENDANCE_CRUD = 14
    
    #* Academic Menu & 2 Screens
    ACADEMIC_MENU = 15
    ASSIGN_INSTRUCTOR = 16
    MANAGE_RESERVATIONS = 17
    
    #* Performance Menu & 2 Screens
    PERFORMANCE_MENU = 18
    MARKS_ENTRY = 19
    ATTENDANCE_ENTRY = 20
    
    #* Results Menu & 1 Screen
    RESULTS_MENU = 21
    RESULTS_VIEWER = 22
    
    #* Queries Menu & 1 Screen
    QUERIES_MENU = 23
    QUERY_VIEWER = 24
    
    #* Audit Menu & 1 Screen
    AUDIT_MENU = 25
    AUDIT_VIEWER = 26