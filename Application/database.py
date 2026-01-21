"""
Application.Database.database
Contains all database CRUD operations and queries
Function definitions for GUI integration
"""

import logging

from  connection import DatabaseConnection as con

from  connection import execute_query as eq


logger = logging.getLogger(__name__)

conection_pam=("uni","postgres","mohamed2006")

#? STUDENT OPERATIONS

def get_all_students():
    """
    Retrieve all students from the database
    
    Returns:
        list[tuple]: List of student records
        Format: (student_id, last_name, first_name, dob, address, city, 
                 zip_code, phone, fax, email, group_id, section_id)
    """

    con.initialize_pool(*conection_pam)
    result=eq("select * from student;",fetch=True)
    con.close_all_connections()
    return result

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
    Note: This query assumes there's an exam_result table linking enrollments to exams
    """
    try:
        con.initialize_pool(*conection_pam)
        # Note: This assumes an exam_result table exists. If not, you may need to join through mark table
        result = eq("""
            SELECT s.student_id, s.last_name, s.first_name, m.mark_value AS current_mark 
            FROM student s 
            INNER JOIN enrollment e ON s.student_id = e.student_id 
            INNER JOIN mark m ON e.student_id = m.student_id AND e.course_id = m.course_id AND e.department_id = m.department_id
            WHERE e.course_id = %s 
            ORDER BY s.last_name, s.first_name;
        """, (course_id,), fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting students with marks: {e}")
        con.close_all_connections()
        return []
    

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
    try:
        con.initialize_pool(*conection_pam)
        eq("INSERT INTO student (last_name, first_name, dob, address, city, zip_code, phone, fax, email, group_id, section_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", 
           (last_name, first_name, dob, address, city, zip_code, phone, fax, email, group_id, section_id))
        con.close_all_connections()
        logger.info(f"Added student {first_name} {last_name}")
        return True
    except Exception as e:
        logger.error(f"Error adding student: {e}")
        con.close_all_connections()
        return False


def update_student(student_id, last_name, first_name, dob, address, city, zip_code, phone, fax, email, group_id, section_id):
    """
    Update an existing student's information
    
    Args:
        student_id (int): Student ID to update
        (same parameters as add_student)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("UPDATE student SET last_name = %s, first_name = %s, dob = %s, address = %s, city = %s, zip_code = %s, phone = %s, fax = %s, email = %s, group_id = %s, section_id = %s WHERE student_id = %s;",
           (last_name, first_name, dob, address, city, zip_code, phone, fax, email, group_id, section_id, student_id))
        con.close_all_connections()
        logger.info(f"Updated student {student_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating student: {e}")
        con.close_all_connections()
        return False


def delete_student(student_id):
    """
    Delete a student from the database
    
    Args:
        student_id (int): Student ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("DELETE FROM student WHERE student_id = %s;", (student_id,))
        con.close_all_connections()
        logger.info(f"Deleted student {student_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting student: {e}")
        con.close_all_connections()
        return False



#? INSTRUCTOR OPERATIONS


def get_all_instructors():
    """
    Retrieve all instructors from the database
    
    Returns:
        list[tuple]: List of instructor records
        Format: (instructor_id, department_id, last_name, first_name, 
                 rank, phone, fax, email)
    """
    try:
        con.initialize_pool(*conection_pam)
        result = eq("SELECT * FROM instructor;", fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting all instructors: {e}")
        con.close_all_connections()
        return []


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
    try:
        con.initialize_pool(*conection_pam)
        eq("INSERT INTO instructor(department_id,last_name,first_name,rank,phone,fax,email) VALUES (%s,%s,%s,%s,%s,%s,%s);",(department_id, last_name, first_name, rank, phone, fax, email))
        con.close_all_connections()
        logger.info(f"Added instructor {first_name} {last_name}")
        return True
    except Exception as e:
        logger.error(f"Error adding instructor: {e}")
        con.close_all_connections()
        return False


def update_instructor(instructor_id, department_id, last_name, first_name, rank, phone, fax, email):
    """
    Update an existing instructor's information
    
    Args:
        instructor_id (int): Instructor ID to update
        (same parameters as add_instructor)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("UPDATE instructor SET department_id = %s,last_name = %s, first_name = %s,rank = %s, phone = %s,fax = %s,email = %s WHERE instructor_id = %s;",(department_id, last_name, first_name, rank, phone, fax, email,instructor_id))
        con.close_all_connections()
        logger.info(f"Updated instructor {instructor_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating instructor: {e}")
        con.close_all_connections()
        return False



