"""
Application.Database.database
Contains all database CRUD operations and queries
Function definitions for GUI integration
"""

import logging

logger = logging.getLogger(__name__)


#? STUDENT OPERATIONS


def get_all_students():
    """
    Retrieve all students from the database
    
    Returns:
        list[tuple]: List of student records
        Format: (student_id, last_name, first_name, dob, address, city, 
                 zip_code, phone, fax, email, group_id, section_id)
    """
    pass


def add_student(last_name, first_name, dob, address, city, zip_code, phone, fax, email, group_id, section_id):
    """
    Insert a new student into the database
    
    Args:
        last_name (str): Student's last name
        first_name (str): Student's first name
        dob (str): Date of birth (format: YYYY-MM-DD)
        address (str): Street address
        city (str): City name
        zip_code (str): Postal code
        phone (str): Phone number
        fax (str): Fax number (optional)
        email (str): Email address (optional)
        group_id (int): Group ID
        section_id (str): Section ID (single character)
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def update_student(student_id, last_name, first_name, dob, address, city, zip_code, phone, fax, email, group_id, section_id):
    """
    Update an existing student's information
    
    Args:
        student_id (int): Student ID to update
        (same parameters as add_student)
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def delete_student(student_id):
    """
    Delete a student from the database
    
    Args:
        student_id (int): Student ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass



#? INSTRUCTOR OPERATIONS


def get_all_instructors():
    """
    Retrieve all instructors from the database
    
    Returns:
        list[tuple]: List of instructor records
        Format: (instructor_id, department_id, last_name, first_name, 
                 rank, phone, fax, email)
    """
    pass


def add_instructor(department_id, last_name, first_name, rank, phone, fax, email):
    """
    Insert a new instructor into the database
    
    Args:
        department_id (int): Department ID
        last_name (str): Instructor's last name
        first_name (str): Instructor's first name
        rank (str): Academic rank (Substitute, MCB, MCA, PROF)
        phone (str): Phone number (optional)
        fax (str): Fax number (optional)
        email (str): Email address (optional)
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def update_instructor(instructor_id, department_id, last_name, first_name, rank, phone, fax, email):
    """
    Update an existing instructor's information
    
    Args:
        instructor_id (int): Instructor ID to update
        (same parameters as add_instructor)
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def delete_instructor(instructor_id):
    """
    Delete an instructor from the database
    
    Args:
        instructor_id (int): Instructor ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass



#? COURSE OPERATIONS


def get_all_courses():
    """
    Retrieve all courses from the database
    
    Returns:
        list[tuple]: List of course records
        Format: (course_id, department_id, name, description)
    """
    pass


def add_course(course_id, department_id, name, description):
    """
    Insert a new course into the database
    
    Args:
        course_id (int): Course ID
        department_id (int): Department ID
        name (str): Course name
        description (str): Course description (optional)
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def update_course(course_id, department_id, name, description):
    """
    Update an existing course's information
    
    Args:
        course_id (int): Course ID to update
        department_id (int): Department ID
        name (str): Course name
        description (str): Course description
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def delete_course(course_id, department_id):
    """
    Delete a course from the database
    
    Args:
        course_id (int): Course ID to delete
        department_id (int): Department ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass



#? DEPARTMENT OPERATIONS


def get_all_departments():
    """
    Retrieve all departments from the database
    
    Returns:
        list[tuple]: List of department records
        Format: (department_id, name)
    """
    pass


def add_department(department_id, name):
    """
    Insert a new department into the database
    
    Args:
        department_id (int): Department ID
        name (str): Department name
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def update_department(department_id, name):
    """
    Update an existing department's information
    
    Args:
        department_id (int): Department ID to update
        name (str): New department name
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def delete_department(department_id):
    """
    Delete a department from the database
    
    Args:
        department_id (int): Department ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass



#? ROOM OPERATIONS


def get_all_rooms():
    """
    Retrieve all rooms from the database
    
    Returns:
        list[tuple]: List of room records
        Format: (building, roomno, capacity)
    """
    pass


