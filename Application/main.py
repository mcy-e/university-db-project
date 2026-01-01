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

import sys

from GUI.main_window import MainWindow

from PyQt6.QtWidgets import QApplication

from UTILS.log import setup_logging
import logging

setup_logging()

logger = logging.getLogger(__name__)
logger.info("Application started")

def _set_app_window_style(App:object):
    App.setStyle("Fusion")

def start():
    
    #* APP instance
    app = QApplication(sys.argv)
    _set_app_window_style(app)
   
    #* Window instance
    window = MainWindow()
    window.show()

    #* Start the loop
    app.exec()


if __name__=='__main__':
    start()