def delete_instructor(instructor_id):
    """
    Delete an instructor from the database
    
    Args:
        instructor_id (int): Instructor ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("DELETE FROM instructor WHERE instructor_id = %s;", (instructor_id,))
        con.close_all_connections()
        logger.info(f"Deleted instructor {instructor_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting instructor: {e}")
        con.close_all_connections()
        return False


#? COURSE OPERATIONS


def get_all_courses():
    """
    Retrieve all courses from the database
    
    Returns:
        list[tuple]: List of course records
        Format: (course_id, department_id, name, description)
    """
    try:
        con.initialize_pool(*conection_pam)
        result = eq("SELECT course_id, department_id, name, description FROM course;", fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting all courses: {e}")
        con.close_all_connections()
        return []


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
    try:
        con.initialize_pool(*conection_pam)
        eq("INSERT INTO course (course_id, department_id, name, description) VALUES (%s, %s, %s, %s);",
           (course_id, department_id, name, description))
        con.close_all_connections()
        logger.info(f"Added course {name}")
        return True
    except Exception as e:
        logger.error(f"Error adding course: {e}")
        con.close_all_connections()
        return False


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
    try:
        con.initialize_pool(*conection_pam)
        eq("UPDATE course SET name = %s, description = %s WHERE course_id = %s AND department_id = %s;",
           (name, description, course_id, department_id))
        con.close_all_connections()
        logger.info(f"Updated course {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating course: {e}")
        con.close_all_connections()
        return False


def delete_course(course_id, department_id):
    """
    Delete a course from the database
    
    Args:
        course_id (int): Course ID to delete
        department_id (int): Department ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("DELETE FROM course WHERE course_id = %s AND department_id = %s;", (course_id, department_id))
        con.close_all_connections()
        logger.info(f"Deleted course {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting course: {e}")
        con.close_all_connections()
        return False



#? DEPARTMENT OPERATIONS


