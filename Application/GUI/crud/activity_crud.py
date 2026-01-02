from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal

from PyQt6.QtWidgets import QComboBox, QLabel, QLineEdit, QGridLayout, QWidget
from .base_crud import BaseCRUD

from Database import database as db

DATA=db.get_all_activities()

class ActivityCRUD(BaseCRUD):

    
    #* Create Back Signal
    go_back=pyqtSignal()

    def __init__(self):
        db_operations = {
            'add': db.add_activity,
            'update': db.update_activity,
            'delete': db.delete_activity,
        }
        header=["Activity_ID", "Activity_Type", "Reservation_ID", "Course_ID", "Department_ID"]
        super().__init__(header, db_operations)

        self.populate_table(DATA)
        self.back_btn.clicked.connect(self.go_back.emit)

    #* Override to add dropdown for Activity_Type
    def _build_form(self):
        
        container = QWidget()
        layout = QGridLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(10)

        self.input_list = []

        for row, header in enumerate(self.headers):
            label = QLabel(header)
            
            #* Special case for Activity_Type
            if header == "Activity_Type":
                input_widget = QComboBox()
                input_widget.addItems(['lecture', 'tutorial', 'practical'])
                input_widget.setEditable(False)
            else:
                input_widget = QLineEdit()
            
            layout.addWidget(label, row, 0)
            layout.addWidget(input_widget, row, 1)
            
            self.inputs[header] = input_widget
            self.input_list.append(input_widget)

        self.scrollArea.setWidget(container)
        self.scrollArea.setWidgetResizable(True)
        

        for i, input_widget in enumerate(self.input_list):
            if isinstance(input_widget, QLineEdit):
                input_widget.returnPressed.connect(
                    lambda idx=i: self._focus_next(idx)
                )