def add_room(building, roomno, capacity):
    """
    Insert a new room into the database
    
    Args:
        building (str): Building code (single character)
        roomno (str): Room number
        capacity (int): Room capacity
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def update_room(building, roomno, capacity):
    """
    Update an existing room's information
    
    Args:
        building (str): Building code
        roomno (str): Room number
        capacity (int): New capacity
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def delete_room(building, roomno):
    """
    Delete a room from the database
    
    Args:
        building (str): Building code
        roomno (str): Room number
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass



#? RESERVATION OPERATIONS


def get_all_reservations():
    """
    Retrieve all reservations from the database
    
    Returns:
        list[tuple]: List of reservation records
        Format: (reservation_id, building, roomno, course_id, department_id,
                 instructor_id, reserv_date, start_time, end_time, hours_number)
    """
    pass


def add_reservation(building, roomno, course_id, department_id, instructor_id, 
                   reserv_date, start_time, end_time, hours_number):
    """
    Insert a new reservation into the database
    
    Args:
        building (str): Building code
        roomno (str): Room number
        course_id (int): Course ID
        department_id (int): Department ID
        instructor_id (int): Instructor ID
        reserv_date (str): Reservation date (YYYY-MM-DD)
        start_time (str): Start time (HH:MM:SS)
        end_time (str): End time (HH:MM:SS)
        hours_number (int): Duration in hours
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def update_reservation(reservation_id, building, roomno, course_id, department_id, 
                      instructor_id, reserv_date, start_time, end_time, hours_number):
    """
    Update an existing reservation's information
    
    Args:
        reservation_id (int): Reservation ID to update
        (same parameters as add_reservation)
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def delete_reservation(reservation_id):
    """
    Delete a reservation from the database
    
    Args:
        reservation_id (int): Reservation ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def check_room_availability(building, roomno, reserv_date, start_time, end_time):
    """
    Check if a room is available for reservation
    
    Args:
        building (str): Building code
        roomno (str): Room number
        reserv_date (str): Desired date (YYYY-MM-DD)
        start_time (str): Desired start time (HH:MM:SS)
        end_time (str): Desired end time (HH:MM:SS)
    
    Returns:
        bool: True if room is available, False if conflicted
    """
    pass



#? ENROLLMENT OPERATIONS


def get_all_enrollments():
    """
    Retrieve all enrollments from the database
    
    Returns:
        list[tuple]: List of enrollment records
        Format: (student_id, course_id, department_id, enrollment_date)
    """
    pass


def add_enrollment(student_id, course_id, department_id, enrollment_date):
    """
    Insert a new enrollment into the database
    
    Args:
        student_id (int): Student ID
        course_id (int): Course ID
        department_id (int): Department ID
        enrollment_date (str): Enrollment date (YYYY-MM-DD)
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def update_enrollment(student_id, course_id, department_id, enrollment_date):
    """
    Update an existing enrollment's information
    
    Args:
        student_id (int): Student ID
        course_id (int): Course ID
        department_id (int): Department ID
        enrollment_date (str): New enrollment date
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def delete_enrollment(student_id, course_id, department_id):
    """
    Delete an enrollment from the database
    
    Args:
        student_id (int): Student ID
        course_id (int): Course ID
        department_id (int): Department ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass



#? MARK OPERATIONS


def get_all_marks():
    """
    Retrieve all marks from the database
    
    Returns:
        list[tuple]: List of mark records
        Format: (mark_id, student_id, course_id, department_id, mark_value, mark_date)
    """
    pass


def add_mark(student_id, course_id, department_id, mark_value, mark_date):
    """
    Insert a new mark into the database
    
    Args:
        student_id (int): Student ID
        course_id (int): Course ID
        department_id (int): Department ID
        mark_value (float): Mark value (0-20)
        mark_date (str): Date mark was given (YYYY-MM-DD)
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def update_mark(mark_id, student_id, course_id, department_id, mark_value, mark_date):
    """
    Update an existing mark's information
    
    Args:
        mark_id (int): Mark ID to update
        (same parameters as add_mark)
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def delete_mark(mark_id):
    """
    Delete a mark from the database
    
    Args:
        mark_id (int): Mark ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass



