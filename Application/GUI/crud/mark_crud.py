from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal

from .base_crud import BaseCRUD

from Database import database as db 

DATA=db.get_all_marks()

class MarkCRUD(BaseCRUD):

    
    #* Create Back Signal
    go_back=pyqtSignal()

    def __init__(self):
        
        db_operations = {
            'add': db.add_mark,
            'update': db.update_mark,
            'delete': db.delete_mark,
        }
        header=["Mark_ID", "Student_ID", "Course_ID", "Department_ID", "Mark_Value", "Mark_Date"]
        super().__init__(header, db_operations)
        
        self.populate_table(DATA)
        self.back_btn.clicked.connect(self.go_back.emit)
