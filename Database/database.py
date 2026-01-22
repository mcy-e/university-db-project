"""
Application.Database.database
Contains all database CRUD operations and queries
Function definitions for GUI integration
"""

import logging

from  Database.connection import DatabaseConnection as con

from  Database.connection import execute_query as eq


logger = logging.getLogger(__name__)

# Credentials are now managed by the main application using con.initialize_pool()

#? STUDENT OPERATIONS

def get_all_students():
    """
    Retrieve all students from the database
    
    Returns:
        list[tuple]: List of student records
        Format: (student_id, last_name, first_name, dob, address, city, 
                 zip_code, phone, fax, email, group_id, section_id)
    """
    try:
        return eq("SELECT student_id, last_name, first_name, dob, address, city, zip_code, phone, fax, email, group_id, section_id FROM student ORDER BY student_id;", fetch=True)
    except Exception as e:
        logger.error(f"Error getting all students: {e}")
        return []

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
    """
    try:
        # We join student, enrollment, and mark. 
        # Since mark doesn't have exam_id, we show the mark for that course.
        return eq("""
            SELECT s.student_id, s.last_name, s.first_name, m.mark_value AS current_mark 
            FROM student s 
            INNER JOIN enrollment e ON s.student_id = e.student_id 
            LEFT JOIN mark m ON s.student_id = m.student_id AND e.course_id = m.course_id AND e.department_id = m.department_id
            WHERE e.course_id = %s 
            ORDER BY s.last_name, s.first_name;
        """, (course_id,), fetch=True)
    except Exception as e:
        logger.error(f"Error getting students with marks: {e}")
        return []
    

def add_student(last_name, first_name, dob, address, city, zip_code, phone, fax, email, group_id, section_id):
    """
    Insert a new student into the database
    """
    try:
        eq("INSERT INTO student (last_name, first_name, dob, address, city, zip_code, phone, fax, email, group_id, section_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", 
           (last_name, first_name, dob, address, city, zip_code, phone, fax, email, group_id, section_id))
        logger.info(f"Added student {first_name} {last_name}")
        return True
    except Exception as e:
        logger.error(f"Error adding student: {e}")
        return False


def update_student(student_id, last_name, first_name, dob, address, city, zip_code, phone, fax, email, group_id, section_id):
    """
    Update an existing student's information
    """
    try:
        eq("UPDATE student SET last_name = %s, first_name = %s, dob = %s, address = %s, city = %s, zip_code = %s, phone = %s, fax = %s, email = %s, group_id = %s, section_id = %s WHERE student_id = %s;",
           (last_name, first_name, dob, address, city, zip_code, phone, fax, email, group_id, section_id, student_id))
        logger.info(f"Updated student {student_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating student: {e}")
        return False


def delete_student(student_id):
    """
    Delete a student from the database
    """
    try:
        eq("DELETE FROM student WHERE student_id = %s;", (student_id,))
        logger.info(f"Deleted student {student_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting student: {e}")
        return False



#? INSTRUCTOR OPERATIONS


def get_all_instructors():
    """
    Retrieve all instructors from the database
    """
    try:
        return eq("SELECT instructor_id, department_id, last_name, first_name, rank, phone, fax, email FROM instructor ORDER BY instructor_id;", fetch=True)
    except Exception as e:
        logger.error(f"Error getting all instructors: {e}")
        return []


def add_instructor(department_id, last_name, first_name, rank, phone, fax, email):
    """
    Insert a new instructor into the database
    """
    try:
        eq("INSERT INTO instructor(department_id,last_name,first_name,rank,phone,fax,email) VALUES (%s,%s,%s,%s,%s,%s,%s);",(department_id, last_name, first_name, rank, phone, fax, email))
        logger.info(f"Added instructor {first_name} {last_name}")
        return True
    except Exception as e:
        logger.error(f"Error adding instructor: {e}")
        return False


def update_instructor(instructor_id, department_id, last_name, first_name, rank, phone, fax, email):
    """
    Update an existing instructor's information
    """
    try:
        eq("UPDATE instructor SET department_id = %s,last_name = %s, first_name = %s,rank = %s, phone = %s,fax = %s,email = %s WHERE instructor_id = %s;",(department_id, last_name, first_name, rank, phone, fax, email,instructor_id))
        logger.info(f"Updated instructor {instructor_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating instructor: {e}")
        return False



def delete_instructor(instructor_id):
    """
    Delete an instructor from the database
    """
    try:
        eq("DELETE FROM instructor WHERE instructor_id = %s;", (instructor_id,))
        logger.info(f"Deleted instructor {instructor_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting instructor: {e}")
        return False


#? COURSE OPERATIONS


def get_all_courses():
    """
    Retrieve all courses from the database
    """
    try:
        return eq("SELECT course_id, department_id, name, description FROM course ORDER BY course_id, department_id;", fetch=True)
    except Exception as e:
        logger.error(f"Error getting all courses: {e}")
        return []


def add_course(course_id, department_id, name, description):
    """
    Insert a new course into the database
    """
    try:
        eq("INSERT INTO course (course_id, department_id, name, description) VALUES (%s, %s, %s, %s);",
           (course_id, department_id, name, description))
        logger.info(f"Added course {name}")
        return True
    except Exception as e:
        logger.error(f"Error adding course: {e}")
        return False


def update_course(course_id, department_id, name, description):
    """
    Update an existing course's information
    """
    try:
        eq("UPDATE course SET name = %s, description = %s WHERE course_id = %s AND department_id = %s;",
           (name, description, course_id, department_id))
        logger.info(f"Updated course {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating course: {e}")
        return False


def delete_course(course_id, department_id):
    """
    Delete a course from the database
    """
    try:
        eq("DELETE FROM course WHERE course_id = %s AND department_id = %s;", (course_id, department_id))
        logger.info(f"Deleted course {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting course: {e}")
        return False



#? DEPARTMENT OPERATIONS


def get_all_departments():
    """
    Retrieve all departments from the database
    """
    try:
        return eq("SELECT department_id, name FROM department ORDER BY department_id;", fetch=True)
    except Exception as e:
        logger.error(f"Error getting all departments: {e}")
        return []


def add_department(department_id, name):
    """
    Insert a new department into the database
    """
    try:
        eq("INSERT INTO department (department_id, name) VALUES (%s, %s);", (department_id, name))
        logger.info(f"Added department {name}")
        return True
    except Exception as e:
        logger.error(f"Error adding department: {e}")
        return False


def update_department(department_id, name):
    """
    Update an existing department's information
    """
    try:
        eq("UPDATE department SET name = %s WHERE department_id = %s;", (name, department_id))
        logger.info(f"Updated department {department_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating department: {e}")
        return False


def delete_department(department_id):
    """
    Delete a department from the database
    """
    try:
        eq("DELETE FROM department WHERE department_id = %s;", (department_id,))
        logger.info(f"Deleted department {department_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting department: {e}")
        return False



#? ROOM OPERATIONS


def get_all_rooms():
    """
    Retrieve all rooms from the database
    """
    try:
        return eq("SELECT building, roomno, capacity FROM room ORDER BY building, roomno;", fetch=True)
    except Exception as e:
        logger.error(f"Error getting all rooms: {e}")
        return []


def add_room(building, roomno, capacity):
    """
    Insert a new room into the database
    """
    try:
        eq("INSERT INTO room (building, roomno, capacity) VALUES (%s, %s, %s);", (building, roomno, capacity))
        logger.info(f"Added room {building} {roomno}")
        return True
    except Exception as e:
        logger.error(f"Error adding room: {e}")
        return False


def update_room(building, roomno, capacity):
    """
    Update an existing room's information
    """
    try:
        eq("UPDATE room SET capacity = %s WHERE building = %s AND roomno = %s;", (capacity, building, roomno))
        logger.info(f"Updated room {building} {roomno}")
        return True
    except Exception as e:
        logger.error(f"Error updating room: {e}")
        return False


def delete_room(building, roomno):
    """
    Delete a room from the database
    """
    try:
        eq("DELETE FROM room WHERE building = %s AND roomno = %s;", (building, roomno))
        logger.info(f"Deleted room {building} {roomno}")
        return True
    except Exception as e:
        logger.error(f"Error deleting room: {e}")
        return False



#? SECTION OPERATIONS


def get_all_sections():
    """
    Retrieve all sections from the database
    """
    try:
        return eq("SELECT DISTINCT section_id, 'Section ' || section_id as section_name FROM student WHERE section_id IS NOT NULL ORDER BY section_id;", fetch=True)
    except Exception as e:
        logger.error(f"Error getting all sections: {e}")
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
    """
    try:
        return eq("SELECT DISTINCT group_id, 'Group ' || group_id::text as group_name FROM student WHERE group_id IS NOT NULL ORDER BY group_id;", fetch=True)
    except Exception as e:
        logger.error(f"Error getting all groups: {e}")
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
    """
    try:
        return eq("SELECT reservation_id, building, roomno, course_id, department_id, instructor_id, reserv_date, start_time, end_time, hours_number FROM reservation ORDER BY reserv_date DESC, start_time;", fetch=True)
    except Exception as e:
        logger.error(f"Error getting all reservations: {e}")
        return []


def get_reservations_by_filter(room=None, date=None):
    """
    Retrieve reservations filtered by room and/or date
    """
    try:
        query = "SELECT reservation_id, building, roomno, course_id, department_id, instructor_id, reserv_date, start_time, end_time, hours_number FROM reservation WHERE 1=1"
        params = []
        
        if room:
            parts = room.split()
            if len(parts) >= 2:
                building, roomno = parts[0], parts[1]
                query += " AND building = %s AND roomno = %s"
                params.extend([building, roomno])
        
        if date:
            query += " AND reserv_date = %s"
            params.append(date)
        
        query += " ORDER BY reserv_date DESC, start_time;"
        return eq(query, tuple(params) if params else None, fetch=True)
    except Exception as e:
        logger.error(f"Error getting filtered reservations: {e}")
        return []


def get_reservation_details(reservation_id):
    """
    Get detailed information about a specific reservation including names
    """
    try:
        result = eq("""
            SELECT r.reservation_id, r.building, r.roomno, r.reserv_date, r.start_time, r.end_time, r.hours_number,
                   c.name as course_name, i.first_name || ' ' || i.last_name as instructor_name
            FROM reservation r
            JOIN course c ON r.course_id = c.course_id AND r.department_id = c.department_id
            JOIN instructor i ON r.instructor_id = i.instructor_id
            WHERE r.reservation_id = %s;
        """, (reservation_id,), fetch=True)
        
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
        return {}


def add_reservation(building, roomno, course_id, department_id, instructor_id, 
                   reserv_date, start_time, end_time, hours_number):
    """
    Insert a new reservation into the database
    """
    connection = None
    cursor = None
    try:
        connection = con.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO reservation (building, roomno, course_id, department_id, instructor_id, reserv_date, start_time, end_time, hours_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING reservation_id;",
            (building, roomno, course_id, department_id, instructor_id, reserv_date, start_time, end_time, hours_number)
        )
        new_id = cursor.fetchone()[0]
        connection.commit()
        logger.info(f"Added reservation - Building: {building}, Room: {roomno}, Course: {course_id}, ID: {new_id}")
        return (True, new_id)
    except Exception as e:
        logger.error(f"Error adding reservation: {e}")
        if connection:
            connection.rollback()
        return (False, None)
    finally:
        if cursor:
            cursor.close()
        if connection:
            con.return_connection(connection)


def update_reservation(reservation_id, building, roomno, course_id, department_id, 
                      instructor_id, reserv_date, start_time, end_time, hours_number):
    """
    Update an existing reservation's information
    """
    try:
        eq("UPDATE reservation SET building = %s, roomno = %s, course_id = %s, department_id = %s, instructor_id = %s, reserv_date = %s, start_time = %s, end_time = %s, hours_number = %s WHERE reservation_id = %s;",
           (building, roomno, course_id, department_id, instructor_id, reserv_date, start_time, end_time, hours_number, reservation_id))
        logger.info(f"Updated reservation {reservation_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating reservation: {e}")
        return False


def delete_reservation(reservation_id):
    """
    Delete a reservation from the database
    """
    try:
        eq("DELETE FROM reservation WHERE reservation_id = %s;", (reservation_id,))
        logger.info(f"Deleted reservation {reservation_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting reservation: {e}")
        return False


def check_room_availability(building, roomno, reserv_date, start_time, end_time):
    """
    Check if a room is available for reservation
    """
    try:
        result = eq("""
            SELECT COUNT(*) FROM reservation 
            WHERE building = %s AND roomno = %s AND reserv_date = %s 
            AND NOT (end_time <= %s OR start_time >= %s);
        """, (building, roomno, reserv_date, start_time, end_time), fetch=True)
        count = result[0][0] if result else 0
        return count == 0
    except Exception as e:
        logger.error(f"Error checking room availability: {e}")
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
    """
    try:
        return eq("SELECT student_id, course_id, department_id, enrollment_date FROM enrollment ORDER BY enrollment_date DESC, student_id;", fetch=True)
    except Exception as e:
        logger.error(f"Error getting all enrollments: {e}")
        return []


