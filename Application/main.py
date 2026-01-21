"""
    Application.main
    Main entry point that:
    Creates the QApplication instance
    Initializes and displays MainWindow
    Starts the event loop
"""

import sys, os

#* Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#& imports
from pathlib import Path 
from GUI.settings.settings import SettingsScreen
from GUI.main_window import MainWindow
from PyQt6.QtWidgets import QApplication
from GUI.styling import styling_loader as sl
from UTILS.log import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)
logger.info("Application started")

BASE_DIR = Path(__file__).resolve().parent
PATH_TO_DEFAULT_STYLE = BASE_DIR / "GUI" / "styling" / "default.qss"


def start():
    #* APP instance
    app = QApplication(sys.argv)
    
    #* Load Language
    SettingsScreen.load_language(app)
    
    #* Set Fusion style 
    app.setStyle("Fusion")
    
    #* Load stylesheet
    sl.load_stylesheet(app, PATH_TO_DEFAULT_STYLE)
   
    #* Window instance
    window = MainWindow()
    window.show()

    #* Start the loop
    sys.exit(app.exec())

if __name__ == '__main__':
    start()