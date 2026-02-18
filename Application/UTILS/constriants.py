"""
Application.Utils.constraints
Data validation rules for all database fields
"""

import re
from datetime import datetime

def check_constraint(field_name, value):
    """
    Validate a field value against its constraints.
    
    Args:
        field_name (str): Name of the field
        value (str): Value to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    
    #* Strip whitespace
    value = str(value).strip()
    
    #* Empty check for required fields
    required_fields = [
        "Last_Name", "First_Name", "DOB", "City",
        "Name", "Department_ID", "Course_ID", "Building",
        "RoomNo", "Capacity", "Student_ID", "Activity_ID"
    ]
    
    if field_name in required_fields and not value:
        return False, f"{field_name} cannot be empty"
    
    
    #* NUMERIC VALIDATIONS
    
    if field_name in ["Group_ID", "Department_ID", "Course_ID", 
                      "Instructor_ID", "Capacity", "Hours_Number", "Duration",
                      "Mark_ID", "Exam_ID", "Activity_ID", "Reservation_ID"]:
        if value and not value.isdigit():
            return False, f"{field_name} must be a number"
        if field_name == "Capacity" and value:
            if int(value) <= 0:
                return False, "Capacity must be positive"
    
    
    #* MARK VALUE VALIDATION
    
    if field_name == "Mark_Value":
        try:
            mark = float(value)
            if mark < 0 or mark > 20:
                return False, "Mark must be between 0 and 20"
        except ValueError:
            return False, "Mark must be a valid number"
    
    
    #* EMAIL VALIDATION
    
    if field_name == "Email" and value:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            return False, "Invalid email format"
    
    
    #* PHONE VALIDATION
    
    if field_name in ["Phone", "Fax"] and value:
        #* DZ phone format: 10 digits starting with 0
        phone_pattern = r'^0\d{9}$'
        if not re.match(phone_pattern, value):
            return False, f"{field_name} must be 10 digits starting with 0"
    
    
    #* DATE VALIDATIONS
    
    if field_name in ["DOB", "Enrollment_Date", "Mark_Date", "Attendance_Date", "Reserv_Date"]:
        if value:
            try:
                date_obj = datetime.strptime(value, "%Y-%m-%d")
                
                # DOB should be in the past
                if field_name == "DOB" and date_obj > datetime.now():
                    return False, "Date of birth cannot be in the future"
                    
            except ValueError:
                return False, f"{field_name} must be in format YYYY-MM-DD"
    
    
    #* TIME VALIDATIONS
    
    if field_name in ["Start_Time", "End_Time"]:
        if value:
            try:
                datetime.strptime(value, "%H:%M:%S")
            except ValueError:
                return False, f"{field_name} must be in format HH:MM:SS"
    
    
    #* ZIP CODE VALIDATION
    
    if field_name == "Zip_Code" and value:
        if not value.isdigit() or len(value) != 5:
            return False, "Zip code must be 6 digits"
    
    
    #* BUILDING VALIDATION*
    
    if field_name == "Building" and value:
        if len(value) != 1 or not value.isalpha():
            return False, "Building must be a single letter"
    
    
    #* SECTION VALIDATION*
    
    if field_name == "Section_ID" and value:
        if len(value) != 1 or not value.isalpha():
            return False, "Section must be a single letter"
    
    
    #* ENUM VALIDATIONS*
    
    if field_name == "Rank" and value:
        valid_ranks = ['Substitute', 'MCB', 'MCA', 'PROF']
        if value not in valid_ranks:
            return False, f"Rank must be one of: {', '.join(valid_ranks)}"
    
    if field_name == "Activity_Type" and value:
        valid_types = ['lecture', 'tutorial', 'practical']
        if value not in valid_types:
            return False, f"Activity type must be one of: {', '.join(valid_types)}"
    
    if field_name == "Status" and value:
        valid_statuses = ['present', 'absent']
        if value not in valid_statuses:
            return False, f"Status must be: present or absent"
    
    if field_name == "Exam_Type" and value:
        valid_types = ['Midterm', 'Final', 'Quiz', 'Project']
        if value not in valid_types:
            return False, f"Exam type must be one of: {', '.join(valid_types)}"
    
    
    #* All checks passed
    return True, ""


def validate_all_fields(field_dict):
    """
    Validate multiple fields at once.
    
    Args:
        field_dict (dict): Dictionary of {field_name: value}
        
    Returns:
        tuple: (is_valid: bool, list of error_messages: list)
    """
    errors = []
    
    for field_name, value in field_dict.items():
        is_valid, error_msg = check_constraint(field_name, value)
        if not is_valid:
            errors.append(error_msg)
    
    return len(errors) == 0, errors