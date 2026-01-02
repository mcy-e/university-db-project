from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout,QWidget,
    QHBoxLayout,QPushButton,QSizePolicy,
    QGridLayout,QLabel, QScrollArea)


class CRUDMenuScreen(QWidget):

    #* Create Signals
    navigate_to_student_crud=pyqtSignal()
    navigate_to_instructor_crud = pyqtSignal()
    navigate_to_course_crud = pyqtSignal()
    navigate_to_department_crud = pyqtSignal()
    navigate_to_room_crud = pyqtSignal()
    navigate_to_reservation_crud = pyqtSignal()
    navigate_to_enrollment_crud = pyqtSignal()
    navigate_to_mark_crud = pyqtSignal()
    navigate_to_activity_crud = pyqtSignal()
    navigate_to_exam_crud = pyqtSignal()
    navigate_to_attendance_crud = pyqtSignal()
    go_back=pyqtSignal()



    def __init__(self):
        super().__init__()


        #* Create BoxLayout instance
        layout= QVBoxLayout()
        layout.addSpacing(10)
        layout.setContentsMargins(20,20,20,20)
        

        #* Create the the parent which holds everything
        holder=QVBoxLayout()
        holder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(holder)
        
        #* Add the top bar and Crud menu buttons
        holder.addLayout(TopBar(self),stretch=1)
        holder.addWidget(CRUDMenuButtons(self),stretch=4)
        

        #* Set the layout for the widget
        self.setLayout(layout)


class TopBar(QHBoxLayout):
    def __init__(self,parent_screen):
        super().__init__()

        self.parent_screen=parent_screen

        #* Push button instance
        # TODO : Change the text and instead use an icon
        btn=QPushButton("<")

        #* Label instance for the title
        title=QLabel("CRUD MENU")

        #* Size policy
        btn.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Expanding)

        
        #* Fixed width for the button so it doesn't go beyond it 
        btn.setFixedWidth(60)
        
        #* Connecting the signal to the button
        btn.clicked.connect(self.parent_screen.go_back.emit)
        
        #* Adding the btn to the Layout with aligning it on top
        self.addWidget(btn,alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft,stretch=1)

        #* Adding the label to the Layout 
        self.addWidget(title,alignment= Qt.AlignmentFlag.AlignCenter,stretch=2)

class CRUDMenuButtons(QWidget):
    def __init__(self,parent_screen):
        super().__init__()
        self.parent_screen=parent_screen

        #* Create Main Layout instance
        layout=QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #* Create Scroll View instance
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        #* Create container to hold the layout
        container = QWidget()
        scroll.setWidget(container)

        #* Create the grid layout
        grid = QGridLayout(container)
        grid.setSpacing(10)

        self._create_buttons(grid)
        
        layout.addWidget(scroll)




        
    def _create_buttons(self,widget:object):
            
            #* Text & signals to put on buttons (don't judge the ui for now we still not focusing on style)
            button_data = [
                ("Student CRUD", self.parent_screen.navigate_to_student_crud),
                ("Instructor CRUD", self.parent_screen.navigate_to_instructor_crud),
                ("Course CRUD", self.parent_screen.navigate_to_course_crud),
                ("Department CRUD", self.parent_screen.navigate_to_department_crud),
                ("Room CRUD", self.parent_screen.navigate_to_room_crud),
                ("Reservation CRUD", self.parent_screen.navigate_to_reservation_crud),
                ("Enrollment CRUD", self.parent_screen.navigate_to_enrollment_crud),
                ("Mark CRUD", self.parent_screen.navigate_to_mark_crud),
                ("Activity CRUD", self.parent_screen.navigate_to_activity_crud),
                ("Exam CRUD", self.parent_screen.navigate_to_exam_crud),
                ("Attendance CRUD", self.parent_screen.navigate_to_attendance_crud),
            ]

            
            #* Number of columns 
            columns_num=3
            
            for i,(text,signal) in enumerate(button_data):
                
                row = i // columns_num
                col = i%columns_num
                
                #* Push button instance
                btn = QPushButton(text)
                
                #* Setting size policy to handle the hight and make width responsive (stretching with the screen)   
                btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

                #* Range of manual hight sizing
                btn.setMinimumSize(100, 100)

                #* Connecting signals to buttons
                btn.clicked.connect(signal.emit)

                #* Adding the btn to the Grid
                widget.addWidget(btn, row, col)

        
