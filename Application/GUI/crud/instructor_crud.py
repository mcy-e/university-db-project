from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal

from PyQt6.QtWidgets import QComboBox, QLabel, QLineEdit, QGridLayout, QWidget
from .base_crud import BaseCRUD

from Database import database  as db 


class InstructorCRUD(BaseCRUD):

    
    #* Create Back Signal
    go_back=pyqtSignal()

    def __init__(self):

        db_operations = {
        'add': db.add_instructor,
        'update': db.update_instructor,
        'delete': db.delete_instructor,
        }
        
        header=["Instructor_ID", "Department_ID", "Last_Name", "First_Name", "Rank", "Phone", "Fax", "Email"]
        super().__init__(header,db_operations)
        
        self.populate_table(db.get_all_instructors())
        self.back_btn.clicked.connect(self.go_back.emit)


    def _is_id_field(self, header):
        return header == "Instructor_ID"

    #* Override to add dropdown for Rank
    def _build_form(self):

        
        container = QWidget()
        layout = QGridLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(10)

        self.input_list = []

        for row, header in enumerate(self.headers):
            label = QLabel(header)
            
            #* Special case for Rank
            if header == "Rank":
                input_widget = QComboBox()
                input_widget.addItems(['Substitute', 'MCB', 'MCA', 'PROF'])
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