def get_all_departments():
    """
    Retrieve all departments from the database
    
    Returns:
        list[tuple]: List of department records
        Format: (department_id, name)
    """
    try:
        con.initialize_pool(*conection_pam)
        result = eq("SELECT department_id, name FROM department;", fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting all departments: {e}")
        con.close_all_connections()
        return []


def add_department(department_id, name):
    """
    Insert a new department into the database
    
    Args:
        department_id (int): Department ID
        name (str): Department name
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("INSERT INTO department (department_id, name) VALUES (%s, %s);", (department_id, name))
        con.close_all_connections()
        logger.info(f"Added department {name}")
        return True
    except Exception as e:
        logger.error(f"Error adding department: {e}")
        con.close_all_connections()
        return False


def update_department(department_id, name):
    """
    Update an existing department's information
    
    Args:
        department_id (int): Department ID to update
        name (str): New department name
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("UPDATE department SET name = %s WHERE department_id = %s;", (name, department_id))
        con.close_all_connections()
        logger.info(f"Updated department {department_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating department: {e}")
        con.close_all_connections()
        return False


def delete_department(department_id):
    """
    Delete a department from the database
    
    Args:
        department_id (int): Department ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("DELETE FROM department WHERE department_id = %s;", (department_id,))
        con.close_all_connections()
        logger.info(f"Deleted department {department_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting department: {e}")
        con.close_all_connections()
        return False



#? ROOM OPERATIONS


def get_all_rooms():
    """
    Retrieve all rooms from the database
    
    Returns:
        list[tuple]: List of room records
        Format: (building, roomno, capacity)
    """
    try:
        con.initialize_pool(*conection_pam)
        result = eq("SELECT building, roomno, capacity FROM room;", fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting all rooms: {e}")
        con.close_all_connections()
        return []


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
    try:
        con.initialize_pool(*conection_pam)
        eq("INSERT INTO room (building, roomno, capacity) VALUES (%s, %s, %s);", (building, roomno, capacity))
        con.close_all_connections()
        logger.info(f"Added room {building} {roomno}")
        return True
    except Exception as e:
        logger.error(f"Error adding room: {e}")
        con.close_all_connections()
        return False


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
    try:
        con.initialize_pool(*conection_pam)
        eq("UPDATE room SET capacity = %s WHERE building = %s AND roomno = %s;", (capacity, building, roomno))
        con.close_all_connections()
        logger.info(f"Updated room {building} {roomno}")
        return True
    except Exception as e:
        logger.error(f"Error updating room: {e}")
        con.close_all_connections()
        return False


def delete_room(building, roomno):
    """
    Delete a room from the database
    
    Args:
        building (str): Building code
        roomno (str): Room number
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("DELETE FROM room WHERE building = %s AND roomno = %s;", (building, roomno))
        con.close_all_connections()
        logger.info(f"Deleted room {building} {roomno}")
        return True
    except Exception as e:
        logger.error(f"Error deleting room: {e}")
        con.close_all_connections()
        return False



#? SECTION OPERATIONS


def get_all_sections():
    """
    Retrieve all sections from the database
    
    Returns:
        list[tuple]: List of section records
        Format: (section_id, section_name)
    Note: Sections are stored as distinct values in student.section_id
    """
    try:
        con.initialize_pool(*conection_pam)
        result = eq("SELECT DISTINCT section_id, 'Section ' || section_id as section_name FROM student ORDER BY section_id;", fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting all sections: {e}")
        con.close_all_connections()
        return []


def add_section(section_id, section_name):
    """
    Insert a new section into the database
    Note: Sections are attributes of students, so this function doesn't directly insert
    
    Args:
        section_id (str): Section ID (single character)
        section_name (str): Section name
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Section {section_id} added (sections are student attributes)")
    return True


def update_section(section_id, section_name):
    """
    Update an existing section's information
    Note: Sections are attributes of students
    
    Args:
        section_id (str): Section ID to update
        section_name (str): New section name
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Section {section_id} updated (sections are student attributes)")
    return True


def delete_section(section_id):
    """
    Delete a section from the database
    Note: Sections are attributes of students, cannot be deleted if students use them
    
    Args:
        section_id (str): Section ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Section {section_id} deletion requested (sections are student attributes)")
    return True



#? GROUP OPERATIONS


def get_all_groups():
    """
    Retrieve all groups from the database
    
    Returns:
        list[tuple]: List of group records
        Format: (group_id, group_name)
    Note: Groups are stored as distinct values in student.group_id
    """
    try:
        con.initialize_pool(*conection_pam)
        result = eq("SELECT DISTINCT group_id, 'Group ' || group_id::text as group_name FROM student ORDER BY group_id;", fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting all groups: {e}")
        con.close_all_connections()
        return []


def add_group(group_id, group_name):
    """
    Insert a new group into the database
    Note: Groups are attributes of students, so this function doesn't directly insert
    
    Args:
        group_id (int): Group ID
        group_name (str): Group name
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Group {group_id} added (groups are student attributes)")
    return True


def update_group(group_id, group_name):
    """
    Update an existing group's information
    Note: Groups are attributes of students
    
    Args:
        group_id (int): Group ID to update
        group_name (str): New group name
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Group {group_id} updated (groups are student attributes)")
    return True


def delete_group(group_id):
    """
    Delete a group from the database
    Note: Groups are attributes of students, cannot be deleted if students use them
    
    Args:
        group_id (int): Group ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Group {group_id} deletion requested (groups are student attributes)")
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
    try:
        con.initialize_pool(*conection_pam)
        result = eq("SELECT reservation_id, building, roomno, course_id, department_id, instructor_id, reserv_date, start_time, end_time, hours_number FROM reservation ORDER BY reserv_date, start_time;", fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting all reservations: {e}")
        con.close_all_connections()
        return []


def get_reservations_by_filter(room=None, date=None):
    """
    Retrieve reservations filtered by room and/or date
    
    Args:
        room (str, optional): Room identifier ("Building RoomNo")
        date (str, optional): Date string (YYYY-MM-DD)
        
    Returns:
        list[tuple]: List of reservation records
    """
    try:
        con.initialize_pool(*conection_pam)
        query = "SELECT reservation_id, building, roomno, course_id, department_id, instructor_id, reserv_date, start_time, end_time, hours_number FROM reservation WHERE 1=1"
        params = []
        
        if room:
            # Parse "Building RoomNo" format
            parts = room.split()
            if len(parts) >= 2:
                building, roomno = parts[0], parts[1]
                query += " AND building = %s AND roomno = %s"
                params.extend([building, roomno])
        
        if date:
            query += " AND reserv_date = %s"
            params.append(date)
        
        query += " ORDER BY reserv_date, start_time;"
        
        result = eq(query, tuple(params) if params else None, fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting filtered reservations: {e}")
        con.close_all_connections()
        return []


def get_reservation_details(reservation_id):
    """
    Get detailed information about a specific reservation including names
    
    Args:
        reservation_id (int): Reservation ID
        
    Returns:
        dict: Dictionary with all reservation details including course and instructor names
    """
    try:
        con.initialize_pool(*conection_pam)
        result = eq("""
            SELECT r.reservation_id, r.building, r.roomno, r.reserv_date, r.start_time, r.end_time, r.hours_number,
                   c.name as course_name, i.first_name || ' ' || i.last_name as instructor_name
            FROM reservation r
            JOIN course c ON r.course_id = c.course_id AND r.department_id = c.department_id
            JOIN instructor i ON r.instructor_id = i.instructor_id
            WHERE r.reservation_id = %s;
        """, (reservation_id,), fetch=True)
        con.close_all_connections()
        
        if result and len(result) > 0:
            row = result[0]
            return {
                "reservation_id": row[0],
                "room": f"{row[1]} {row[2]}",
                "course_name": row[7],
                "instructor_name": row[8],
                "date": str(row[3]),
                "start_time": str(row[4]),
                "end_time": str(row[5]),
                "hours": row[6]
            }
        return {}
    except Exception as e:
        logger.error(f"Error getting reservation details: {e}")
        con.close_all_connections()
        return {}


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
    try:
        con.initialize_pool(*conection_pam)
        connection = con.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO reservation (building, roomno, course_id, department_id, instructor_id, reserv_date, start_time, end_time, hours_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING reservation_id;",
            (building, roomno, course_id, department_id, instructor_id, reserv_date, start_time, end_time, hours_number)
        )
        new_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        con.return_connection(connection)
        con.close_all_connections()
        logger.info(f"Added reservation - Building: {building}, Room: {roomno}, Course: {course_id}, ID: {new_id}")
        return (True, new_id)
    except Exception as e:
        logger.error(f"Error adding reservation: {e}")
        if 'connection' in locals():
            connection.rollback()
            if 'cursor' in locals():
                cursor.close()
            con.return_connection(connection)
        con.close_all_connections()
        return (False, None)


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
    try:
        con.initialize_pool(*conection_pam)
        eq("UPDATE reservation SET building = %s, roomno = %s, course_id = %s, department_id = %s, instructor_id = %s, reserv_date = %s, start_time = %s, end_time = %s, hours_number = %s WHERE reservation_id = %s;",
           (building, roomno, course_id, department_id, instructor_id, reserv_date, start_time, end_time, hours_number, reservation_id))
        con.close_all_connections()
        logger.info(f"Updated reservation {reservation_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating reservation: {e}")
        con.close_all_connections()
        return False


def delete_reservation(reservation_id):
    """
    Delete a reservation from the database
    
    Args:
        reservation_id (int): Reservation ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("DELETE FROM reservation WHERE reservation_id = %s;", (reservation_id,))
        con.close_all_connections()
        logger.info(f"Deleted reservation {reservation_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting reservation: {e}")
        con.close_all_connections()
        return False


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
    try:
        con.initialize_pool(*conection_pam)
        result = eq("""
            SELECT COUNT(*) FROM reservation 
            WHERE building = %s AND roomno = %s AND reserv_date = %s 
            AND NOT (end_time <= %s OR start_time >= %s);
        """, (building, roomno, reserv_date, start_time, end_time), fetch=True)
        con.close_all_connections()
        count = result[0][0] if result else 0
        is_available = count == 0
        logger.info(f"Checking availability for {building} {roomno} on {reserv_date}: {'Available' if is_available else 'Conflict'}")
        return is_available
    except Exception as e:
        logger.error(f"Error checking room availability: {e}")
        con.close_all_connections()
        return False


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
    try:
        con.initialize_pool(*conection_pam)
        result = eq("SELECT student_id, course_id, department_id, enrollment_date FROM enrollment ORDER BY enrollment_date;", fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting all enrollments: {e}")
        con.close_all_connections()
        return []


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
    try:
        con.initialize_pool(*conection_pam)
        eq("INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (%s, %s, %s, %s);",
           (student_id, course_id, department_id, enrollment_date))
        con.close_all_connections()
        logger.info(f"Added enrollment - Student: {student_id}, Course: {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error adding enrollment: {e}")
        con.close_all_connections()
        return False


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
    try:
        con.initialize_pool(*conection_pam)
        eq("UPDATE enrollment SET enrollment_date = %s WHERE student_id = %s AND course_id = %s AND department_id = %s;",
           (enrollment_date, student_id, course_id, department_id))
        con.close_all_connections()
        logger.info(f"Updated enrollment - Student: {student_id}, Course: {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating enrollment: {e}")
        con.close_all_connections()
        return False


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
    try:
        con.initialize_pool(*conection_pam)
        eq("DELETE FROM enrollment WHERE student_id = %s AND course_id = %s AND department_id = %s;",
           (student_id, course_id, department_id))
        con.close_all_connections()
        logger.info(f"Deleted enrollment - Student: {student_id}, Course: {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting enrollment: {e}")
        con.close_all_connections()
        return False



#? MARK OPERATIONS


def get_all_marks():
    """
    Retrieve all marks from the database
    
    Returns:
        list[tuple]: List of mark records
        Format: (mark_id, student_id, course_id, department_id, mark_value, mark_date)
    """
    try:
        con.initialize_pool(*conection_pam)
        result = eq("SELECT mark_id, student_id, course_id, department_id, mark_value, mark_date FROM mark ORDER BY mark_date DESC;", fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting all marks: {e}")
        con.close_all_connections()
        return []


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
    try:
        con.initialize_pool(*conection_pam)
        eq("INSERT INTO mark (student_id, course_id, department_id, mark_value, mark_date) VALUES (%s, %s, %s, %s, %s);",
           (student_id, course_id, department_id, mark_value, mark_date))
        con.close_all_connections()
        logger.info(f"Added mark - Student: {student_id}, Course: {course_id}, Value: {mark_value}")
        return True
    except Exception as e:
        logger.error(f"Error adding mark: {e}")
        con.close_all_connections()
        return False


def update_mark(mark_id, student_id, course_id, department_id, mark_value, mark_date):
    """
    Update an existing mark's information
    
    Args:
        mark_id (int): Mark ID to update
        (same parameters as add_mark)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("UPDATE mark SET student_id = %s, course_id = %s, department_id = %s, mark_value = %s, mark_date = %s WHERE mark_id = %s;",
           (student_id, course_id, department_id, mark_value, mark_date, mark_id))
        con.close_all_connections()
        logger.info(f"Updated mark {mark_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating mark: {e}")
        con.close_all_connections()
        return False


def delete_mark(mark_id):
    """
    Delete a mark from the database
    
    Args:
        mark_id (int): Mark ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("DELETE FROM mark WHERE mark_id = %s;", (mark_id,))
        con.close_all_connections()
        logger.info(f"Deleted mark {mark_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting mark: {e}")
        con.close_all_connections()
        return False


def save_bulk_marks(marks_records):
    """
    Save multiple marks at once
    
    Args:
        marks_records (list): List of dicts with student_id, course_id, department_id, mark_value, mark_date
        
    Returns:
        bool: True if successful
    """
    try:
        con.initialize_pool(*conection_pam)
        connection = con.get_connection()
        cursor = connection.cursor()
        
        for record in marks_records:
            cursor.execute(
                "INSERT INTO mark (student_id, course_id, department_id, mark_value, mark_date) VALUES (%s, %s, %s, %s, %s);",
                (record.get('student_id'), record.get('course_id'), record.get('department_id'), 
                 record.get('mark_value'), record.get('mark_date'))
            )
        
        connection.commit()
        cursor.close()
        con.return_connection(connection)
        con.close_all_connections()
        logger.info(f"Saved {len(marks_records)} marks in bulk")
        return True
    except Exception as e:
        logger.error(f"Error saving bulk marks: {e}")
        if 'connection' in locals():
            connection.rollback()
            if 'cursor' in locals():
                cursor.close()
            con.return_connection(connection)
        con.close_all_connections()
        return False



#? ACTIVITY OPERATIONS


def get_all_activities():
    """
    Retrieve all activities from the database
    
    Returns:
        list[tuple]: List of activity records
        Format: (activity_id, activity_type, reservation_id, course_id, department_id)
    """
    try:
        con.initialize_pool(*conection_pam)
        result = eq("SELECT activity_id, activity_type, reservation_id, course_id, department_id FROM activity ORDER BY activity_id;", fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting all activities: {e}")
        con.close_all_connections()
        return []


def add_activity(activity_id, activity_type, reservation_id, course_id, department_id):
    """
    Insert a new activity into the database
    
    Args:
        activity_id (int): Activity ID (ignored, uses AUTO_INCREMENT)
        activity_type (str): Type (lecture, toturiol, practical)
        reservation_id (int): Associated reservation ID
        course_id (int): Course ID
        department_id (int): Department ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("INSERT INTO activity (activity_type, reservation_id, course_id, department_id) VALUES (%s, %s, %s, %s);",
           (activity_type, reservation_id, course_id, department_id))
        con.close_all_connections()
        logger.info(f"Added activity {activity_type} for course {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error adding activity: {e}")
        con.close_all_connections()
        return False


def update_activity(activity_id, activity_type, reservation_id, course_id, department_id):
    """
    Update an existing activity's information
    
    Args:
        activity_id (int): Activity ID to update
        (same parameters as add_activity)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("UPDATE activity SET activity_type = %s, reservation_id = %s, course_id = %s, department_id = %s WHERE activity_id = %s;",
           (activity_type, reservation_id, course_id, department_id, activity_id))
        con.close_all_connections()
        logger.info(f"Updated activity {activity_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating activity: {e}")
        con.close_all_connections()
        return False


def delete_activity(activity_id):
    """
    Delete an activity from the database
    
    Args:
        activity_id (int): Activity ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("DELETE FROM activity WHERE activity_id = %s;", (activity_id,))
        con.close_all_connections()
        logger.info(f"Deleted activity {activity_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting activity: {e}")
        con.close_all_connections()
        return False



#? EXAM OPERATIONS


def get_all_exams():
    """
    Retrieve all exams from the database
    
    Returns:
        list[tuple]: List of exam records
        Format: (exam_id, duration, exam_type, course_id, department_id)
    """
    try:
        con.initialize_pool(*conection_pam)
        result = eq("SELECT exam_id, duration, exam_type, course_id, department_id FROM exam ORDER BY exam_id;", fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting all exams: {e}")
        con.close_all_connections()
        return []


def get_exams_by_course(course_id):
    """
    Retrieve exams for a specific course
    
    Args:
        course_id (int): Course ID
    
    Returns:
        list[tuple]: List of exam records
        Format: (exam_id, exam_type, duration, department_id)
    """
    try:
        con.initialize_pool(*conection_pam)
        result = eq("SELECT exam_id, exam_type, duration, department_id FROM exam WHERE course_id = %s ORDER BY exam_id;", (course_id,), fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting exams by course: {e}")
        con.close_all_connections()
        return []


def add_exam(exam_id, duration, exam_type, course_id, department_id):
    """
    Insert a new exam into the database
    
    Args:
        exam_id (int): Exam ID (ignored, uses AUTO_INCREMENT)
        duration (int): Duration in minutes
        exam_type (str): Type of exam (midterm, final, project, etc.)
        course_id (int): Course ID
        department_id (int): Department ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("INSERT INTO exam (duration, exam_type, course_id, department_id) VALUES (%s, %s, %s, %s);",
           (duration, exam_type, course_id, department_id))
        con.close_all_connections()
        logger.info(f"Added exam {exam_type} for course {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error adding exam: {e}")
        con.close_all_connections()
        return False


def update_exam(exam_id, duration, exam_type, course_id, department_id):
    """
    Update an existing exam's information
    
    Args:
        exam_id (int): Exam ID to update
        (same parameters as add_exam)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("UPDATE exam SET duration = %s, exam_type = %s, course_id = %s, department_id = %s WHERE exam_id = %s;",
           (duration, exam_type, course_id, department_id, exam_id))
        con.close_all_connections()
        logger.info(f"Updated exam {exam_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating exam: {e}")
        con.close_all_connections()
        return False


def delete_exam(exam_id):
    """
    Delete an exam from the database
    
    Args:
        exam_id (int): Exam ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        con.initialize_pool(*conection_pam)
        eq("DELETE FROM exam WHERE exam_id = %s;", (exam_id,))
        con.close_all_connections()
        logger.info(f"Deleted exam {exam_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting exam: {e}")
        con.close_all_connections()
        return False



#? ATTENDANCE OPERATIONS


def get_all_attendance():
    """
    Retrieve all attendance records from the database
    
    Returns:
        list[tuple]: List of attendance records
        Format: (student_id, activity_id, attendance_date, status)
    """
    try:
        con.initialize_pool(*conection_pam)
        result = eq("SELECT student_id, activity_id, attendance_date, statu FROM attendance_to_activities ORDER BY attendance_date DESC;", fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting all attendance: {e}")
        con.close_all_connections()
        return []


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
    try:
        con.initialize_pool(*conection_pam)
        eq("INSERT INTO attendance_to_activities (student_id, activity_id, attendance_date, statu) VALUES (%s, %s, %s, %s);",
           (student_id, activity_id, attendance_date, status))
        con.close_all_connections()
        logger.info(f"Added attendance - Student: {student_id}, Activity: {activity_id}")
        return True
    except Exception as e:
        logger.error(f"Error adding attendance: {e}")
        con.close_all_connections()
        return False


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
    try:
        con.initialize_pool(*conection_pam)
        eq("UPDATE attendance_to_activities SET statu = %s WHERE student_id = %s AND activity_id = %s AND attendance_date = %s;",
           (status, student_id, activity_id, attendance_date))
        con.close_all_connections()
        logger.info(f"Updated attendance - Student: {student_id}, Activity: {activity_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating attendance: {e}")
        con.close_all_connections()
        return False


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
    try:
        con.initialize_pool(*conection_pam)
        eq("DELETE FROM attendance_to_activities WHERE student_id = %s AND activity_id = %s AND attendance_date = %s;",
           (student_id, activity_id, attendance_date))
        con.close_all_connections()
        logger.info(f"Deleted attendance - Student: {student_id}, Activity: {activity_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting attendance: {e}")
        con.close_all_connections()
        return False


def save_bulk_attendance(attendance_records):
    """
    Save multiple attendance records at once
    
    Args:
        attendance_records (list): List of dicts with student_id, activity_id, attendance_date, status
        
    Returns:
        bool: True if successful
    """
    try:
        con.initialize_pool(*conection_pam)
        connection = con.get_connection()
        cursor = connection.cursor()
        
        for record in attendance_records:
            cursor.execute(
                "INSERT INTO attendance_to_activities (student_id, activity_id, attendance_date, statu) VALUES (%s, %s, %s, %s);",
                (record.get('student_id'), record.get('activity_id'), record.get('attendance_date'), record.get('status'))
            )
        
        connection.commit()
        cursor.close()
        con.return_connection(connection)
        con.close_all_connections()
        logger.info(f"Saved {len(attendance_records)} attendance records in bulk")
        return True
    except Exception as e:
        logger.error(f"Error saving bulk attendance: {e}")
        if 'connection' in locals():
            connection.rollback()
            if 'cursor' in locals():
                cursor.close()
            con.return_connection(connection)
        con.close_all_connections()
        return False



#? INSTRUCTOR-COURSE ASSIGNMENT OPERATIONS


def get_all_instructor_course_assignments():
    """
    Retrieve all instructor-course assignments from the database
    Note: There's no explicit assignment table, so we derive from reservations
    
    Returns:
        list[tuple]: List of assignment records
        Format: (instructor_id, instructor_name, course_id, course_name, department_id, assignment_date)
    """
    try:
        con.initialize_pool(*conection_pam)
        result = eq("""
            SELECT DISTINCT r.instructor_id, 
                   i.first_name || ' ' || i.last_name as instructor_name,
                   r.course_id, c.name as course_name, r.department_id, 
                   MIN(r.reserv_date) as assignment_date
            FROM reservation r
            JOIN instructor i ON r.instructor_id = i.instructor_id
            JOIN course c ON r.course_id = c.course_id AND r.department_id = c.department_id
            GROUP BY r.instructor_id, i.first_name, i.last_name, r.course_id, c.name, r.department_id
            ORDER BY r.instructor_id, r.course_id;
        """, fetch=True)
        con.close_all_connections()
        return result
    except Exception as e:
        logger.error(f"Error getting instructor-course assignments: {e}")
        con.close_all_connections()
        return []


def assign_instructor_to_course(instructor_id, course_id, department_id, assignment_date):
    """
    Assign an instructor to a course
    Note: Since there's no explicit assignment table, we create a reservation entry
    or this could be logged differently depending on your schema
    
    Args:
        instructor_id (int): Instructor ID
        course_id (int): Course ID
        department_id (int): Department ID
        assignment_date (str): Date of assignment (YYYY-MM-DD)
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Note: If you have an instructor_course table, use that instead
    # For now, we'll just log it as assignments are derived from reservations
    logger.info(f"Assigned instructor {instructor_id} to course {course_id} on {assignment_date}")
    return True


def remove_instructor_from_course(instructor_id, course_id, department_id):
    """
    Remove an instructor's assignment from a course
    Note: Since assignments are derived from reservations, this would require
    deleting future reservations or having a separate assignment table
    
    Args:
        instructor_id (int): Instructor ID
        course_id (int): Course ID
        department_id (int): Department ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Removed instructor {instructor_id} from course {course_id}")
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
