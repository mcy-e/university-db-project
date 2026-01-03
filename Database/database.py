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
    return [
        ("1", "Reffas", "Chouaib", "2007-02-23", "1t, 02", "Annaba", "202235", "064862265", "Null", "mcy@gmail.com", 1, "A"),
        ("2", "Amine", "Benkacem", "2006-05-15", "12 Av. Liberté", "Algiers", "16000", "0555123456", "021123456", "amine.b@gmail.com", 1, "A"),
        ("3", "Sara", "Belkacem", "2007-11-02", "23 Rue El-Fadjr", "Oran", "31000", "0661234567", "031987654", "sara.belkacem@gmail.com", 2, "A"),
        ("4", "Youssef", "Haddad", "2005-07-18", "45 Bd. Pasteur", "Constantine", "25000", "0559876543", "031123987", "youssef.h@gmail.com", 2, "B"),
        ("5", "Leila", "Mansouri", "2006-01-09", "7 Impasse des Roses", "Annaba", "202200", "0669876543", "038123456", "leila.m@gmail.com", 3, "B"),
    ]


def get_students_by_filters(section_id=None, group_id=None):
    """
    Retrieve students filtered by section and/or group
    
    Args:
        section_id (str, optional): Section ID to filter by
        group_id (int, optional): Group ID to filter by
    
    Returns:
        list[tuple]: List of student records
        Format: (student_id, last_name, first_name, group_id, section_id)
    """
    all_students = get_all_students()
    filtered = []
    
    for student in all_students:
        student_id, last_name, first_name, dob, address, city, zip_code, phone, fax, email, group, section = student
        
        if section_id and section != section_id:
            continue
        if group_id and group != group_id:
            continue
        
        filtered.append((student_id, last_name, first_name, group, section))
    
    return filtered


def get_students_with_marks(course_id, exam_id):
    """
    Retrieve students enrolled in a course with their marks for a specific exam
    
    Args:
        course_id (int): Course ID
        exam_id (int): Exam ID
    
    Returns:
        list[tuple]: List of student records with marks
        Format: (student_id, last_name, first_name, current_mark)
    """
    return [
        ("1", "Reffas", "Chouaib", 15.5),
        ("2", "Amine", "Benkacem", 12.0),
        ("3", "Sara", "Belkacem", None),
        ("4", "Youssef", "Haddad", 14.0),
    ]


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
    logger.info(f"Mock: Added student {first_name} {last_name}")
    return True


def update_student(student_id, last_name, first_name, dob, address, city, zip_code, phone, fax, email, group_id, section_id):
    """
    Update an existing student's information
    
    Args:
        student_id (int): Student ID to update
        (same parameters as add_student)
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Updated student {student_id}")
    return True


def delete_student(student_id):
    """
    Delete a student from the database
    
    Args:
        student_id (int): Student ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Deleted student {student_id}")
    return True



#? INSTRUCTOR OPERATIONS


def get_all_instructors():
    """
    Retrieve all instructors from the database
    
    Returns:
        list[tuple]: List of instructor records
        Format: (instructor_id, department_id, last_name, first_name, 
                 rank, phone, fax, email)
    """
    return [
        (1, 101, "BenAbbes", "Abbas", "PROF", "0661112233", "031112233", "abbas.b@univ.dz"),
        (2, 101, "BenMokhtar", "Mokhtar", "MCA", "0662223344", "031223344", "mokhtar.b@univ.dz"),
        (3, 102, "BenMohamed", "Djemaa", "MCB", "0663334455", "031334455", "djemaa.b@univ.dz"),
        (4, 102, "Mohamed", "Lahlou", "PROF", "0664445566", "031445566", "lahlou.m@univ.dz"),
        (5, 103, "Chad", "Abla", "Substitute", "0665556677", "031556677", "abla.c@univ.dz"),
    ]


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
    logger.info(f"Mock: Added instructor {first_name} {last_name}")
    return True


def update_instructor(instructor_id, department_id, last_name, first_name, rank, phone, fax, email):
    """
    Update an existing instructor's information
    
    Args:
        instructor_id (int): Instructor ID to update
        (same parameters as add_instructor)
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Updated instructor {instructor_id}")
    return True


def delete_instructor(instructor_id):
    """
    Delete an instructor from the database
    
    Args:
        instructor_id (int): Instructor ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Deleted instructor {instructor_id}")
    return True



