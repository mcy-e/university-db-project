from .activity_crud import ActivityCRUD
from .attendance_crud import AttendanceCRUD
from .course_crud import CourseCRUD
from .department_crud import DepartmentCRUD
from .enrollment_crud import EnrollmentCRUD
from .exam_crud import ExamCRUD
from .mark_crud import MarkCRUD
from .reservation_crud import ReservationCRUD
from .instructor_crud import InstructorCRUD
from .room_crud import RoomCRUD
from .student_crud import StudentCRUD

__all__ = [
    "ActivityCRUD",
    "AttendanceCRUD",
    "CourseCRUD",
    "DepartmentCRUD",
    "EnrollmentCRUD",
    "ExamCRUD",
    "MarkCRUD",
    "ReservationCRUD",
    "InstructorCRUD",
    "RoomCRUD",
    "StudentCRUD",
]