#& Imports

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QHeaderView, QTableWidgetItem, QMessageBox
)

from Database import database as db

import logging

logger = logging.getLogger(__name__)

#* Path to ui file for query viewer
PATH_TO_UI = "Application/GUI/UI/query_viewer.ui"

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
        self.query_selection.addItem("Select Query")
        
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
            QMessageBox.warning(self, "Validation Error", "Please select a query")
            return
        
        query_name = self.query_selection.currentText()
        
        try:
            headers, data = db.execute_query(query_name)
            self._display_results(headers, data)
            
            self.state.setText(f"Success - {len(data)} rows")
            logger.info(f"Executed query: {query_name}")
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            self.state.setText("Error")
            QMessageBox.critical(self, "Error", f"Failed to execute query: {e}")

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