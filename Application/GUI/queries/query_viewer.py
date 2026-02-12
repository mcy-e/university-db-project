#& Imports

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QHeaderView, QTableWidgetItem, QMessageBox, QInputDialog
)

from Database import database as db

import logging

logger = logging.getLogger(__name__)

#* Path to ui file for query viewer
from config import get_resource_path
import os
PATH_TO_UI = get_resource_path(os.path.join("GUI", "UI", "query_viewer.ui"))


class QueryViewer(QWidget):

    go_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi(PATH_TO_UI, self)
        
        #* Setup UI components
        self._setup_table()
        self._populate_queries()
        self._connect_signals()
        
        logger.info("QueryViewer initialized")

    #* Setup the query results table
    def _setup_table(self):

        #* Hide row numbers
        self.table.verticalHeader().setVisible(False)
        
        logger.debug("Query table configured")

    #* Populate the query dropdown with available queries
    def _populate_queries(self):
 
        queries = db.get_available_queries()
        self.query_selection.addItem(self.tr("Select Query"))
        
        for query in queries:
            self.query_selection.addItem(query)
        
        logger.debug(f"Loaded {len(queries)} queries")

    #* Connect all signals to their handlers
    def _connect_signals(self):

        self.back.clicked.connect(self.go_back.emit)
        self.execute_query.clicked.connect(self._execute_selected_query)
        
        logger.debug("All signals connected")

    #* Execute the selected query
    def _execute_selected_query(self):
 
        query_index = self.query_selection.currentIndex()
        
        if query_index == 0:
            QMessageBox.warning(self, self.tr("Validation Error"), self.tr("Please select a query"))
            return
        
        query_name = self.query_selection.currentText()
        
        params = None
        
        #* Handle parameterized queries
        if query_name == "Students by Group":
            group_id, ok = QInputDialog.getInt(self, self.tr("Input"), self.tr("Enter Group ID:"))
            if ok:
                params = group_id
            else:
                return
                
        elif query_name == "Students by Section":
            section_id, ok = QInputDialog.getText(self, self.tr("Input"), self.tr("Enter Section ID:"))
            if ok and section_id:
                params = section_id.strip()
            else:
                return
                
        elif query_name == "Instructor Timetable":
            inst_id, ok = QInputDialog.getInt(self, self.tr("Input"), self.tr("Enter Instructor ID:"))
            if ok:
                params = inst_id
            else:
                return

        try:
            headers, data = db.execute_query(query_name, params)
            self._display_results(headers, data)
            
            self.state.setText(self.tr("Success ") + f"{len(data)}" +self.tr ("rows"))
            logger.info(f"Executed query: {query_name}")
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            self.state.setText(self.tr("Error"))
            QMessageBox.critical(self, self.tr("Error"), self.tr("Failed to execute query:") +f" {e}")

    #* Display query results in the table
    def _display_results(self, headers, data):
       
        #* Setup columns
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        #* Stretch all columns
        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        
        #* Clear and populate rows
        self.table.setRowCount(0)
        
        for row_idx, row_data in enumerate(data):
            self.table.insertRow(row_idx)
            
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        
        logger.debug(f"Displayed {len(data)} rows in table")