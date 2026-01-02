from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal

from .base_crud import BaseCRUD
from Database import database as db
DATA=db.get_all_reservations()

class ReservationCRUD(BaseCRUD):

    
    #* Create Back Signal
    go_back=pyqtSignal()

    def __init__(self):
        
        db_operations = {

            'add': db.add_reservation,
            'update': db.update_reservation,
            'delete': db.delete_reservation,
        }
        header=["Reservation_ID", "Building", "RoomNo", "Course_ID", "Department_ID", "Instructor_ID", "Reserv_Date", "Start_Time", "End_Time", "Hours_Number"]
        super().__init__(header, db_operations)

        self.populate_table(DATA)
        self.back_btn.clicked.connect(self.go_back.emit)

