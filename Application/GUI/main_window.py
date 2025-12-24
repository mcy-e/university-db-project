"""
    Application.GUI.main_window
    Contains main window layout with:
    Navigation grid (6 buttons)
    Top bar (menu + title)
    Settings button

"""
    


#& imports
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QGridLayout,
    QLabel,
    QSpacerItem)

#* Main Window class
class MainWindow (QMainWindow):
    def __init__(self):
        super().__init__()
        #* Window Title
        self.setWindowTitle("UniversityManagement")
        
        #* Window Min Size
        self.setMinimumSize(600, 600)


        #* Create BoxLayout instance
        layout= QVBoxLayout()
        layout.addSpacing(10)
        layout.setContentsMargins(20,10,20,10)
        
        #* Create widget instance
        widget=QWidget()

        #* Create the the parent which holds everything
        holder=QVBoxLayout()
        holder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(holder)
        
        #* Add the elements (top bar, button grid,settings button)
        
        holder.addLayout(TopBar(),stretch=1)        
        holder.addLayout(ButtonsGrid(),stretch=2)
        holder.addLayout(SettingsButton(),stretch=1)
        

        #* Set the layout for the widget
        widget.setLayout(layout)

        #* Set the Main Widget for the Main Window
        self.setCentralWidget(widget)

class ButtonsGrid(QGridLayout):
    def __init__(self):
        super().__init__()

        #* Setting alignment
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        #* Add Spacing
        self.setSpacing(10)

        #* Columns and Rows for the Grid layout to configure it
        positions = [
            (0, 0), (0, 1),
            (1, 0), (1, 1),
            (2, 0), (2, 1)
        ]

        #* Text to put on buttons (don't judge the ui for now we still not focusing on style)
        btn_text=[
            "CRUD Operations",
            "Academic Management",
            "Student Performance",
            "Results Processing",
            "Query Results",
            "Audit Log"
        ]
        for i,(row,col) in enumerate(positions):

            #* Push button instance
            btn=QPushButton(btn_text[i])

            #* Setting size policy to handle the hight and make width responsive (stretching with the screen)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Fixed)
            
            #* Range of manual hight sizing
            btn.setMinimumHeight(100)
            btn.setMaximumHeight(200)

            #* Adding the btn to the Grid
            self.addWidget(btn,row,col)
        
class SettingsButton(QHBoxLayout):
    def __init__(self):
        super().__init__()

        #* Setting alignment
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        #* Padding
        self.setContentsMargins(10,10,10,10)

        #* Push button instance
        btn=QPushButton("Settings")
    
        #* Size Policies
        btn.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
        
        #* Manual Hight Sizing Range
        btn.setMinimumHeight(60)
        btn.setMaximumHeight(70)

        #* Manual Width Sizing Range
        btn.setMinimumWidth(400)
        btn.setMaximumWidth(800)

        #* Adding the btn to the Layout
        self.addWidget(btn)

class TopBar(QHBoxLayout):
    def __init__(self):
        super().__init__()

        #* Push button instance
        # TODO : Change the text and instead use an icon
        btn=QPushButton("☰")

        #* Label instance for the title
        title=QLabel("University Management System")
        
        #* Fixed width for the button so it doesn't go beyond it 
        btn.setFixedWidth(80)

        #* Size policy
        btn.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Expanding)
        
        #* Adding the btn to the Layout with aligning it on top
        self.addWidget(btn,alignment=Qt.AlignmentFlag.AlignTop)

        #* Adding the label to the Layout 
        self.addWidget(title,alignment=Qt.AlignmentFlag.AlignCenter)


        
