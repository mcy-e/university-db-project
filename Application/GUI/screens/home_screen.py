
#& Imports

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from GUI.screens.side_menu import SideMenu

import logging

logger = logging.getLogger(__name__)

#* Path to ui file for home screen
PATH_TO_UI = "Application/GUI/UI/home_screen.ui"

class HomeScreen(QWidget):
    
    #* Create Signals
    navigate_to_crud = pyqtSignal()
    navigate_to_academic = pyqtSignal()
    navigate_to_performance = pyqtSignal()
    navigate_to_results = pyqtSignal()
    navigate_to_queries = pyqtSignal()
    navigate_to_audit = pyqtSignal()
    navigate_to_settings = pyqtSignal()
    open_side_bar = pyqtSignal()  #* Keep for compatibility with MainWindow

    def __init__(self):
        super().__init__()
        
        #* Create container for original content
        self.content_widget = QWidget()
        uic.loadUi(PATH_TO_UI, self.content_widget)
        
        #* Initialize side menu
        self.side_menu = SideMenu()
        self.side_menu.setFixedWidth(0)  #* Start with 0 width (hidden)
        
        #* Create horizontal layout to hold side menu and content
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.side_menu)
        self.main_layout.addWidget(self.content_widget)
        
        #* Menu state
        self.menu_visible = False
        
        #* Connect signals for navigation
        self.content_widget.menu_btn.clicked.connect(self.toggle_side_menu)
        self.content_widget.crud_btn.clicked.connect(self.navigate_to_crud.emit)
        self.content_widget.academic_btn.clicked.connect(self.navigate_to_academic.emit)
        self.content_widget.performance_btn.clicked.connect(self.navigate_to_performance.emit)
        self.content_widget.results_btn.clicked.connect(self.navigate_to_results.emit)
        self.content_widget.queries_btn.clicked.connect(self.navigate_to_queries.emit)
        self.content_widget.audit_btn.clicked.connect(self.navigate_to_audit.emit)
        self.content_widget.settings_btn.clicked.connect(self.navigate_to_settings.emit)
        
        #* Connect side menu signals - no close button needed since hamburger toggles it
        
        logger.info("HomeScreen initialized")

    #* Toggle side menu visibility with animation    
    def toggle_side_menu(self):

        if self.menu_visible:
            self.hide_side_menu()
        else:
            self.show_side_menu()
    
    #* Show side menu with resize animation
    def show_side_menu(self):

        #* Create animation for side menu width
        self.animation = QPropertyAnimation(self.side_menu, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(0)
        self.animation.setEndValue(250)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        #* Animate minimum width to ensure smooth animation
        self.animation_min = QPropertyAnimation(self.side_menu, b"minimumWidth")
        self.animation_min.setDuration(300)
        self.animation_min.setStartValue(0)
        self.animation_min.setEndValue(250)
        self.animation_min.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.animation.start()
        self.animation_min.start()
        
        self.menu_visible = True
        logger.info("Side menu opened")

    #* Hide side menu with resize animation    
    def hide_side_menu(self):

        #* Create animation for side menu width
        self.animation = QPropertyAnimation(self.side_menu, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(250)
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QEasingCurve.Type.InCubic)
        
        #* Animate minimum width
        self.animation_min = QPropertyAnimation(self.side_menu, b"minimumWidth")
        self.animation_min.setDuration(300)
        self.animation_min.setStartValue(250)
        self.animation_min.setEndValue(0)
        self.animation_min.setEasingCurve(QEasingCurve.Type.InCubic)
        
        self.animation.start()
        self.animation_min.start()
        
        self.menu_visible = False
        logger.info("Side menu closed")