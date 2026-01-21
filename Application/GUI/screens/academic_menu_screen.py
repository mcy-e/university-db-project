
#& Imports


from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QHeaderView, QLabel, QLineEdit,
    QGridLayout, QTableWidgetItem
)

import logging

from GUI.styling import styling_loader as sl


logger = logging.getLogger(__name__)


#* Path to ui file for the academic menu
PATH_TO_UI = "Application/GUI/UI/academic_menu.ui"



class AcademicMenu(QWidget):
    
    #* Create Signals
    navigate_to_assign_instructor=pyqtSignal()
    navigate_to_manage_reservation=pyqtSignal()
    go_back=pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi(PATH_TO_UI, self)
 
        self.back_btn.clicked.connect(self.go_back.emit)
 
        self.IC_Assignments.clicked.connect(self.navigate_to_assign_instructor.emit)
 
        self.reservation_managment.clicked.connect(self.navigate_to_manage_reservation.emit)

        #* Set the button styles
        sl.apply_button_styles(self,sl.ACADEMIC_MENU_STYLES)