#? COURSE OPERATIONS


def get_all_courses():
    """
    Retrieve all courses from the database
    
    Returns:
        list[tuple]: List of course records
        Format: (course_id, department_id, name, description)
    """
    return [
        (1, 101, "Databases", "Introduction to Relational Databases"),
        (2, 101, "Advanced Databases", "NoSQL and Big Data"),
        (3, 101, "Software Engineering", "SDLC and Agile Methodologies"),
        (4, 102, "Operating Systems", "Process Management and Memory"),
        (5, 102, "Computer Networks", "TCP/IP and Routing"),
    ]


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
    logger.info(f"Mock: Added course {name}")
    return True


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
    logger.info(f"Mock: Updated course {course_id}")
    return True


def delete_course(course_id, department_id):
    """
    Delete a course from the database
    
    Args:
        course_id (int): Course ID to delete
        department_id (int): Department ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Deleted course {course_id}")
    return True



#? DEPARTMENT OPERATIONS


def get_all_departments():
    """
    Retrieve all departments from the database
    
    Returns:
        list[tuple]: List of department records
        Format: (department_id, name)
    """
    return [
        (101, "Computer Science"),
        (102, "Information Technology"),
        (103, "Software Engineering"),
        (104, "Artificial Intelligence"),
    ]


def add_department(department_id, name):
    """
    Insert a new department into the database
    
    Args:
        department_id (int): Department ID
        name (str): Department name
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Added department {name}")
    return True


def update_department(department_id, name):
    """
    Update an existing department's information
    
    Args:
        department_id (int): Department ID to update
        name (str): New department name
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Updated department {department_id}")
    return True


def delete_department(department_id):
    """
    Delete a department from the database
    
    Args:
        department_id (int): Department ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Deleted department {department_id}")
    return True



#? ROOM OPERATIONS


def get_all_rooms():
    """
    Retrieve all rooms from the database
    
    Returns:
        list[tuple]: List of room records
        Format: (building, roomno, capacity)
    """
    return [
        ("A", "101", 50),
        ("A", "102", 40),
        ("B", "201", 100),
        ("B", "LAB1", 25),
        ("C", "AUDITORIUM", 300),
    ]


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
    logger.info(f"Mock: Added room {building} {roomno}")
    return True


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
    logger.info(f"Mock: Updated room {building} {roomno}")
    return True


def delete_room(building, roomno):
    """
    Delete a room from the database
    
    Args:
        building (str): Building code
        roomno (str): Room number
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Deleted room {building} {roomno}")
    return True



#? SECTION OPERATIONS


def get_all_sections():
    """
    Retrieve all sections from the database
    
    Returns:
        list[tuple]: List of section records
        Format: (section_id, section_name)
    """
    return [
        ("A", "Section A"),
        ("B", "Section B"),
        ("C", "Section C"),
    ]


def add_section(section_id, section_name):
    """
    Insert a new section into the database
    
    Args:
        section_id (str): Section ID (single character)
        section_name (str): Section name
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Added section {section_name}")
    return True


def update_section(section_id, section_name):
    """
    Update an existing section's information
    
    Args:
        section_id (str): Section ID to update
        section_name (str): New section name
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Updated section {section_id}")
    return True


def delete_section(section_id):
    """
    Delete a section from the database
    
    Args:
        section_id (str): Section ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Deleted section {section_id}")
    return True



#? GROUP OPERATIONS


def get_all_groups():
    """
    Retrieve all groups from the database
    
    Returns:
        list[tuple]: List of group records
        Format: (group_id, group_name)
    """
    return [
        (1, "Group 1"),
        (2, "Group 2"),
        (3, "Group 3"),
        (4, "Group 4"),
    ]


def add_group(group_id, group_name):
    """
    Insert a new group into the database
    
    Args:
        group_id (int): Group ID
        group_name (str): Group name
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Added group {group_name}")
    return True


def update_group(group_id, group_name):
    """
    Update an existing group's information
    
    Args:
        group_id (int): Group ID to update
        group_name (str): New group name
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Updated group {group_id}")
    return True


