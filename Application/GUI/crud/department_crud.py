from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal

from .base_crud import BaseCRUD

from Database import database  as db

DATA=db.get_all_departments()

class DepartmentCRUD(BaseCRUD):

    
    #* Create Back Signal
    go_back=pyqtSignal()


    def __init__(self):
        
        db_operations = {
        'add': db.add_department,
        'update': db.update_department,
        'delete': db.delete_department,
        }   
        header=["Department_ID", "Name"]
        super().__init__(header,db_operations)
        
        self.populate_table(DATA)
        self.back_btn.clicked.connect(self.go_back.emit)

