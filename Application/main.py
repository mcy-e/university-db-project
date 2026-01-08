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
from GUI.main_window import MainWindow
from PyQt6.QtWidgets import QApplication
from UTILS.log import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)
logger.info("Application started")

BASE_DIR = Path(__file__).resolve().parent
PATH_TO_DEFAULT_STYLE = BASE_DIR / "GUI" / "styling" / "default.qss"

def load_stylesheet(app: QApplication, path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            stylesheet = f.read()
        app.setStyleSheet(stylesheet)
        logger.info(f"Stylesheet loaded: {path}")
    except Exception as e:
        logger.error(f"Failed to load stylesheet: {e}")

def start():
    #* APP instance
    app = QApplication(sys.argv)
    
    #* Set Fusion style 
    app.setStyle("Fusion")
    
    #* Load stylesheet
    load_stylesheet(app, PATH_TO_DEFAULT_STYLE)
   
    #* Window instance
    window = MainWindow()
    window.show()

    #* Start the loop
    sys.exit(app.exec())

if __name__ == '__main__':
    start()