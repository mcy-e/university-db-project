
#& Imports


from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QHeaderView, QLabel, QLineEdit,
    QGridLayout, QTableWidgetItem
)

import logging

logger = logging.getLogger(__name__)


#* Path to ui file for the academic menu
PATH_TO_UI = "Application/GUI/UI/performance_menu.ui"



class PerformanceMenu(QWidget):
    
    #* Create Signals
    navigate_to_attendance=pyqtSignal()
    navigate_to_marks=pyqtSignal()
    go_back=pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi(PATH_TO_UI, self)
        self.back.clicked.connect(self.go_back.emit)
        self.attendance.clicked.connect(self.navigate_to_attendance.emit)
        self.marks.clicked.connect(self.navigate_to_marks.emit)
