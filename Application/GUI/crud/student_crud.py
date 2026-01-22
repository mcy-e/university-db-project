from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal


from .base_crud import BaseCRUD

from Database import database as db

class StudentCRUD(BaseCRUD):

    
    #* Create Back Signal
    go_back=pyqtSignal()


    def __init__(self):

        db_operations = {
        'add': db.add_student,
        'update': db.update_student,
        'delete': db.delete_student,
        }

        header=["Student_ID", "Last_Name", "First_Name", "DOB", "Address", "City", "Zip_Code", "Phone", "Fax", "Email", "Group_ID", "Section_ID"]
        
        super().__init__(header,db_operations)
        self.populate_table(db.get_all_students())
        self.back_btn.clicked.connect(self.go_back.emit)

    def _is_id_field(self, header):
        return header == "Student_ID"

