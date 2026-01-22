"""
    Application.main
    Main entry point that:
    Creates the QApplication instance
    Initializes and displays MainWindow
    Starts the event loop
"""

import sys
import os

#* Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#& imports
from pathlib import Path 
from PyQt6.QtWidgets import QApplication, QMessageBox
from GUI.settings.settings import SettingsScreen
from GUI.main_window import MainWindow
from GUI.styling import styling_loader as sl
from UTILS.log import setup_logging
from config import get_database_config
from Database.connection import DatabaseConnection
import logging

setup_logging()
logger = logging.getLogger(__name__)
logger.info("Application started")

BASE_DIR = Path(__file__).resolve().parent
PATH_TO_DEFAULT_STYLE = BASE_DIR / "GUI" / "styling" / "default.qss"


def initialize_database():
    
    #* Initialize database connection using configuration from .env file
    
    try:
        db_config = get_database_config()
        DatabaseConnection.initialize_pool(**db_config)
        logger.info("Connected to database successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        QMessageBox.critical(
            None, 
            "Database Error", 
            f"Failed to connect to database:\n{e}\n\n"
            "Please check your .env file or DATABASE_URL environment variable."
        )
        return False


def start():
    #* APP instance
    app = QApplication(sys.argv)

    #* Initialize Database Connection
    if not initialize_database():
        sys.exit(1)
    
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