def delete_group(group_id):
    """
    Delete a group from the database
    
    Args:
        group_id (int): Group ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Deleted group {group_id}")
    return True



#? RESERVATION OPERATIONS


def get_all_reservations():
    """
    Retrieve all reservations from the database
    
    Returns:
        list[tuple]: List of reservation records
        Format: (reservation_id, building, roomno, course_id, department_id,
                 instructor_id, reserv_date, start_time, end_time, hours_number)
    """
    return [
        (1, "A", "101", 1, 101, 1, "2025-10-01", "08:00:00", "10:00:00", 2),
        (2, "B", "201", 2, 101, 2, "2025-10-01", "10:00:00", "12:00:00", 2),
        (3, "C", "AUDITORIUM", 3, 102, 4, "2025-10-02", "14:00:00", "16:00:00", 2),
    ]


def get_reservations_by_filter(room=None, date=None):
    """
    Retrieve reservations filtered by room and/or date
    
    Args:
        room (str, optional): Room identifier ("Building RoomNo")
        date (str, optional): Date string (YYYY-MM-DD)
        
    Returns:
        list[tuple]: List of reservation records
    """
    return get_all_reservations()


def get_reservation_details(reservation_id):
    """
    Get detailed information about a specific reservation including names
    
    Args:
        reservation_id (int): Reservation ID
        
    Returns:
        dict: Dictionary with all reservation details including course and instructor names
    """
    return {
        "reservation_id": reservation_id,
        "room": "A 101",
        "course_name": "Databases",
        "instructor_name": "Dr. Abbas",
        "date": "2025-10-01",
        "start_time": "08:00:00",
        "end_time": "10:00:00",
        "hours": 2
    }


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
        tuple: (success: bool, new_reservation_id: int) 
    """
    mock_new_id = 999
    logger.info(f"Mock: Added reservation - Building: {building}, Room: {roomno}, Course: {course_id}")
    return (True, mock_new_id)


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
    logger.info(f"Mock: Updated reservation {reservation_id}")
    return True


def delete_reservation(reservation_id):
    """
    Delete a reservation from the database
    
    Args:
        reservation_id (int): Reservation ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Deleted reservation {reservation_id}")
    return True


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
    logger.info(f"Mock: Checking availability for {building} {roomno} on {reserv_date}")
    return True


def get_courses_for_reservation():
    """
    Get list of courses formatted for reservation dropdowns
    
    Returns:
        list[tuple]: List of (course_id, display_name, department_id)
    """
    courses = get_all_courses()
    result = []
    for course_id, dept_id, name, desc in courses:
        display = f"{name} (Dept {dept_id})"
        result.append((course_id, display, dept_id))
    return result


def get_instructors_for_reservation():
    """
    Get list of instructors formatted for reservation dropdowns
    
    Returns:
        list[tuple]: List of (instructor_id, display_name, department_id)
    """
    instructors = get_all_instructors()
    result = []
    for inst_id, dept_id, last_name, first_name, rank, phone, fax, email in instructors:
        display = f"{rank} {first_name} {last_name}"
        result.append((inst_id, display, dept_id))
    return result



#? ENROLLMENT OPERATIONS


def get_all_enrollments():
    """
    Retrieve all enrollments from the database
    
    Returns:
        list[tuple]: List of enrollment records
        Format: (student_id, course_id, department_id, enrollment_date)
    """
    return [
        ("1", 1, 101, "2025-09-15"),
        ("1", 2, 101, "2025-09-15"),
        ("2", 1, 101, "2025-09-16"),
        ("3", 4, 102, "2025-09-20"),
    ]


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
    logger.info(f"Mock: Added enrollment - Student: {student_id}, Course: {course_id}")
    return True


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
    logger.info(f"Mock: Updated enrollment - Student: {student_id}, Course: {course_id}")
    return True


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
    logger.info(f"Mock: Deleted enrollment - Student: {student_id}, Course: {course_id}")
    return True



#? MARK OPERATIONS


def get_all_marks():
    """
    Retrieve all marks from the database
    
    Returns:
        list[tuple]: List of mark records
        Format: (mark_id, student_id, course_id, department_id, mark_value, mark_date)
    """
    return [
        (1, "1", 1, 101, 15.5, "2025-11-20"),
        (2, "1", 2, 101, 12.0, "2025-11-22"),
        (3, "2", 1, 101, 18.0, "2025-11-20"),
    ]


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
    logger.info(f"Mock: Added mark - Student: {student_id}, Course: {course_id}, Value: {mark_value}")
    return True


def update_mark(mark_id, student_id, course_id, department_id, mark_value, mark_date):
    """
    Update an existing mark's information
    
    Args:
        mark_id (int): Mark ID to update
        (same parameters as add_mark)
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Updated mark {mark_id}")
    return True


