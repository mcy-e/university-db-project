
#& Imports

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QMessageBox
import webbrowser
import logging

logger = logging.getLogger(__name__)

#* Path to ui file for side menu
PATH_TO_UI = "Application/GUI/UI/side_menu.ui"

class SideMenu(QWidget):
    
    #* Create Signals
    close_menu = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        uic.loadUi(PATH_TO_UI, self)
        
        #* Connect signals
        self.github_dev1_btn.clicked.connect(self.open_github_dev1)
        self.linkedin_dev1_btn.clicked.connect(self.open_linkedin_dev1)
        self.twitter_dev1_btn.clicked.connect(self.open_twitter_dev1)
        self.github_dev2_btn.clicked.connect(self.open_github_dev2)
        self.linkedin_dev2_btn.clicked.connect(self.open_linkedin_dev2)
        self.twitter_dev2_btn.clicked.connect(self.open_twitter_dev2)
        self.about_btn.clicked.connect(self.show_about)
        
        logger.info("SideMenu initialized")

    #* Open GitHub profile for Reffas Chouaib in browser    
    def open_github_dev1(self):
        webbrowser.open("https://github.com/mcy-e")  
        logger.info("Opening GitHub for Reffas Chouaib")

    #* Open LinkedIn profile for Reffas Chouaib in browser    
    def open_linkedin_dev1(self):
        webbrowser.open("https://linkedin.com/in/chouaibreffas")  
        logger.info("Opening LinkedIn for Reffas Chouaib")

    #* Open Twitter profile for Reffas Chouaib in browser    
    def open_twitter_dev1(self):
        webbrowser.open("https://x.com/MRc_MCY")  
        logger.info("Opening Twitter for Reffas Chouaib")

    #* Open GitHub profile for Fehis Mohammed Essadek in browser    
    def open_github_dev2(self):
        webbrowser.open("https://github.com/M071m2d")  
        logger.info("Opening GitHub for Fehis Mohammed Essadek")

    #* Open LinkedIn profile for Fehis Mohammed Essadek in browser    
    def open_linkedin_dev2(self):
        webbrowser.open("https://www.linkedin.com/in/fehis-mohamed-essadek-43aa2337a") 
        logger.info("Opening LinkedIn for Fehis Mohammed Essadek")

    #* Open Twitter profile for Fehis Mohammed Essadek in browser    
    def open_twitter_dev2(self):
        webbrowser.open("https://x.com/SadekSdmoh88238")  
        logger.info("Opening Twitter for Fehis Mohammed Essadek")

    #* Show about with app and dev info    
    def show_about(self):
        about_text = f""" 
            <h2>{self.tr("University Management System")}</h2>
            <p><b style="color: #ff9800;">{self.tr("BETA VERSION")}</b></p>
            <p>{self.tr("A comprehensive system for managing university operations including student records, academic management, performance tracking, and results processing.")}</p>
            
            <h3>{self.tr("Current Features:")}</h3>
            <ul>
                <li>{self.tr("Complete CRUD Operations (Create, Read, Update, Delete)")}</li>
                <li>{self.tr("Academic Management Tools")}</li>
                <li>{self.tr("Student Performance Tracking")}</li>
                <li>{self.tr("Theme Selection & Customization")}</li>
                <li>{self.tr("Multi-language Support (English, Arabic, French)")}</li>
            </ul>
            
            <h3>{self.tr("Coming Soon:")}</h3>
            <ul>
                <li>{self.tr("Advanced Settings (Date/Time formats, Notifications, etc.)")}</li>
                <li>{self.tr("PDF Export Functionality")}</li>
                <li>{self.tr("Database Backup & Restore")}</li>
            </ul>
            
            <h3>{self.tr("Developed By:")}</h3>
            <p><b>{self.tr("Reffas Chouaib")}</b></p>
            <p><b>{self.tr("Fehis Mohammed Essadek")}</b></p>

            <hr>
            <p><b>{self.tr("Version:")}</b> {self.tr("1.0.0 Beta")} </p>
            <p><b>{self.tr("Release Date:")}</b> {self.tr("January 2026")}</p>
            <p style="color: #888;"><i>{self.tr("Thank you for testing our beta release!")}</i></p>
            """
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.tr("About"))
        msg_box.setTextFormat(Qt.TextFormat.RichText)  
        msg_box.setText(about_text)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()
        
        logger.info("About dialog shown")