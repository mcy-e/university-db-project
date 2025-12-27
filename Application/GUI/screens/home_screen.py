

from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout,QWidget,
    QHBoxLayout,QPushButton,QSizePolicy,
    QGridLayout,QLabel,)

class HomeScreen(QWidget):

    #* Signals for navigation
    navigate_to_crud = pyqtSignal()
    navigate_to_academic = pyqtSignal()
    navigate_to_performance = pyqtSignal()
    navigate_to_results = pyqtSignal()
    navigate_to_queries = pyqtSignal()
    navigate_to_audit = pyqtSignal()
    navigate_to_settings=pyqtSignal()
    open_side_bar=pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()

        #* Create BoxLayout instance
        layout= QVBoxLayout()
        layout.addSpacing(10)
        layout.setContentsMargins(20,10,20,10)
        

        #* Create the the parent which holds everything
        holder=QVBoxLayout()
        holder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(holder)
        
        #* Add the elements (top bar, button grid,settings button)
        
        holder.addLayout(TopBar(self),stretch=1)        
        holder.addLayout(ButtonsGrid(self),stretch=2)
        holder.addLayout(SettingsButton(self),stretch=1)
        

        #* Set the layout for the widget
        self.setLayout(layout)



class ButtonsGrid(QGridLayout):
    def __init__(self,parent_screen):
        super().__init__()

        self.parent_screen=parent_screen
        #* Setting alignment
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        #* Add Spacing
        self.setSpacing(10)

        #* Create Buttons
        self._create_buttons()
    
    
    def _create_buttons(self):
            
            #* Text & signals to put on buttons (don't judge the ui for now we still not focusing on style)
            button_data = [
                ("CRUD Operations", self.parent_screen.navigate_to_crud),
                ("Academic Management", self.parent_screen.navigate_to_academic),
                ("Student Performance", self.parent_screen.navigate_to_performance),
                ("Results Processing", self.parent_screen.navigate_to_results),
                ("Query Results", self.parent_screen.navigate_to_queries),
                ("Audit Log", self.parent_screen.navigate_to_audit),
            ]
            
            #* Columns and Rows for the Grid layout to configure it
            positions = [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1)]
            
            for (row, col), (text, signal) in zip(positions, button_data):
                
                #* Push button instance
                btn = QPushButton(text)
                
                #* Setting size policy to handle the hight and make width responsive (stretching with the screen)   
                btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

                #* Range of manual hight sizing
                btn.setMinimumHeight(100)
                btn.setMaximumHeight(200)

                #* Connecting signals to buttons
                btn.clicked.connect(signal.emit)

                #* Adding the btn to the Grid
                self.addWidget(btn, row, col)

class SettingsButton(QHBoxLayout):
    def __init__(self,parent_screen):
        super().__init__()

        self.parent_screen=parent_screen

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

        btn.clicked.connect(self.parent_screen.navigate_to_settings.emit)

        #* Adding the btn to the Layout
        self.addWidget(btn)

class TopBar(QHBoxLayout):
    def __init__(self,parent_screen):
        super().__init__()

        self.parent_screen=parent_screen

        #* Push button instance
        # TODO : Change the text and instead use an icon
        btn=QPushButton("☰")

        #* Label instance for the title
        title=QLabel("University Management System")
        
        #* Fixed width for the button so it doesn't go beyond it 
        btn.setFixedWidth(80)

        #* Size policy
        btn.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Expanding)
        
        #* Connecting the signal to the button
        btn.clicked.connect(self.parent_screen.open_side_bar.emit)
        
        #* Adding the btn to the Layout with aligning it on top
        self.addWidget(btn,alignment=Qt.AlignmentFlag.AlignTop)

        #* Adding the label to the Layout 
        self.addWidget(title,alignment=Qt.AlignmentFlag.AlignCenter)


        