#? ACTIVITY OPERATIONS


def get_all_activities():
    """
    Retrieve all activities from the database
    
    Returns:
        list[tuple]: List of activity records
        Format: (activity_id, activity_type, reservation_id, course_id, department_id)
    """
    pass


def add_activity(activity_id, activity_type, reservation_id, course_id, department_id):
    """
    Insert a new activity into the database
    
    Args:
        activity_id (int): Activity ID
        activity_type (str): Type (lecture, tutorial, practical)
        reservation_id (int): Associated reservation ID
        course_id (int): Course ID
        department_id (int): Department ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def update_activity(activity_id, activity_type, reservation_id, course_id, department_id):
    """
    Update an existing activity's information
    
    Args:
        activity_id (int): Activity ID to update
        (same parameters as add_activity)
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def delete_activity(activity_id):
    """
    Delete an activity from the database
    
    Args:
        activity_id (int): Activity ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass



#? EXAM OPERATIONS


def get_all_exams():
    """
    Retrieve all exams from the database
    
    Returns:
        list[tuple]: List of exam records
        Format: (exam_id, duration, exam_type, course_id, department_id)
    """
    pass


def add_exam(exam_id, duration, exam_type, course_id, department_id):
    """
    Insert a new exam into the database
    
    Args:
        exam_id (int): Exam ID
        duration (int): Duration in minutes
        exam_type (str): Type of exam (midterm, final, project, etc.)
        course_id (int): Course ID
        department_id (int): Department ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def update_exam(exam_id, duration, exam_type, course_id, department_id):
    """
    Update an existing exam's information
    
    Args:
        exam_id (int): Exam ID to update
        (same parameters as add_exam)
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def delete_exam(exam_id):
    """
    Delete an exam from the database
    
    Args:
        exam_id (int): Exam ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass



#? ATTENDANCE OPERATIONS


def get_all_attendance():
    """
    Retrieve all attendance records from the database
    
    Returns:
        list[tuple]: List of attendance records
        Format: (student_id, activity_id, attendance_date, status)
    """
    pass


def add_attendance(student_id, activity_id, attendance_date, status):
    """
    Insert a new attendance record into the database
    
    Args:
        student_id (int): Student ID
        activity_id (int): Activity ID
        attendance_date (str): Date (YYYY-MM-DD)
        status (str): Status (present, absent)
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def update_attendance(student_id, activity_id, attendance_date, status):
    """
    Update an existing attendance record
    
    Args:
        student_id (int): Student ID
        activity_id (int): Activity ID
        attendance_date (str): Date
        status (str): New status (present, absent)
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def delete_attendance(student_id, activity_id, attendance_date):
    """
    Delete an attendance record from the database
    
    Args:
        student_id (int): Student ID
        activity_id (int): Activity ID
        attendance_date (str): Date
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass



#? INSTRUCTOR-COURSE ASSIGNMENT OPERATIONS

#! NOTE: This requires creating a new table in the database


def get_all_instructor_course_assignments():
    """
    Retrieve all instructor-course assignments from the database
    
    Returns:
        list[tuple]: List of assignment records
        Format: (instructor_id, course_id, department_id, assignment_date)
    """
    pass


def assign_instructor_to_course(instructor_id, course_id, department_id, assignment_date):
    """
    Assign an instructor to a course
    
    Args:
        instructor_id (int): Instructor ID
        course_id (int): Course ID
        department_id (int): Department ID
        assignment_date (str): Date of assignment (YYYY-MM-DD)
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def remove_instructor_from_course(instructor_id, course_id, department_id):
    """
    Remove an instructor's assignment from a course
    
    Args:
        instructor_id (int): Instructor ID
        course_id (int): Course ID
        department_id (int): Department ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass


def get_instructor_full_name_list():
    """
    Retrieve list of instructor full names for display
    
    Returns:
        list[str]: List of formatted instructor names
        Format: ["Dr. FirstName LastName", ...]
    """
    pass


def get_course_name_list():
    """
    Retrieve list of course names for display
    
    Returns:
        list[str]: List of course names
    """
    pass