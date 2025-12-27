
#& Imports

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QWidget, QHeaderView, QLabel, QLineEdit,
    QGridLayout, QTableWidgetItem
)

import logging

logger = logging.getLogger(__name__)


#* Path to ui file for the crud
PATH_TO_UI = "Application/GUI/UI/CRUD.ui"


class BaseCRUD(QWidget):
    def __init__(self, headers):
        super().__init__()
        uic.loadUi(PATH_TO_UI, self)

        self.headers = headers

        logger.debug(f"BaseCRUD initialized with headers: {self.headers}")

        self.inputs = {} 

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

    #* Load the Selected rows in the bottom
    def _load_selected_row(self):

        row = self.table.currentRow()
        self._enable_buttons()
        if row < 0:
            return

        for col, header in enumerate(self.headers):
            item = self.table.item(row, col)
            self.inputs[header].setText(item.text() if item else "")

            self.save_btn.setEnabled(False)
            self.update_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
            self.clear_btn.setEnabled(True)
        logger.debug(f"Row {row} selected for editing")


    #* Insert the values to the table from the existing db
    def populate_table(self, rows:list[tuple]):
        
        #* Clear rows
        self.table.setRowCount(0)  
        
        for row_idx,row_data in enumerate(rows):
            
            self.table.insertRow(row_idx)
        
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_idx, col_idx, item)

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
            self.inputs[header].clear()

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
            self.inputs[header].clear()

        self.table.blockSignals(False)

        self._disable_buttons()

        logger.debug("Form cleared and selection reset")


    def _save_new(self):

        logger.info("Save requested for new row")

        #* Insert a new empty row at the end
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)

        row_data=[]

        #* Fill the row with data from inputs
        for col_idx, line_input in enumerate(self.input_list):
            value = line_input.text()

            row_data.append(value)
            #* Validate value (place holder) 
            item = QTableWidgetItem(value)
            self.table.setItem(row_idx, col_idx, item)

        #* Call insert to db function

        #* Clear the form for next entry
        for line_input in self.input_list:
            line_input.setText("")

        #* Enable the table and buttons
        self._clear_form()
        self.table.setEnabled(True)
        self._enable_buttons()

        logger.info(f"New row inserted at index {row_idx}")
        logger.debug(f"Inserted row data: {row_data}", )


    def _update_row(self):
        
        
        row = self.table.currentRow()
        logger.info(f"Update requested for row {row}")

        if row < 0:
            return

        #* Validate value (place holder) 
        updated_data = []

        for col_idx, line_input in enumerate(self.input_list):
            value = line_input.text().strip()
            updated_data.append(value)

            self.table.setItem(row, col_idx, QTableWidgetItem(value))
        
        logger.info(f"Row {row} updated successfully")
        logger.debug(f"Updated row data: {updated_data}")

        #* Call insert to db function to update insert

    def _delete_row(self):

        row = self.table.currentRow()
        if row < 0:
            return

        self.table.removeRow(row)

        logger.warning(f"Row {row} deleted by user action")

        #* Call insert to db function to update insert

        self._clear_form()

        

        


