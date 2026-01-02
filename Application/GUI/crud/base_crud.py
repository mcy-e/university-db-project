
#& Imports

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QWidget, QHeaderView, QLabel, QLineEdit,
    QGridLayout, QTableWidgetItem
)

from Database import database as db

from UTILS import constriants

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
            
            #* Create labels with there line edit object
            label = QLabel(header)
            line_edit = QLineEdit()
            
            #* Make ID fields read-only and visually distinct
            if self._is_id_field(header):
                line_edit.setReadOnly(True)
                line_edit.setStyleSheet("QLineEdit { background-color: #f0f0f0; color: #666; }")
                line_edit.setPlaceholderText("Auto-generated")

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
            if not line_edit.isReadOnly(): 
                line_edit.returnPressed.connect(
                    lambda le=line_edit, idx=i: self._focus_next(idx)
                )
        logger.debug(f"Form input created for fields")

    def _focus_next(self, idx):

        #* Move focus to next editable input field, loop back to first when the end is reached
        next_idx = (idx + 1) % len(self.input_list)
        
        #* Skip read-only fields
        attempts = 0
        while self.input_list[next_idx].isReadOnly() and attempts < len(self.input_list):
            next_idx = (next_idx + 1) % len(self.input_list)
            attempts += 1
        
        if not self.input_list[next_idx].isReadOnly():
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
        field_dict = {}

        #* Collect only non-ID field values for insertion AND build validation dict
        for line_input, header in zip(self.input_list, self.headers):
            if not self._is_id_field(header):
                value = self._get_input_value(line_input)
                row_data.append(value)
                field_dict[header] = value

        #* VALIDATE BEFORE SAVING
        is_valid, errors = constriants.validate_all_fields(field_dict)
        if not is_valid:
            error_msg = "\n".join(errors)
            logger.error(f"Validation failed: {error_msg}")
            # TODO: Show QMessageBox to user
            return

        #* Call database insert function
        try:
            result = self.db_operations['add'](*row_data)
            if not result:
                logger.error("Database insert failed")
                return
            
            #* If result is tuple (success, new_id), extract the new ID
            if isinstance(result, tuple) and result[0]:
                new_id = result[1]
            else:
                #* Placeholder if DB doesn't return ID
                new_id = "Auto"  
                
        except Exception as e:
            logger.error(f"Error saving new row: {e}")
            return

        #* Insert into table UI with all fields including IDs
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)
        
        #* Build complete row data with IDs
        full_row_data = []
        data_idx = 0
        for header in self.headers:
            if self._is_id_field(header):
                full_row_data.append(str(new_id))
            else:
                full_row_data.append(str(row_data[data_idx]))
                data_idx += 1
        
        #* Add all data to table
        for col_idx, value in enumerate(full_row_data):
            item = QTableWidgetItem(str(value))
            self.table.setItem(row_idx, col_idx, item)

        #* Clear the form for next entry
        for line_input in self.input_list:
            if not line_input.isReadOnly():
                self._set_input_value(line_input, "")

        #* Enable the table and buttons
        self._clear_form()
        self.table.setEnabled(True)
        self._enable_buttons()

        logger.info(f"New row inserted at index {row_idx} with ID {new_id}")
        logger.debug(f"Inserted row data: {row_data}")


    def _update_row(self):
        
        row = self.table.currentRow()
        logger.info(f"Update requested for row {row}")

        if row < 0:
            return

        #* Collect ALL field values (including IDs for update) AND validate
        updated_data = []
        field_dict = {}

        for line_input, header in zip(self.input_list, self.headers):
            value = self._get_input_value(line_input).strip()
            updated_data.append(value)
            
            #* Add non-ID fields to validation dict
            if not self._is_id_field(header):
                field_dict[header] = value

        #* VALIDATE BEFORE UPDATING
        is_valid, errors = constriants.validate_all_fields(field_dict)
        if not is_valid:
            error_msg = "\n".join(errors)
            logger.error(f"Validation failed: {error_msg}")
            # TODO: Show QMessageBox to user
            return

        #* Call database update function
        try:
            success = self.db_operations['update'](*updated_data)
            if not success:
                logger.error("Database update failed")
                return
            
            #* Update was successful, now update the table UI
            for col_idx, value in enumerate(updated_data):
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

    def _is_id_field(self, header):
       #* Check if a header represents is an ID
        return header.endswith('_ID') or header == 'ID' or 'ID' in header.split('_') or 'ID' in header.strip()

        


