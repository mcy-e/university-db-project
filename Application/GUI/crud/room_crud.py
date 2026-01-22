from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal

from .base_crud import BaseCRUD
from Database import database as db

class RoomCRUD(BaseCRUD):

    
    #* Create Back Signal
    go_back=pyqtSignal()

    def __init__(self):
    
        db_operations = {
            'add': db.add_room,
            'update': db.update_room,
            'delete': db.delete_room,
        }
        header=["Building", "RoomNo", "Capacity"]
        super().__init__(header, db_operations)
        
        self.populate_table(db.get_all_rooms())
        self.back_btn.clicked.connect(self.go_back.emit)