def delete_mark(mark_id):
    """
    Delete a mark from the database
    
    Args:
        mark_id (int): Mark ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Deleted mark {mark_id}")
    return True


def save_bulk_marks(marks_records):
    """
    Save multiple marks at once
    
    Args:
        marks_records (list): List of dicts with student_id, course_id, exam_id, mark_value
        
    Returns:
        bool: True if successful
    """
    logger.info(f"Mock: Saved {len(marks_records)} marks in bulk")
    return True



#? ACTIVITY OPERATIONS


def get_all_activities():
    """
    Retrieve all activities from the database
    
    Returns:
        list[tuple]: List of activity records
        Format: (activity_id, activity_type, course_name)
    """
    return [
        (1, "Lecture", "Databases"),
        (2, "Tutorial", "Databases"),
        (3, "Lab", "Advanced Databases"),
        (4, "Lecture", "Operating Systems"),
    ]


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
    logger.info(f"Mock: Added activity {activity_type} for course {course_id}")
    return True


def update_activity(activity_id, activity_type, reservation_id, course_id, department_id):
    """
    Update an existing activity's information
    
    Args:
        activity_id (int): Activity ID to update
        (same parameters as add_activity)
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Updated activity {activity_id}")
    return True


def delete_activity(activity_id):
    """
    Delete an activity from the database
    
    Args:
        activity_id (int): Activity ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Deleted activity {activity_id}")
    return True



#? EXAM OPERATIONS


def get_all_exams():
    """
    Retrieve all exams from the database
    
    Returns:
        list[tuple]: List of exam records
        Format: (exam_id, duration, exam_type, course_id, department_id)
    """
    return [
        (1, 120, "Midterm", 1, 101),
        (2, 180, "Final", 1, 101),
        (3, 60, "Quiz", 2, 101),
    ]


def get_exams_by_course(course_id):
    """
    Retrieve exams for a specific course
    
    Args:
        course_id (int): Course ID
    
    Returns:
        list[tuple]: List of exam records
        Format: (exam_id, exam_type, duration, department_id)
    """
    return [
        (1, "Midterm", 120, 101),
        (2, "Final", 180, 101),
        (3, "Quiz", 60, 101),
    ]


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
    logger.info(f"Mock: Added exam {exam_type} for course {course_id}")
    return True


def update_exam(exam_id, duration, exam_type, course_id, department_id):
    """
    Update an existing exam's information
    
    Args:
        exam_id (int): Exam ID to update
        (same parameters as add_exam)
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Updated exam {exam_id}")
    return True


