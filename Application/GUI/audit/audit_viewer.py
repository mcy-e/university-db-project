#& Imports

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, QDate
from PyQt6.QtWidgets import (
    QWidget, QHeaderView, QTableWidgetItem, QMessageBox
)

from Database import database as db


from GUI.styling import styling_loader as sl

import logging

logger = logging.getLogger(__name__)

#* Path to ui file for audit viewer
PATH_TO_UI = "Application/GUI/UI/audit_viewer.ui"

class AuditViewer(QWidget):

    go_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi(PATH_TO_UI, self)
        
        #* Setup UI components
        self._setup_table()
        self._populate_table_filter()
        self._connect_signals()
        
        #* Set default dates
        self.from_date_selection.setDate(QDate.currentDate().addMonths(-1))
        self.to_date_selection.setDate(QDate.currentDate())

        sl.apply_button_styles(self,sl.AUDIT_VIEWER_STYLES)
        
        logger.info("AuditViewer initialized")

    #* Setup the audit log table with proper columns
    def _setup_table(self):
 
        headers = ["Timestamp", "User", "Action", "Table", "Details"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        #* Stretch all columns
        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        
        #* Hide row numbers
        self.table.verticalHeader().setVisible(False)
        
        logger.debug("Audit table configured")

    #* Populate the table filter dropdown
    def _populate_table_filter(self):

        self.table_selection.addItem("All Tables")
        
        tables = db.get_table_names()
        for table in tables:
            self.table_selection.addItem(table)
        
        logger.debug(f"Loaded {len(tables)} tables for filter")

    #* Connect all signals 
    def _connect_signals(self):
     
        self.back.clicked.connect(self.go_back.emit)
        self.filter.clicked.connect(self._filter_logs)
        self.refresh.clicked.connect(self._refresh_logs)
        
        logger.debug("All signals connected")

    #* Filter audit logs 
    def _filter_logs(self):

        from_date = self.from_date_selection.date().toString("yyyy-MM-dd")
        to_date = self.to_date_selection.date().toString("yyyy-MM-dd")
        
        table_index = self.table_selection.currentIndex()
        table_name = None if table_index == 0 else self.table_selection.currentText()
        
        try:
            logs = db.get_audit_logs(from_date, to_date, table_name)
            self._display_logs(logs)
            logger.info(f"Filtered logs: {len(logs)} records found")
        except Exception as e:
            logger.error(f"Error filtering logs: {e}")
            QMessageBox.critical(self, "Error", f"Failed to filter logs: {e}")

    #* Refresh the audit logs
    def _refresh_logs(self):
        
        self._filter_logs()

    #* Display logs in the table
    def _display_logs(self, logs):
 
        self.table.setRowCount(0)
        
        for row_idx, log in enumerate(logs):
            timestamp, user, action, table, details = log
            
            self.table.insertRow(row_idx)
            
            self.table.setItem(row_idx, 0, QTableWidgetItem(timestamp))
            self.table.setItem(row_idx, 1, QTableWidgetItem(user))
            self.table.setItem(row_idx, 2, QTableWidgetItem(action))
            self.table.setItem(row_idx, 3, QTableWidgetItem(table))
            self.table.setItem(row_idx, 4, QTableWidgetItem(details))
        
        logger.debug(f"Displayed {len(logs)} logs in table")