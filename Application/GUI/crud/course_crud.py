from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal

from .base_crud import BaseCRUD

from Database import database as db 

DATA=db.get_all_courses()

class CourseCRUD(BaseCRUD):

    
    #* Create Back Signal
    go_back=pyqtSignal()


    def __init__(self):

        db_operations = {
        'add': db.add_course,
        'update': db.update_course,
        'delete': db.delete_course,
        }
        header=["Course_ID", "Department_ID", "Name", "Description"]
        super().__init__(header,db_operations)
    
        self.populate_table(DATA)
        self.back_btn.clicked.connect(self.go_back.emit)

    def _is_id_field(self, header):
        return header == "Course_ID"
