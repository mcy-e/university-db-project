
#& Imports


from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QHeaderView, QLabel, QLineEdit,
    QGridLayout, QTableWidgetItem
)

import logging

logger = logging.getLogger(__name__)


#* Path to ui file for reservation management
PATH_TO_UI = "Application/GUI/UI/Reservation_Management.ui"



class ManageReservation(QWidget):

    go_back=pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi(PATH_TO_UI, self)
        self.back_btn.clicked.connect(self.go_back.emit)