
#& Imports

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QWidget, QHeaderView, QLabel, QLineEdit,
    QGridLayout, QTableWidgetItem
)

from Database import database as db

import logging

logger = logging.getLogger(__name__)


#* Path to ui file for the crud
PATH_TO_UI = "Application/GUI/UI/CRUD.ui"

# TODO : Change the way of getting all data and make it dynamic in the base class

class BaseCRUD(QWidget):
    def __init__(self, headers:list, db_operations:dict):
        super().__init__()
        uic.loadUi(PATH_TO_UI, self)

        self.headers = headers
        logger.debug(f"BaseCRUD initialized with headers: {self.headers}")


        self.all_rows_data = []  
        self.inputs = {} 
        self.db_operations = db_operations

        self._setup_table()
        self._build_form()
        self._connect_signals()
        self._disable_buttons()

    #* Setup the table depending on columns
    def _setup_table(self):

        #* Set the columns and there labels respectively
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)

        #* Stretching the table
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        #* Ignore Row indexes
        self.table.verticalHeader().setVisible(False)

        #* Start with empty table (no rows)
        self.table.setRowCount(0)

        #* Selecting rows only
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(self.table.SelectionMode.SingleSelection)

        logger.info(f"Table initialized with {len(self.headers)} columns" )

    #* Helper to get the input wether from combo box or edit line
    def _get_input_value(self, input_widget):
        if hasattr(input_widget, 'currentText'):  
            return input_widget.currentText()
        else:  
            return input_widget.text()

    #* Helper to set the input wether from combo box or edit line
    def _set_input_value(self, input_widget, value):
        if hasattr(input_widget, 'setCurrentText'):  
            input_widget.setCurrentText(value)
        else:  
            input_widget.setText(value)


    def _build_form(self):

        #* Create container widget for scroll area
        container = QWidget()
        layout = QGridLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(10)

        self.input_list = []  

        for row, header in enumerate(self.headers):
            
            #* Create labels with there line dit object
            label = QLabel(header)
            line_edit = QLineEdit()

            #* Add them to the layout 
            layout.addWidget(label, row, 0)
            layout.addWidget(line_edit, row, 1)

            #* Save the object instances for handling logic later
            self.inputs[header] = line_edit

            self.input_list.append(line_edit)

        #* Set container to scroll area
        self.scrollArea.setWidget(container)
        self.scrollArea.setWidgetResizable(True)
        for i, line_edit in enumerate(self.input_list):
            line_edit.returnPressed.connect(
                lambda le=line_edit, idx=i: self._focus_next(idx)
            )
        logger.debug(f"Form input created for field: {header}")


    def _focus_next(self, idx):

        #* Move focus to next input field  loop back to first when the end is reached
        next_idx = (idx + 1) % len(self.input_list)
        self.input_list[next_idx].setFocus()


    #* Connect signals
    def _connect_signals(self):
        self.table.itemSelectionChanged.connect(self._load_selected_row)
        self.add_btn.clicked.connect(self._add_new_to_table)
        self.clear_btn.clicked.connect(self._clear_form)
        self.save_btn.clicked.connect(self._save_new)
        self.update_btn.clicked.connect(self._update_row)
        self.delete_btn.clicked.connect(self._delete_row)
        self.search_box.textChanged.connect(self._search_table)

    #* Load the Selected rows in the bottom
    def _load_selected_row(self):

        row = self.table.currentRow()
        self._enable_buttons()
        if row < 0:
            return

        for col, header in enumerate(self.headers):
            item = self.table.item(row, col)
            self._set_input_value(self.inputs[header], item.text() if item else "")

            self.save_btn.setEnabled(False)
            self.update_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
            self.clear_btn.setEnabled(True)
        logger.debug(f"Row {row} selected for editing")


    #* Insert the values to the table from the existing db
    def populate_table(self, rows:list[tuple]):
        
        #* Store all rows for searching
        self.all_rows_data = rows.copy()
        
        #* Clear rows
        self.table.setRowCount(0)  
        
        for row_idx,row_data in enumerate(rows):
            
            self.table.insertRow(row_idx)
        
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_idx, col_idx, item)
        
        logger.info(f"Table of {__class__.__name__} got populated with {self.table.rowCount()}")

    def _disable_buttons(self):
        
        self.save_btn.setEnabled(False)
        self.update_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
    
    def _enable_buttons(self):
        
        self.save_btn.setEnabled(True)
        self.update_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)


    def _add_new_to_table(self):

        self.table.blockSignals(True)
        self.table.clearSelection()
        self.table.setCurrentCell(-1, -1)
        self.table.blockSignals(False)

        self.table.setEnabled(False)

        for header in self.headers:
            self._set_input_value(self.inputs[header], "")

        #* Enable editing buttons
        self.save_btn.setEnabled(True)
        self.update_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.clear_btn.setEnabled(True)

        logger.info("Add-new mode activated: table disabled, selection cleared")


    def _clear_form(self):
    
        self.table.blockSignals(True)

        self.table.clearSelection()
        self.table.setCurrentCell(-1, -1)

        for header in self.headers:
            self._set_input_value(self.inputs[header], "")

        self.table.blockSignals(False)

        self._disable_buttons()

        logger.debug("Form cleared and selection reset")


    def _save_new(self):

        logger.info("Save requested for new row")

        row_data = []

        #* Determine starting index (skip ID if auto-increment)
        start_idx = 1 if self._should_skip_first_field() else 0

        #* Fill the row with data from inputs (skip first field if needed)
        for col_idx in range(start_idx, len(self.input_list)):
            value = self._get_input_value(self.input_list[col_idx])
            row_data.append(value)

        #* Call database insert function
        try:
            result = self.db_operations['add'](*row_data)
            if not result:
                logger.error("Database insert failed")
                return
            
            #* If result is tuple (success, new_id), use the new_id
            if isinstance(result, tuple) and result[0]:
                new_id = result[1]
            else:
                new_id = self._get_input_value(self.input_list[0]) if not self._should_skip_first_field() else "N/A"
                
        except Exception as e:
            logger.error(f"Error saving new row: {e}")
            return

        #* Insert into table UI with actual ID
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)
        
        #* Add ID to first column
        self.table.setItem(row_idx, 0, QTableWidgetItem(str(new_id)))
        
        #* Add the rest of the data
        for col_idx, value in enumerate(row_data, start=1):
            item = QTableWidgetItem(str(value))
            self.table.setItem(row_idx, col_idx, item)

        #* Clear the form for next entry
        for line_input in self.input_list:
            self._set_input_value(line_input, "")

        #* Enable the table and buttons
        self._clear_form()
        self.table.setEnabled(True)
        self._enable_buttons()

        logger.info(f"New row inserted at index {row_idx}")
        logger.debug(f"Inserted row data: {row_data}")

    def _update_row(self):
        
        
        row = self.table.currentRow()
        logger.info(f"Update requested for row {row}")

        if row < 0:
            return

        #* Validate value (place holder) 
        updated_data = []

        for col_idx, line_input in enumerate(self.input_list):
            value = self._get_input_value(line_input).strip()
            updated_data.append(value)



        #* Call insert to db function to update insert
        try:
            success = self.db_operations['update'](*updated_data)
            if not success:
                logger.error("Database update failed")
            else:
                for col_idx, line_input in enumerate(updated_data):
                    self.table.setItem(row, col_idx, QTableWidgetItem(value))
            
                logger.info(f"Row {row} updated successfully")
                logger.debug(f"Updated row data: {updated_data}")

        except Exception as e:
            logger.error(f"Error updating row: {e}")

    def _delete_row(self):

        row = self.table.currentRow()
        if row < 0:
            return

        #* Get the ID from first column for deletion
        id_value = self.table.item(row, 0).text()

        #* Call database delete function
        try:
            success = self.db_operations['delete'](id_value)
            if not success:
                logger.error("Database delete failed")
                return 
        except Exception as e:
            logger.error(f"Error deleting row: {e}")
            return
        self.table.removeRow(row)
        logger.warning(f"Row {row} deleted by user action")
        self._clear_form()


    def _search_table(self):
        
        search_text = self.search_box.text().strip().lower()
        
        logger.info(f"Search initiated with query: '{search_text}'")
        
        if not search_text:
            
            #* Show all data for empty search
            self.populate_table(self.all_rows_data)
            logger.debug("Search cleared....,showing all rows")
            return
        
        #* Filter rows that match the text box
        filtered_rows = []
        for row_data in self.all_rows_data:
            #* Check if the text exists in any column of this row
            if any(search_text in str(value).lower() for value in row_data):
                filtered_rows.append(row_data)
        
        #* Clear table and populate with filtered results
        self.table.setRowCount(0)

        for row_idx, row_data in enumerate(filtered_rows):
        
            self.table.insertRow(row_idx)
        
            for col_idx, value in enumerate(row_data):
        
                item = QTableWidgetItem(str(value))
        
                self.table.setItem(row_idx, col_idx, item)
        
        logger.info(f"Search complete, {len(filtered_rows)} rows match '{search_text}'")

    def _skip_first_field(self):
        """
        Check if first field should be skipped (for auto-increment IDs)
        Override in child classes if needed
        """
        return False


        

        


