#& Imports

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, QDate
from PyQt6.QtWidgets import (
    QWidget, QMessageBox, QFileDialog
)

from PyQt6.QtCore import QTranslator

from PyQt6.QtCore import QEvent

from PyQt6.QtCore import QTimer

from PyQt6.QtWidgets import QApplication

from GUI.styling import styling_loader as sl

from pathlib import Path

from datetime import datetime

import sys

import os

import json

import logging

logger = logging.getLogger(__name__)

#* Path to UI file and settings storage
from config import get_resource_path
import os
PATH_TO_UI = get_resource_path(os.path.join("GUI", "UI", "settings.ui"))

if getattr(sys, 'frozen', False):
    base_dir = Path(sys.executable).parent
else:
    base_dir = Path(__file__).resolve().parent

SETTINGS_FILE = str(base_dir / "app_settings.json")


STYLING_DIR = Path(get_resource_path(os.path.join("GUI", "styling")))

class SettingsScreen(QWidget):
    
    #* Settings screen with auto-save functionality and theme management
    
    go_back = pyqtSignal()

    #* Emit theme file path when changed
    theme_changed = pyqtSignal(str)  
    
    #* Emit language when changed
    language_changed = pyqtSignal(str)  
    
    #* Date formats
    DATE_FORMATS = {
        "DD/MM/YYYY": "%d/%m/%Y",
        "MM/DD/YYYY": "%m/%d/%Y",
        "YYYY-MM-DD": "%Y-%m-%d",
        "DD.MM.YYYY": "%d.%m.%Y"
    }
    
    #* Time formats
    TIME_FORMATS = {
        "24-hour (HH:MM)": "%H:%M",
        "12-hour (hh:MM AM/PM)": "%I:%M %p"
    }
    
    LANGUAGE_DIR = Path(get_resource_path("Translations"))

    LANGUAGE_FILES = {
        "English": None, 
        "العربية (Arabic)": "ar.qm",
        "Français (French)": "fr.qm"
    }
    
    @classmethod
    #* Load language from settings class method  
    def load_language(cls, app):

        
        #* Check if settings file exists
        if not Path(SETTINGS_FILE).exists():
            return

        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            lang = settings.get('language', 'English')
            qm_file = cls.LANGUAGE_FILES.get(lang)
            
            if qm_file:
                qm_path = cls.LANGUAGE_DIR / qm_file
                if qm_path.exists():

                    translator = QTranslator()
                    
                    if translator.load(str(qm_path)):
                        app.installTranslator(translator)
                
                        app.translator = translator 
                        logger.info(f"Loaded language: {lang}")
                    else:
                        logger.error(f"Failed to load translation: {qm_file}")
                else:
                    logger.warning(f"Translation file missing: {qm_path}")
                    
        except Exception as e:
            logger.error(f"Error loading language: {e}")


    def __init__(self):
        super().__init__()
        uic.loadUi(PATH_TO_UI, self)
        
        #* Status message timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._clear_status)
        
        #* Initialize UI
        self._discover_themes()
        self._populate_dropdowns()
        self._disable_unimplemented_features()
        self._load_settings()
        self._connect_signals()

        logger.info("Settings Screen initialized")

    #* Discover all .qss files in the styling directory
    def _discover_themes(self):
        
        
        self.available_themes = {}
        
        if not STYLING_DIR.exists():
            logger.warning(f"Styling directory not found: {STYLING_DIR}")
            return
        
        #* Find all .qss files
        for qss_file in STYLING_DIR.glob("*.qss"):
            theme_name = qss_file.stem.replace("_", " ").title()
            self.available_themes[theme_name] = str(qss_file)
        
        logger.info(f"Discovered {len(self.available_themes)} themes: {list(self.available_themes.keys())}")

    #* Populate all dropdown menus
    def _populate_dropdowns(self):

        
        #* Theme selection
        if self.available_themes:
            self.theme_selection.addItems(sorted(self.available_themes.keys()))
        else:
            self.theme_selection.addItem("Default")
            logger.warning("No themes found... , added 'Default' placeholder")
        
        #* Language selection

        self.language_selection.addItems([
            "English",
            "العربية (Arabic)",
            "Français (French)"
        ])
        
        #* Date format selection
        self.date_format_selection.addItems(self.DATE_FORMATS.keys())
        
        #* Time format selection
        self.time_format_selection.addItems(self.TIME_FORMATS.keys())
        
        #* Default semester
        self.default_semester_selection.addItems([
            "Semester 1",
            "Semester 2",])
        
        #* Academic year
        current_year = datetime.now().year
        years = [f"{year}-{year+1}" for year in range(current_year-2, current_year+2)]
        self.academic_year_selection.addItems(years)

    #* Disable unimplemented features and add tooltips
    def _disable_unimplemented_features(self):
        
        tooltip_text = "Feature coming soon in future versions"
        
        #* Appearance - Font Size (disable)
        self.font_size_spinbox.setEnabled(False)
        self.font_size_spinbox.setToolTip(tooltip_text)
        
        #* Regional - Date & Time Formats (disable)
        self.date_format_selection.setEnabled(False)
        self.date_format_selection.setToolTip(tooltip_text)
        
        self.time_format_selection.setEnabled(False)
        self.time_format_selection.setToolTip(tooltip_text)
        
        #* Notifications - Coming Soon
        self.enable_notifications.setEnabled(False)
        self.enable_notifications.setToolTip(tooltip_text)
        
        self.enable_sound.setEnabled(False)
        self.enable_sound.setToolTip(tooltip_text)
        
        #* Data Management - Auto Backup
        self.auto_backup.setEnabled(False)
        self.auto_backup.setToolTip(tooltip_text)
        
        #* Academic Settings
        self.default_semester_selection.setEnabled(False)
        self.default_semester_selection.setToolTip(tooltip_text)
        
        self.academic_year_selection.setEnabled(False)
        self.academic_year_selection.setToolTip(tooltip_text)
        
        #* Advanced - Coming Soon
        self.rows_per_page_spinbox.setEnabled(False)
        self.rows_per_page_spinbox.setToolTip(tooltip_text)
        
        self.confirm_delete.setEnabled(False)
        self.confirm_delete.setToolTip(tooltip_text)
        
        logger.info("Disabled unimplemented features (keeping only Language and Theme active)")



    #* Connect all signals for auto-save and actions
    def _connect_signals(self):
        
        
        #* Navigation
        self.back.clicked.connect(self.go_back.emit)
        
        #* Appearance
        self.theme_selection.currentTextChanged.connect(self._on_theme_changed)
        self.font_size_spinbox.valueChanged.connect(self._auto_save)
        
        #* Regional
        self.language_selection.currentTextChanged.connect(self._on_language_changed)
        self.date_format_selection.currentTextChanged.connect(self._auto_save)
        self.time_format_selection.currentTextChanged.connect(self._auto_save)
        
        #* Notifications
        self.enable_notifications.stateChanged.connect(self._auto_save)
        self.enable_sound.stateChanged.connect(self._auto_save)
        
        #* Data Management
        self.auto_backup.stateChanged.connect(self._auto_save)
        self.backup_now_btn.clicked.connect(self._backup_database)
        self.restore_backup_btn.clicked.connect(self._restore_database)
        
        #* Academic
        self.default_semester_selection.currentTextChanged.connect(self._auto_save)
        self.academic_year_selection.currentTextChanged.connect(self._auto_save)
        
        #* Advanced
        self.rows_per_page_spinbox.valueChanged.connect(self._auto_save)
        self.confirm_delete.stateChanged.connect(self._auto_save)
        
        #* Reset button
        self.reset_defaults_btn.clicked.connect(self._reset_to_defaults)
        
        logger.debug("All signals connected")

    #* Load settings from JSON file
    def _load_settings(self):
       
        
        if not Path(SETTINGS_FILE).exists():
            logger.info("Settings file not found, using defaults")
            self._reset_to_defaults(silent=True)
            return
        
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            #* Appearance
            theme_name = settings.get('theme', list(self.available_themes.keys())[0] if self.available_themes else 'Default')
            idx = self.theme_selection.findText(theme_name)
            app = QApplication.instance()
            if idx >= 0 and app:
                self.theme_selection.setCurrentIndex(idx)
                sl.load_stylesheet(app, self.available_themes[theme_name], settings.get('font_size', 10))
                logger.info(f"Loaded theme '{theme_name}' from saved settings using path: '{self.available_themes[theme_name]}' ")
            
            self.font_size_spinbox.setValue(settings.get('font_size', 10))
            
            #* Regional
            lang = settings.get('language', 'English')
            idx = self.language_selection.findText(lang)
            if idx >= 0:
                self.language_selection.blockSignals(True)  
                self.language_selection.setCurrentIndex(idx)
                self.language_selection.blockSignals(False) 

            date_fmt = settings.get('date_format', 'DD/MM/YYYY')
            idx = self.date_format_selection.findText(date_fmt)
            if idx >= 0:
                self.date_format_selection.setCurrentIndex(idx)
            
            time_fmt = settings.get('time_format', '24-hour (HH:MM)')
            idx = self.time_format_selection.findText(time_fmt)
            if idx >= 0:
                self.time_format_selection.setCurrentIndex(idx)
            
            #* Notifications
            self.enable_notifications.setChecked(settings.get('enable_notifications', True))
            self.enable_sound.setChecked(settings.get('enable_sound', True))
            
            #* Data
            self.auto_backup.setChecked(settings.get('auto_backup', False))
            
            #* Academic
            semester = settings.get('default_semester', 'Semester 1')
            idx = self.default_semester_selection.findText(semester)
            if idx >= 0:
                self.default_semester_selection.setCurrentIndex(idx)
            
            year = settings.get('academic_year', f"{datetime.now().year}-{datetime.now().year+1}")
            idx = self.academic_year_selection.findText(year)
            if idx >= 0:
                self.academic_year_selection.setCurrentIndex(idx)
            
            #* Advanced
            self.rows_per_page_spinbox.setValue(settings.get('rows_per_page', 50))
            self.confirm_delete.setChecked(settings.get('confirm_delete', True))
            
            logger.info("Settings loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load settings: {e}")
            self._reset_to_defaults(silent=True)

    #* Auto-save settings when any option changes
    def _auto_save(self):
        
        #* Check if dropdowns are populated before saving
        if not self.date_format_selection.currentText() or not self.time_format_selection.currentText():
            logger.debug("Skipping auto save: dropdowns not populated yet...")
            return
        
        settings = {

            #* Appearance
            'theme': self.theme_selection.currentText(),
            'theme_file': self.available_themes.get(self.theme_selection.currentText(), ''),
            'font_size': self.font_size_spinbox.value(),
            
            #* Regional
            'language': self.language_selection.currentText(),
            'date_format': self.date_format_selection.currentText(),
            'date_format_code': self.DATE_FORMATS[self.date_format_selection.currentText()],
            'time_format': self.time_format_selection.currentText(),
            'time_format_code': self.TIME_FORMATS[self.time_format_selection.currentText()],
            
            #* Notifications
            'enable_notifications': self.enable_notifications.isChecked(),
            'enable_sound': self.enable_sound.isChecked(),
            
            #* Data
            'auto_backup': self.auto_backup.isChecked(),
            
            #* Academic
            'default_semester': self.default_semester_selection.currentText(),
            'academic_year': self.academic_year_selection.currentText(),
            
            #* Advanced
            'rows_per_page': self.rows_per_page_spinbox.value(),
            'confirm_delete': self.confirm_delete.isChecked()
        }
        
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            
            self._show_status("Settings saved", 2000)
            logger.debug("Settings auto-saved")

            #* Apply font size change immediately
            app = QApplication.instance()
            if app:
                theme_name = self.theme_selection.currentText()
                theme_file = self.available_themes.get(theme_name, '')
                if theme_file:
                     sl.load_stylesheet(app, theme_file, self.font_size_spinbox.value())
            
            
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            self._show_status("Error saving settings", 3000)

    #* Handle theme change    
    def _on_theme_changed(self, theme_name):
        
        theme_file = self.available_themes.get(theme_name, '')
        app = QApplication.instance()
        if not app:
            logger.error(f"APP instance not found")
            return

        if theme_file and Path(theme_file).exists() and app:
            self.theme_changed.emit(theme_file)
            self._auto_save()
            sl.load_stylesheet(app, theme_file, self.font_size_spinbox.value())
            self._show_status(f"Theme changed to {theme_name}", 2000)
            logger.info(f"Theme changed to: {theme_name} ({theme_file})")
        else:
            logger.warning(f"Theme file not found: {theme_file}")
            self._show_status(f"Theme file not found", 3000)

    #* Handle language change    
    def _on_language_changed(self, language):

        
        #* Save the language preference
        self._auto_save()
        
        logger.info(f"Language changed to {language}. Restarting application...")
        
        #* Show message to restart app
        msg = QMessageBox(self)
        msg.setWindowTitle("Restart Required")
        msg.setText(f"Language changed to {language}.\n\nThe application will now restart to apply changes.")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

        #* Force restart to apply changes
        python = sys.executable
        os.execl(python, python, *sys.argv)


               

    #* Create database backup
    def _backup_database(self):
        logger.debug("Feature Coming Soon!, database backup")
        QMessageBox.information(self, "Feature Coming Soon", "Database backup functionality will be available in future versions.")

    #* Restore database from backup
    def _restore_database(self):
        logger.debug("Feature Coming Soon!, restore database backup")
        QMessageBox.information(self, "Feature Coming Soon", "Database restore functionality will be available in future versions.")

    #* Reset all settings to default values
    def _reset_to_defaults(self, silent=False):
       
        
        if not silent:
            reply = QMessageBox.question(
                self,
                "Reset Settings",
                "Reset all settings to default values?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        #* Appearance
        if self.available_themes:
            self.theme_selection.setCurrentIndex(0)
        self.font_size_spinbox.setValue(10)
        
        #* Regional
        self.language_selection.setCurrentText("English")
        self.date_format_selection.setCurrentText("DD/MM/YYYY")
        self.time_format_selection.setCurrentText("24-hour (HH:MM)")
        
        #* Notifications
        self.enable_notifications.setChecked(True)
        self.enable_sound.setChecked(True)
        
        #* Data
        self.auto_backup.setChecked(False)
        
        #* Academic
        self.default_semester_selection.setCurrentText("Semester 1")
        current_year = datetime.now().year
        self.academic_year_selection.setCurrentText(f"{current_year}-{current_year+1}")
        
        #* Advanced
        self.rows_per_page_spinbox.setValue(50)
        self.confirm_delete.setChecked(True)
        
        self._auto_save()
        
        if not silent:
            self._show_status("Settings reset to defaults", 3000)
        
        logger.info("Settings reset to defaults")

    #* Show status message temporarily
    def _show_status(self, message, duration=2000):
        
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.status_timer.start(duration)

    #*Clear status message
    def _clear_status(self):
        
        self.status_label.setText("")
        self.status_timer.stop()
 
    #* Get current settings
    def get_current_settings(self):
       
        if Path(SETTINGS_FILE).exists():
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error reading settings: {e}")
        return None