def add_enrollment(student_id, course_id, department_id, enrollment_date):
    """
    Insert a new enrollment into the database
    """
    try:
        eq("INSERT INTO enrollment (student_id, course_id, department_id, enrollment_date) VALUES (%s, %s, %s, %s);",
           (student_id, course_id, department_id, enrollment_date))
        logger.info(f"Added enrollment - Student: {student_id}, Course: {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error adding enrollment: {e}")
        return False


def update_enrollment(student_id, course_id, department_id, enrollment_date):
    """
    Update an existing enrollment's information
    """
    try:
        eq("UPDATE enrollment SET enrollment_date = %s WHERE student_id = %s AND course_id = %s AND department_id = %s;",
           (enrollment_date, student_id, course_id, department_id))
        logger.info(f"Updated enrollment - Student: {student_id}, Course: {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating enrollment: {e}")
        return False


def delete_enrollment(student_id, course_id, department_id):
    """
    Delete an enrollment from the database
    """
    try:
        eq("DELETE FROM enrollment WHERE student_id = %s AND course_id = %s AND department_id = %s;",
           (student_id, course_id, department_id))
        logger.info(f"Deleted enrollment - Student: {student_id}, Course: {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting enrollment: {e}")
        return False



#? MARK OPERATIONS


def get_all_marks():
    """
    Retrieve all marks from the database
    """
    try:
        return eq("SELECT mark_id, student_id, course_id, department_id, mark_value, mark_date FROM mark ORDER BY mark_date DESC, student_id;", fetch=True)
    except Exception as e:
        logger.error(f"Error getting all marks: {e}")
        return []


