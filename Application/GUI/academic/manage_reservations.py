
#& Imports

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, QDate, QTime
from PyQt6.QtWidgets import (
    QWidget, QHeaderView, QTableWidgetItem, QMessageBox, QPushButton
)

from Database import database as db

import logging

logger = logging.getLogger(__name__)

#* Path to ui file for reservation management
from config import get_resource_path
import os
PATH_TO_UI = get_resource_path(os.path.join("GUI", "UI", "Reservation_Management.ui"))


#* Working hours constraints
WORK_START_TIME = QTime(8, 0)   # 8:00 AM
WORK_END_TIME = QTime(18, 0)    # 6:00 PM

class ManageReservation(QWidget):

    go_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi(PATH_TO_UI, self)
        
        #* Store all reservations for filtering
        self.all_reservations = []
        
        #* Setup UI components FIRST before loading data
        self._setup_table()
        self._connect_signals()
        self._populate_dropdowns()
        
        #* Set default dates to today
        today = QDate.currentDate()
        self.date_edit.setDate(today)
        self.date_edit_filter.setDate(today)
        
        #* Set default times within working hours
        self.start_edit.setTime(WORK_START_TIME)
        self.end_edit.setTime(QTime(10, 0))
        
        #* Disable create button initially
        self.create_reservation_btn.setEnabled(False)
        
        #* Load reservations LAST (after everything is set up)
        self._load_all_reservations()
        
        logger.info("ManageReservation initialized")

    #* Setup the reservations table
    def _setup_table(self):
        headers = [ self.tr("ID"),
                    self.tr("Room"),
                    self.tr("Course"),
                    self.tr("Instructor"),
                    self.tr("Date"),
                    self.tr("Start"),
                    self.tr("End"),
                    self.tr("Hours"),
                    self.tr("Actions")]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        #* Stretch most columns, but keep Actions column fixed
        header = self.table.horizontalHeader()
        for i in range(len(headers) - 1):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(len(headers) - 1, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(len(headers) - 1, 100)
        
        #* Hide row numbers
        self.table.verticalHeader().setVisible(False)
        
        #* Select rows only
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)
        
        logger.debug("Reservation table configured")

    #* Populate all dropdown menus with data
    def _populate_dropdowns(self):
        #* Populate purpose (Activity types)
        activities = [self.tr("Lecture"),
                     self.tr("Tutorial"),
                     self.tr("Practical"),
                     self.tr("Exam")]
        self.purpose_selection.addItems(activities)
        
        #* Populate rooms
        rooms = db.get_all_rooms()
        self.room_selection.addItem(self.tr("Select Room"))
        self.room_filter_selection.addItem(self.tr("All Rooms"))
       
        for building, roomno, capacity in rooms:
            room_display = f"{building} {roomno} (Cap: {capacity})"
            self.room_selection.addItem(room_display, userData=(building, roomno))
            self.room_filter_selection.addItem(room_display, userData=(building, roomno))
        
        #* Populate courses
        courses = db.get_courses_for_reservation()
        self.course_selection.addItem(self.tr("Select Course"))
        for course_id, display, dept_id in courses:
            self.course_selection.addItem(display, userData=(course_id, dept_id))
        
        #* Populate instructors
        instructors = db.get_instructors_for_reservation()
        self.instructor_selection.addItem(self.tr("Select Instructor"))
        for inst_id, display, dept_id in instructors:
            self.instructor_selection.addItem(display, userData=(inst_id, dept_id))
        
        logger.debug(f"Loaded {len(rooms)} rooms, {len(courses)} courses, {len(instructors)} instructors")

    #* Load all reservations from database and display them
    def _load_all_reservations(self):
        try:
            reservations = db.get_all_reservations()
            self.all_reservations = reservations
            self._display_reservations(reservations)
            logger.info(f"Loaded {len(reservations)} reservations")
        except Exception as e:
            logger.error(f"Error loading reservations: {e}")
            QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to load reservations:")+ f" {e}")

    #* Display reservations in the table
    def _display_reservations(self, reservations):
        #* Block signals to prevent triggering during setup
        self.table.blockSignals(True)
        
        #* Clear existing rows
        self.table.setRowCount(0)
        
        #* Get lookups for displaying names instead of IDs
        courses = {c[0]: c[1] for c in db.get_all_courses()}
        instructors_data = db.get_all_instructors()
        instructors = {i[0]: f"{i[4]} {i[3]} {i[2]}" for i in instructors_data}
        
        for row_idx, reservation in enumerate(reservations):
            reservation_id, building, roomno, course_id, dept_id, instructor_id, \
                reserv_date, start_time, end_time, hours_number = reservation
            
            self.table.insertRow(row_idx)
            
            #* Format display data
            room_display = f"{building} {roomno}"
            course_display = courses.get(course_id, f"Course {course_id}")
            instructor_display = instructors.get(instructor_id, f"Instructor {instructor_id}")
            
            #* Add data to table
            data = [
                str(reservation_id),
                room_display,
                course_display,
                instructor_display,
                str(reserv_date),
                str(start_time),
                str(end_time),
                str(hours_number)
            ]
            
            for col_idx, value in enumerate(data):
                item = QTableWidgetItem(value)
                self.table.setItem(row_idx, col_idx, item)
            
            #* Add delete button in Actions column
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, res_id=reservation_id: self._delete_reservation(res_id))
            self.table.setCellWidget(row_idx, 8, delete_btn)
        
        #* Unblock signals
        self.table.blockSignals(False)
        
        logger.debug(f"Displayed {len(reservations)} reservations in table")
    
    #* Connect all button and widget signals
    def _connect_signals(self):
        self.back_btn.clicked.connect(self.go_back.emit)
        
        #* Make the top "create reservation" button work as refresh
        self.creat_reservation.clicked.connect(self._refresh_table)
        
        self.check_availability_btn.clicked.connect(self._check_availability)
        self.create_reservation_btn.clicked.connect(self._create_reservation)
        
        #* Connect filter changes
        self.room_filter_selection.currentIndexChanged.connect(self._apply_filters)
        self.date_edit_filter.dateChanged.connect(self._apply_filters)
        
        #* Connect form changes to reset create button
        self.room_selection.currentIndexChanged.connect(self._on_form_change)
        self.course_selection.currentIndexChanged.connect(self._on_form_change)
        self.instructor_selection.currentIndexChanged.connect(self._on_form_change)
        self.date_edit.dateChanged.connect(self._on_form_change)
        self.start_edit.timeChanged.connect(self._on_form_change)
        self.end_edit.timeChanged.connect(self._on_form_change)
        
        logger.debug("All signals connected")

    #* Refresh the table by reloading all reservations
    def _refresh_table(self):
        logger.info("Refreshing reservations table")
        self._load_all_reservations()
        self.status.setText(self.tr("Status: Table refreshed"))

    #* Handle form changes - disable create button when form is modified
    def _on_form_change(self):
        self.create_reservation_btn.setEnabled(False)
        self.status.setText(self.tr("Status: Check availability before creating"))

    #* Validate working hours
    def _validate_working_hours(self, start_time, end_time):
        if start_time < WORK_START_TIME or end_time > WORK_END_TIME:
            return False, f"Reservations must be between {WORK_START_TIME.toString('HH:mm')} and {WORK_END_TIME.toString('HH:mm')}"
        return True, ""

    #* Check if selected room is available for selected time slot
    def _check_availability(self):
        #* Validate room selection
        if self.room_selection.currentIndex() == 0:
            self.status.setText(self.tr("Status: Please select a room"))
            return
        
        #* Validate course selection
        if self.course_selection.currentIndex() == 0:
            self.status.setText(self.tr("Status: Please select a course"))
            return
        
        #* Validate instructor selection
        if self.instructor_selection.currentIndex() == 0:
            self.status.setText(self.tr("Status: Please select an instructor"))
            return
        
        #* Get selected data
        room_data = self.room_selection.currentData()
        if not room_data:
            self.status.setText(self.tr("Status: Invalid room selection"))
            return
        
        building, roomno = room_data
        date = self.date_edit.date().toString("yyyy-MM-dd")
        start_time = self.start_edit.time()
        end_time = self.end_edit.time()
        
        #* Validate time range
        if start_time >= end_time:
            self.status.setText(self.tr("Status: End time must be after start time"))
            return
        
        #* Validate working hours
        is_valid, error_msg = self._validate_working_hours(start_time, end_time)
        if not is_valid:
            self.status.setText(f"Status: {error_msg}")
            return
        
        start_time_str = start_time.toString("HH:mm:ss")
        end_time_str = end_time.toString("HH:mm:ss")
        
        #* Check availability with database
        try:
            is_available = db.check_room_availability(building, roomno, date, start_time_str, end_time_str)
            
            if is_available:
                self.status.setText(self.tr("Status: Room is available! You can now create the reservation"))
                self.create_reservation_btn.setEnabled(True)
                logger.info(f"Room {building} {roomno} is available on {date} from {start_time_str} to {end_time_str}")
            else:
                self.status.setText(self.tr("Status: Room is already booked for this time"))
                self.create_reservation_btn.setEnabled(False)
                logger.warning(f"Room {building} {roomno} conflict on {date}")
                
        except Exception as e:
            logger.error(f"Error checking availability: {e}")
            self.status.setText(self.tr("Status: Error checking availability"))
            self.create_reservation_btn.setEnabled(False)

    #* Create a new reservation
    def _create_reservation(self):
        #* Get all selected data
        room_data = self.room_selection.currentData()
        course_data = self.course_selection.currentData()
        instructor_data = self.instructor_selection.currentData()
        
        if not room_data or not course_data or not instructor_data:
            QMessageBox.warning(self, self.tr("Validation Error"), self.tr("Please select all required fields"))
            return
        
        building, roomno = room_data
        course_id, dept_id = course_data
        instructor_id, _ = instructor_data
        
        date = self.date_edit.date().toString("yyyy-MM-dd")
        start_time = self.start_edit.time()
        end_time = self.end_edit.time()
        start_time_str = start_time.toString("HH:mm:ss")
        end_time_str = end_time.toString("HH:mm:ss")
        
        #* Calculate hours
        hours = start_time.secsTo(end_time) / 3600
        
        logger.info(f"Attempting to create reservation: {building} {roomno}, Course: {course_id}, Instructor: {instructor_id}, Date: {date}, Time: {start_time_str}-{end_time_str}")
        
        #* Double check availability
        try:
            is_available = db.check_room_availability(building, roomno, date, start_time_str, end_time_str)
            
            if not is_available:
                QMessageBox.warning(
                    self, 
                    self.tr("Reservation Conflict"), 
                    self.tr("This room is no longer available. Please check availability again.")
                )
                self.create_reservation_btn.setEnabled(False)
                return
            
            #* Create the reservation - call database function
            result = db.add_reservation(
                building, roomno, course_id, dept_id, instructor_id,
                date, start_time_str, end_time_str, int(hours)
            )
            
            logger.info(f"Database add_reservation returned: {result}")
            
            #* Check if result is success (True or tuple with success)
            if result is True or (isinstance(result, tuple) and result[0] is True):
                QMessageBox.information(self, self.tr("Success"), self.tr("Reservation created successfully!"))
                self.status.setText(self.tr("Status: Reservation created successfully"))
                
                #* Reload reservations to show new one
                self._load_all_reservations()
                
                #* Clear form
                self._clear_form()
                
                logger.info(f"Created reservation for {building} {roomno} on {date}")
            else:
                QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to create reservation - Database returned False"))
                logger.error("Database returned False for add_reservation")
                
        except Exception as e:
            logger.error(f"Error creating reservation: {e}")
            QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to create reservation:") +f" {e}")

    #* Delete a reservation
    def _delete_reservation(self, reservation_id):
        logger.info(f"Delete button clicked for reservation ID: {reservation_id}")
        
        reply = QMessageBox.question(
            self,
            self.tr("Confirm Deletion"),
            self.tr("Are you sure you want to delete reservation") +f" #{reservation_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                logger.info(f"Calling db.delete_reservation({reservation_id})")
                result = db.delete_reservation(reservation_id)
                logger.info(f"Database delete_reservation returned: {result}")
                
                #* Check if deletion was successful
                if result is True:
                    QMessageBox.information(self, self.tr("Success"), self.tr("Reservation deleted successfully!"))
                    
                    #* Update the UI by removing from stored data and refreshing display
                    self.all_reservations = [r for r in self.all_reservations if r[0] != reservation_id]
                    self._display_reservations(self.all_reservations)
                    
                    logger.info(f"Deleted reservation {reservation_id} and refreshed UI")
                else:
                    QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to delete reservation - Database returned False"))
                    logger.error(f"Database returned False for delete_reservation({reservation_id})")
                    
            except Exception as e:
                logger.error(f"Error deleting reservation: {e}")
                QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to delete reservation:") + f" {e}")

    #* Clear the reservation form
    def _clear_form(self):
        self.room_selection.setCurrentIndex(0)
        self.course_selection.setCurrentIndex(0)
        self.instructor_selection.setCurrentIndex(0)
        self.purpose_selection.setCurrentIndex(0)
        self.date_edit.setDate(QDate.currentDate())
        self.start_edit.setTime(WORK_START_TIME)
        self.end_edit.setTime(QTime(10, 0))
        self.status.setText(self.tr("Status:"))
        self.create_reservation_btn.setEnabled(False)

    #* Apply room and date filters to the reservation table
    def _apply_filters(self):
        #* Get filter values
        room_filter = None
        if self.room_filter_selection.currentIndex() > 0:
            room_data = self.room_filter_selection.currentData()
            if room_data:
                building, roomno = room_data
                room_filter = f"{building} {roomno}"
        
        date_filter = self.date_edit_filter.date().toString("yyyy-MM-dd")
        
        #* Filter reservations
        filtered = []
        for reservation in self.all_reservations:
            reservation_id, building, roomno, course_id, dept_id, instructor_id, \
                reserv_date, start_time, end_time, hours_number = reservation
            
            room_match = True
            date_match = True
            
            #* Check room filter
            if room_filter:
                reservation_room = f"{building} {roomno}"
                room_match = (reservation_room == room_filter)
            
            #* Check date filter
            if date_filter:
                date_match = (str(reserv_date) == date_filter)
            
            if room_match and date_match:
                filtered.append(reservation)
        
        #* Display filtered results
        self._display_reservations(filtered)
        logger.debug(f"Applied filters: {len(filtered)} reservations match")