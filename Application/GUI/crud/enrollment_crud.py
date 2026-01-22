from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal

from .base_crud import BaseCRUD

from Database import database as db 

class EnrollmentCRUD(BaseCRUD):

    
    #* Create Back Signal
    go_back=pyqtSignal()

    def __init__(self):
    
        db_operations = {
            'add': db.add_enrollment,
            'update': db.update_enrollment,
            'delete': db.delete_enrollment,
        }
        header=["Student_ID", "Course_ID", "Department_ID", "Enrollment_Date"]
        super().__init__(header, db_operations)
    
        
        self.populate_table(db.get_all_enrollments())
        self.back_btn.clicked.connect(self.go_back.emit)

