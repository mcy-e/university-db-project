from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal

from .base_crud import BaseCRUD

from Database import database  as db 

class ExamCRUD(BaseCRUD):

    
    #* Create Back Signal
    go_back=pyqtSignal()

    def __init__(self):
        db_operations = {
            'add': db.add_exam,
            'update': db.update_exam,
            'delete': db.delete_exam,
        }
        header=["Exam_ID", "Duration", "Exam_Type", "Course_ID", "Department_ID"]
        super().__init__(header, db_operations)

        self.populate_table(db.get_all_exams())
        self.back_btn.clicked.connect(self.go_back.emit)