def add_mark(student_id, course_id, department_id, mark_value, mark_date):
    """
    Insert a new mark into the database
    """
    try:
        eq("INSERT INTO mark (student_id, course_id, department_id, mark_value, mark_date) VALUES (%s, %s, %s, %s, %s);",
           (student_id, course_id, department_id, mark_value, mark_date))
        logger.info(f"Added mark - Student: {student_id}, Course: {course_id}, Value: {mark_value}")
        return True
    except Exception as e:
        logger.error(f"Error adding mark: {e}")
        return False


def update_mark(mark_id, student_id, course_id, department_id, mark_value, mark_date):
    """
    Update an existing mark's information
    """
    try:
        eq("UPDATE mark SET student_id = %s, course_id = %s, department_id = %s, mark_value = %s, mark_date = %s WHERE mark_id = %s;",
           (student_id, course_id, department_id, mark_value, mark_date, mark_id))
        logger.info(f"Updated mark {mark_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating mark: {e}")
        return False


def delete_mark(mark_id):
    """
    Delete a mark from the database
    """
    try:
        eq("DELETE FROM mark WHERE mark_id = %s;", (mark_id,))
        logger.info(f"Deleted mark {mark_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting mark: {e}")
        return False


def save_bulk_marks(marks_records):
    """
    Save multiple marks at once
    marks_records should contain: student_id, course_id, department_id (optional), mark_value, mark_date (optional)
    If department_id is missing, it will be fetched from the course
    If mark_date is missing, current date will be used
    """
    connection = None
    cursor = None
    try:
        connection = con.get_connection()
        cursor = connection.cursor()
        
        from datetime import date
        
        for record in marks_records:
            student_id = record.get('student_id')
            course_id = record.get('course_id')
            department_id = record.get('department_id')
            mark_value = record.get('mark_value')
            mark_date = record.get('mark_date') or record.get('date') or date.today()
            
            # If department_id is not provided, get it from the course
            if not department_id:
                cursor.execute("SELECT department_id FROM course WHERE course_id = %s LIMIT 1;", (course_id,))
                result = cursor.fetchone()
                if result:
                    department_id = result[0]
                else:
                    logger.error(f"Course {course_id} not found, skipping mark for student {student_id}")
                    continue
            
            cursor.execute(
                "INSERT INTO mark (student_id, course_id, department_id, mark_value, mark_date) VALUES (%s, %s, %s, %s, %s);",
                (student_id, course_id, department_id, mark_value, mark_date)
            )
        
        connection.commit()
        logger.info(f"Saved {len(marks_records)} marks in bulk")
        return True
    except Exception as e:
        logger.error(f"Error saving bulk marks: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            con.return_connection(connection)



#? ACTIVITY OPERATIONS


def get_all_activities():
    """
    Retrieve all activities from the database with course names
    Returns: list[tuple]: (activity_id, activity_type, course_name)
    """
    try:
        return eq("""
            SELECT a.activity_id, a.activity_type, c.name as course_name 
            FROM activity a
            JOIN course c ON a.course_id = c.course_id AND a.department_id = c.department_id
            ORDER BY a.activity_id;
        """, fetch=True)
    except Exception as e:
        logger.error(f"Error getting all activities: {e}")
        return []


def add_activity(activity_type, reservation_id, course_id, department_id):
    """
    Insert a new activity into the database
    """
    try:
        eq("INSERT INTO activity (activity_type, reservation_id, course_id, department_id) VALUES (%s, %s, %s, %s);",
           (activity_type, reservation_id, course_id, department_id))
        logger.info(f"Added activity {activity_type} for course {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error adding activity: {e}")
        return False


def update_activity(activity_id, activity_type, reservation_id, course_id, department_id):
    """
    Update an existing activity's information
    """
    try:
        eq("UPDATE activity SET activity_type = %s, reservation_id = %s, course_id = %s, department_id = %s WHERE activity_id = %s;",
           (activity_type, reservation_id, course_id, department_id, activity_id))
        logger.info(f"Updated activity {activity_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating activity: {e}")
        return False


def delete_activity(activity_id):
    """
    Delete an activity from the database
    """
    try:
        eq("DELETE FROM activity WHERE activity_id = %s;", (activity_id,))
        logger.info(f"Deleted activity {activity_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting activity: {e}")
        return False



#? EXAM OPERATIONS


def get_all_exams():
    """
    Retrieve all exams from the database
    """
    try:
        return eq("SELECT exam_id, duration, exam_type, course_id, department_id FROM exam ORDER BY exam_id;", fetch=True)
    except Exception as e:
        logger.error(f"Error getting all exams: {e}")
        return []


def get_exams_by_course(course_id):
    """
    Retrieve exams for a specific course
    """
    try:
        return eq("SELECT exam_id, exam_type, duration, department_id FROM exam WHERE course_id = %s ORDER BY exam_id;", (course_id,), fetch=True)
    except Exception as e:
        logger.error(f"Error getting exams by course: {e}")
        return []


def add_exam(duration, exam_type, course_id, department_id):
    """
    Insert a new exam into the database
    """
    try:
        eq("INSERT INTO exam (duration, exam_type, course_id, department_id) VALUES (%s, %s, %s, %s);",
           (duration, exam_type, course_id, department_id))
        logger.info(f"Added exam {exam_type} for course {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error adding exam: {e}")
        return False


def update_exam(exam_id, duration, exam_type, course_id, department_id):
    """
    Update an existing exam's information
    """
    try:
        eq("UPDATE exam SET duration = %s, exam_type = %s, course_id = %s, department_id = %s WHERE exam_id = %s;",
           (duration, exam_type, course_id, department_id, exam_id))
        logger.info(f"Updated exam {exam_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating exam: {e}")
        return False


def delete_exam(exam_id):
    """
    Delete an exam from the database
    """
    try:
        eq("DELETE FROM exam WHERE exam_id = %s;", (exam_id,))
        logger.info(f"Deleted exam {exam_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting exam: {e}")
        return False


#? ATTENDANCE OPERATIONS


def get_all_attendances():
    """
    Retrieve all attendance records from the database
    """
    try:
        return eq("SELECT student_id, activity_id, attendance_date, statu FROM attendance_to_activities ORDER BY attendance_date DESC, student_id;", fetch=True)
    except Exception as e:
        logger.error(f"Error getting all attendances: {e}")
        return []


def add_attendance(student_id, activity_id, attendance_date, status='present'):
    """
    Insert a new attendance record into the database
    """
    try:
        eq("INSERT INTO attendance_to_activities (student_id, activity_id, attendance_date, statu) VALUES (%s, %s, %s, %s);",
           (student_id, activity_id, attendance_date, status))
        logger.info(f"Added attendance - Student: {student_id}, Activity: {activity_id}")
        return True
    except Exception as e:
        logger.error(f"Error adding attendance: {e}")
        return False


def update_attendance(student_id, activity_id, attendance_date, status):
    """
    Update an existing attendance record
    """
    try:
        eq("UPDATE attendance_to_activities SET statu = %s WHERE student_id = %s AND activity_id = %s AND attendance_date = %s;",
           (status, student_id, activity_id, attendance_date))
        logger.info(f"Updated attendance - Student: {student_id}, Activity: {activity_id}")
        return True
    except Exception as e:
        logger.error(f"Error updating attendance: {e}")
        return False


def delete_attendance(student_id, activity_id, attendance_date):
    """
    Delete an attendance record from the database
    """
    try:
        eq("DELETE FROM attendance_to_activities WHERE student_id = %s AND activity_id = %s AND attendance_date = %s;",
           (student_id, activity_id, attendance_date))
        logger.info(f"Deleted attendance - Student: {student_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting attendance: {e}")
        return False


def save_bulk_attendance(attendance_records):
    """
    Save multiple attendance records at once
    attendance_records should contain: student_id, activity_id, attendance_date (or 'date'), status (or 'statu')
    """
    connection = None
    cursor = None
    try:
        connection = con.get_connection()
        cursor = connection.cursor()
        
        for record in attendance_records:
            student_id = record.get('student_id')
            activity_id = record.get('activity_id')
            # Handle both 'attendance_date' and 'date' keys
            attendance_date = record.get('attendance_date') or record.get('date')
            # Handle both 'status' and 'statu' keys (statu is the actual column name)
            status = record.get('status') or record.get('statu')
            
            if not all([student_id, activity_id, attendance_date, status]):
                logger.warning(f"Incomplete attendance record: {record}, skipping")
                continue
            
            cursor.execute(
                "INSERT INTO attendance_to_activities (student_id, activity_id, attendance_date, statu) VALUES (%s, %s, %s, %s);",
                (student_id, activity_id, attendance_date, status)
            )
        
        connection.commit()
        logger.info(f"Saved {len(attendance_records)} attendance records in bulk")
        return True
    except Exception as e:
        logger.error(f"Error saving bulk attendance: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            con.return_connection(connection)



#? INSTRUCTOR-COURSE ASSIGNMENT OPERATIONS
# Note: The instructor_course_assignment table is a junction table for many-to-many
# relationship between instructors and courses. If this table doesn't exist, create it with:
# CREATE TABLE instructor_course_assignment (
#     instructor_id INTEGER NOT NULL,
#     course_id INTEGER NOT NULL,
#     department_id INTEGER NOT NULL,
#     PRIMARY KEY (instructor_id, course_id, department_id),
#     FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id),
#     FOREIGN KEY (course_id, department_id) REFERENCES course(course_id, department_id)
# );


def get_all_instructor_course_assignments():
    """
    Retrieve all instructor-course assignments from the database with names
    Returns: list[tuple]: (instructor_id, instructor_name, course_id, course_name, department_id, assignment_date)
    Note: assignment_date will be NULL if not stored in the table
    """
    try:
        return eq("""
            SELECT 
                ica.instructor_id,
                i.first_name || ' ' || i.last_name as instructor_name,
                ica.course_id,
                c.name as course_name,
                ica.department_id,
                NULL as assignment_date
            FROM instructor_course_assignment ica
            JOIN instructor i ON ica.instructor_id = i.instructor_id
            JOIN course c ON ica.course_id = c.course_id AND ica.department_id = c.department_id
            ORDER BY ica.instructor_id, ica.course_id;
        """, fetch=True)
    except Exception as e:
        logger.error(f"Error getting instructor-course assignments: {e}")
        return []


def assign_instructor_to_course(instructor_id, course_id, department_id, assignment_date=None):
    """
    Assign an instructor to a course
    Args:
        instructor_id: Instructor ID
        course_id: Course ID
        department_id: Department ID
        assignment_date: Optional assignment date (for compatibility with GUI)
    """
    try:
        eq("INSERT INTO instructor_course_assignment (instructor_id, course_id, department_id) VALUES (%s, %s, %s);",
           (instructor_id, course_id, department_id))
        logger.info(f"Assigned instructor {instructor_id} to course {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error assigning instructor: {e}")
        return False


def remove_instructor_from_course(instructor_id, course_id, department_id):
    """
    Remove an instructor's assignment from a course
    """
    try:
        eq("DELETE FROM instructor_course_assignment WHERE instructor_id = %s AND course_id = %s AND department_id = %s;",
           (instructor_id, course_id, department_id))
        logger.info(f"Removed instructor {instructor_id} from course {course_id}")
        return True
    except Exception as e:
        logger.error(f"Error removing instructor assignment: {e}")
        return False


def get_instructor_list_with_ids():
    """
    Retrieve list of instructors for selection
    """
    try:
        return eq("SELECT instructor_id, first_name || ' ' || last_name, department_id FROM instructor ORDER BY instructor_id;", fetch=True)
    except Exception as e:
        logger.error(f"Error getting instructor list: {e}")
        return []


def get_course_list_with_ids():
    """
    Retrieve list of courses for selection
    """
    try:
        return eq("SELECT course_id, name, department_id FROM course ORDER BY course_id, department_id;", fetch=True)
    except Exception as e:
        logger.error(f"Error getting course list: {e}")
        return []



#? QUERY OPERATIONS


def get_available_queries():
    """
    Retrieve list of available pre-defined functions from the database logic
    """
    return [
        "Student Averages",
        "Students by Group",
        "Students by Section",
        "Instructor Timetable",
        "Disqualifying Marks by Course",
        "Average Marks by Course",
        "Failing Students Report"
    ]


def execute_query(query_name, params=None):
    """
    Execute a specific pre-defined query or function
    Args:
        query_name: Name of the query to execute
        params: Optional parameter for queries that need input (group_id, section_id, instructor_id)
    """
    try:
        if query_name == "Student Averages":
            headers = ["Student ID", "Average Mark"]
            data = eq("SELECT * FROM get_average_of_students();", fetch=True)
        elif query_name == "Students by Group":
            headers = ["Student ID", "Last Name", "First Name"]
            if params is None:
                logger.warning("Students by Group query requires a group_id parameter")
                return ["Error"], [("This query requires a group_id parameter",)]
            data = eq("SELECT * FROM get_students_by_group(%s);", (params,), fetch=True)
        elif query_name == "Students by Section":
            headers = ["Student ID", "Last Name", "First Name"]
            if params is None:
                logger.warning("Students by Section query requires a section_id parameter")
                return ["Error"], [("This query requires a section_id parameter",)]
            data = eq("SELECT * FROM get_students_by_section(%s);", (params,), fetch=True)
        elif query_name == "Instructor Timetable":
            headers = ["Date", "Start Time", "End Time"]
            if params is None:
                logger.warning("Instructor Timetable query requires an instructor_id parameter")
                return ["Error"], [("This query requires an instructor_id parameter",)]
            data = eq("SELECT * FROM get_instructor_timetable(%s);", (params,), fetch=True)
        elif query_name == "Disqualifying Marks by Course":
            headers = ["DQ Mark", "Course ID", "Dept ID"]
            data = eq("SELECT * FROM disqualifying_mark_by_course();", fetch=True)
        elif query_name == "Average Marks by Course":
            headers = ["Avg Mark", "Course ID", "Dept ID"]
            data = eq("SELECT * FROM avg_mark_by_course();", fetch=True)
        elif query_name == "Failing Students Report":
            headers = ["Student ID", "Course ID", "Dept ID", "Mark", "DQ Mark"]
            data = eq("SELECT * FROM students_who_received_a_failing_grade_in_a_module();", fetch=True)
        else:
            headers = ["Result"]
            data = [("Unknown query",)]
        
        # Handle empty results
        if not data:
            data = [("No results found",)]
        
        return headers, data
    except Exception as e:
        logger.error(f"Error executing named query {query_name}: {e}")
        return ["Error"], [(str(e),)]



#? AUDIT OPERATIONS


def get_audit_logs(from_date, to_date, table_name):
    """
    Retrieve audit logs filtered by date range and table
    """
    try:
        if "mark" in table_name.lower():
            return eq("SELECT logid, operationtype, operationtime, description FROM mark_audit_log WHERE operationtime BETWEEN %s AND %s ORDER BY operationtime DESC;", (from_date, to_date), fetch=True)
        else:
            return eq("SELECT logid, operationtype, operationtime, description FROM attendance_audit_log WHERE operationtime BETWEEN %s AND %s ORDER BY operationtime DESC;", (from_date, to_date), fetch=True)
    except Exception as e:
        logger.error(f"Error getting audit logs: {e}")
        return []


def get_table_names():
    """
    Retrieve list of database table names for audit
    """
    return ["Marks", "Attendance"]



#? RESULTS OPERATIONS


def get_student_results(semester, course_id):
    """
    Retrieve results for a specific course
    """
    try:
        return eq("""
            SELECT s.student_id, s.first_name || ' ' || s.last_name, m.mark_value, 
                   CASE WHEN m.mark_value >= 10 THEN 'Pass' ELSE 'Fail' END as status
            FROM student s
            JOIN mark m ON s.student_id = m.student_id
            WHERE m.course_id = %s
            ORDER BY s.last_name, s.first_name;
        """, (course_id,), fetch=True)
    except Exception as e:
        logger.error(f"Error getting student results: {e}")
        return []


def get_semesters_list():
    """
    Retrieve list of academic years/semesters from enrollment data
    """
    try:
        results = eq("SELECT DISTINCT enrollment_date::text FROM enrollment ORDER BY enrollment_date DESC;", fetch=True)
        return [row[0] for row in results] if results else ["No Data"]
    except Exception as e:
        logger.error(f"Error getting semesters list: {e}")
        return ["Error"]



#? PERFORMANCE OPERATIONS


def get_performance_stats():
    """
    Retrieve real-time performance statistics from the database
    """
    try:
        total_students_result = eq("SELECT COUNT(*) FROM student;", fetch=True)
        total_students = total_students_result[0][0] if total_students_result and len(total_students_result) > 0 else 0
        
        avg_gpa_result = eq("SELECT ROUND(AVG(mark_value), 2) FROM mark;", fetch=True)
        avg_gpa = avg_gpa_result[0][0] if avg_gpa_result and len(avg_gpa_result) > 0 and avg_gpa_result[0][0] is not None else None
        
        attendance_rate_result = eq("SELECT ROUND((COUNT(*) FILTER (WHERE statu = 'present')::numeric / NULLIF(COUNT(*), 0)) * 100, 1) FROM attendance_to_activities;", fetch=True)
        attendance_rate = attendance_rate_result[0][0] if attendance_rate_result and len(attendance_rate_result) > 0 and attendance_rate_result[0][0] is not None else None
        
        pass_rate_result = eq("SELECT ROUND((COUNT(*) FILTER (WHERE mark_value >= 10)::numeric / NULLIF(COUNT(*), 0)) * 100, 1) FROM mark;", fetch=True)
        pass_rate = pass_rate_result[0][0] if pass_rate_result and len(pass_rate_result) > 0 and pass_rate_result[0][0] is not None else None
        
        return {
            "Total Students": total_students or 0,
            "Average GPA": str(avg_gpa) if avg_gpa is not None else "N/A",
            "Attendance Rate": f"{attendance_rate}%" if attendance_rate is not None else "N/A",
            "Pass Rate": f"{pass_rate}%" if pass_rate is not None else "N/A",
        }
    except Exception as e:
        logger.error(f"Error getting performance stats: {e}")
        return {"Error": "Failed to load stats"}
