

#& IMPORTS
from PyQt6.QtWidgets import QPushButton, QWidget,QApplication
from typing import Dict

import logging

logger = logging.getLogger(__name__)

#* Apply style to every button in widget depending on description 
def apply_button_styles(widget: QWidget, button_styles: Dict[str, str]) -> None:

    for button_name, style in button_styles.items():
        button = widget.findChild(QPushButton, button_name)
        if button:
            button.setProperty('buttonStyle', style)
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()

#* Load style sheet to app using qss file path
def load_stylesheet(app: QApplication, path: str, font_size: int = None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            stylesheet = f.read()
        
        #* Inject font size if provided
        if font_size is None:
            #* Try to read from settings
            try:
                import json
                with open("app_settings.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    font_size = settings.get("font_size", None)
            except Exception:
                pass

        if font_size:
            #* Prepend global font rule
            global_rule = f"QWidget {{ font-size: {font_size}pt; }}\n"
            stylesheet = global_rule + stylesheet
            logger.info(f"injected font size: {font_size}pt")

        app.setStyleSheet(stylesheet)
        
        #* Force all widgets to refresh their style
        for widget in app.allWidgets():
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()
        
        logger.info(f"Stylesheet loaded: {path}")
    except Exception as e:
        logger.error(f"Failed to load stylesheet: {e}")

#? UI files buttons names and level (or description) dicts

#* home_screen.ui
HOME_SCREEN_STYLES = {
    'menu_btn': 'primary',
    'crud_btn': 'primary',
    'academic_btn': 'primary',
    'performance_btn': 'primary',
    'results_btn': 'primary',
    'queries_btn': 'primary',
    'audit_btn': 'primary',
    'settings_btn': 'primary'
}

#* crud_menu_screen.ui
CRUD_MENU_STYLES = {
    'back_btn': 'primary',
    'student_crud_btn': 'primary',
    'instructor_crud_btn': 'primary',
    'course_crud_btn': 'primary',
    'department_crud_btn': 'primary',
    'room_crud_btn': 'primary',
    'reservation_crud_btn': 'primary',
    'enrollment_crud_btn': 'primary',
    'mark_crud_btn': 'primary',
    'activity_crud_btn': 'primary',
    'exam_crud_btn': 'primary',
    'attendance_crud_btn': 'primary'
}

#* academic_menu.ui
ACADEMIC_MENU_STYLES = {
    'back_btn': 'primary',
    'IC_Assignments': 'primary',
    'reservation_managment': 'primary'
}

#* performance_menu.ui
PERFORMANCE_MENU_STYLES = {
    'back': 'primary',
    'attendance': 'primary',
    'marks': 'primary'
}

#* attendance_entry.ui
ATTENDANCE_ENTRY_STYLES = {
    'back': 'primary',
    'mark_all': 'primary',
    'save': 'primary'
}

#* marks_entry.ui
MARKS_ENTRY_STYLES = {
    'back': 'primary',
    'save': 'primary'
}

#* results_viewer.ui
RESULTS_VIEWER_STYLES = {
    'back': 'primary',
    'export_pdf': 'primary'
}

#* audit_viewer.ui
AUDIT_VIEWER_STYLES = {
    'back': 'primary',
    'filter': 'primary',
    'refresh': 'primary'
}

#* query_viewer.ui
QUERY_VIEWER_STYLES = {
    'back': 'primary',
    'execute_query': 'primary'
}

#* CRUD.ui
CRUD_STYLES = {
    'back_btn': 'primary',
    'add_btn': 'primary',
    'save_btn': 'primary',
    'update_btn': 'primary',
    'delete_btn': 'danger',
    'clear_btn': 'primary'
}

#* IC_Assignments.ui
IC_ASSIGNMENTS_STYLES = {
    'back_btn': 'primary',
    'assign_btn': 'primary',
    'remove': 'danger'
}

#* Reservation_Management.ui
RESERVATION_MANAGEMENT_STYLES = {
    'back_btn': 'primary',
    'creat_reservation': 'primary',
    'check_availability_btn': 'primary',
    'create_reservation_btn': 'primary'
}

#* settings.ui
SETTINGS_STYLES = {
    'back': 'primary',
    'backup_now_btn': 'primary',
    'restore_backup_btn': 'primary',
    'reset_defaults_btn': 'danger'
}