def delete_exam(exam_id):
    """
    Delete an exam from the database
    
    Args:
        exam_id (int): Exam ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock: Deleted exam {exam_id}")
    return True



#? ATTENDANCE OPERATIONS


def get_all_attendance():
    """
    Retrieve all attendance records from the database
    
    Returns:
        list[tuple]: List of attendance records
        Format: (student_id, activity_id, attendance_date, status)
    """
    return [
        ("1", 1, "2025-10-01", "Present"),
        ("2", 1, "2025-10-01", "Absent"),
        ("3", 1, "2025-10-01", "Present"),
    ]


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
    logger.info(f"Mock: Added attendance - Student: {student_id}, Activity: {activity_id}")
    return True


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
    logger.info(f"Mock: Updated attendance - Student: {student_id}, Activity: {activity_id}")
    return True


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
    logger.info(f"Mock: Deleted attendance - Student: {student_id}, Activity: {activity_id}")
    return True


def save_bulk_attendance(attendance_records):
    """
    Save multiple attendance records at once
    
    Args:
        attendance_records (list): List of dicts with student_id, activity_id, date, status
        
    Returns:
        bool: True if successful
    """
    logger.info(f"Mock: Saved {len(attendance_records)} attendance records in bulk")
    return True



#? INSTRUCTOR-COURSE ASSIGNMENT OPERATIONS


def get_all_instructor_course_assignments():
    """
    Retrieve all instructor-course assignments from the database
    
    Returns:
        list[tuple]: List of assignment records
        Format: (instructor_id, instructor_name, course_id, course_name, department_id, assignment_date)
    """
    return [
        (1, "Dr. Abbas BenAbbes", 1, "Databases", 101, "2025-09-01"),
        (2, "Dr. Mokhtar BenMokhtar", 2, "Advanced Databases", 101, "2025-09-01"),
    ]


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
    logger.info(f"Mock: Assigned instructor {instructor_id} to course {course_id}")
    return True


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
    logger.info(f"Mock: Removed instructor {instructor_id} from course {course_id}")
    return True


def get_instructor_list_with_ids():
    """
    Retrieve list of instructors with their IDs for assignment
    
    Returns:
        list[tuple]: List of (instructor_id, full_name, department_id)
    """
    instructors = get_all_instructors()
    result = []
    for instructor in instructors:
        instructor_id, dept_id, last_name, first_name, rank, phone, fax, email = instructor
        full_name = f"Dr. {first_name} {last_name}"
        result.append((instructor_id, full_name, dept_id))
    return result


def get_course_list_with_ids():
    """
    Retrieve list of courses with their IDs for assignment
    
    Returns:
        list[tuple]: List of (course_id, course_name, department_id)
    """
    courses = get_all_courses()
    result = []
    for course in courses:
        course_id, dept_id, name, desc = course
        result.append((course_id, name, dept_id))
    return result



#? QUERY OPERATIONS


def get_available_queries():
    """
    Retrieve list of available pre-defined queries
    
    Returns:
        list[str]: List of query names/descriptions
    """
    return [
        "Students with average grade > 15",
        "Courses with no enrolled students",
        "Instructors teaching > 3 courses",
        "Rooms fully booked today",
    ]


def execute_query(query_name):
    """
    Execute a specific named query
    
    Args:
        query_name (str): The name/ID of the query to execute
        
    Returns:
        tuple: (headers, data) where headers is list of strings, data is list of rows
    """
    if "average grade" in query_name:
        headers = ["Student ID", "First Name", "Last Name", "Average"]
        data = [
            ("3", "Sara", "Belkacem", 16.5),
            ("4", "Youssef", "Haddad", 15.2),
        ]
        return headers, data
    else:
        headers = ["Result"]
        data = [("Mock Result 1",), ("Mock Result 2",)]
        return headers, data



#? AUDIT OPERATIONS


def get_audit_logs(from_date, to_date, table_name):
    """
    Retrieve audit logs filtered by date range and table
    
    Args:
        from_date (str): Start date
        to_date (str): End date
        table_name (str): Table name filter
        
    Returns:
        list[tuple]: List of log records
    """
    return [
        ("2025-12-28 10:00", "admin", "INSERT", "Students", "Added Student 100"),
        ("2025-12-28 11:30", "admin", "UPDATE", "Marks", "Changed mark for Student 1"),
        ("2025-12-29 09:15", "user", "DELETE", "Reservations", "Removed Reservation 5"),
    ]


def get_table_names():
    """
    Retrieve list of database table names
    
    Returns:
        list[str]: List of tables
    """
    return ["Students", "Instructors", "Courses", "Marks", "Attendance", "Reservations"]



#? RESULTS OPERATIONS


def get_student_results(semester, course_id):
    """
    Retrieve results for a specific semester and course
    
    Args:
        semester (str): Semester ID/Name
        course_id (int): Course ID
        
    Returns:
        list[tuple]: List of student results
    """
    return [
        ("1", "Reffas Chouaib", 15.5, "Pass"),
        ("2", "Amine Benkacem", 12.0, "Pass"),
        ("3", "Sara Belkacem", 18.0, "Distinction"),
    ]


def get_semesters_list():
    """
    Retrieve list of semesters
    
    Returns:
        list[str]: List of semesters
    """
    return ["S1 2025/2026", "S2 2025/2026", "S1 2024/2025"]



#? PERFORMANCE OPERATIONS


def get_performance_stats():
    """
    Retrieve general performance statistics
    
    Returns:
        dict: Dictionary of statistics
    """
    return {
        "Total Students": 1500,
        "Average GPA": 12.5,
        "Attendance Rate": "85%",
        "Pass Rate": "92%",
    }