from PyQt6.QtGui import QPixmap, QBrush, QPainter, QFont
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QLabel, QPushButton, QMainWindow, QWidget, QVBoxLayout
from go import Go
from menu import Menu
from custom_button import CustomButton as button


class Start(QMainWindow):
    def __init__(self):
        super().__init__()
        self.go_window=None
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        lbl_title = QLabel("Go Game", self)

        # resize the text size
        font = QFont()
        font.setPointSize(20)
        lbl_title.setFont(font)

        # create a label that show the picture
        lbl_picture = QLabel(self)
        lbl_picture.setPixmap(QPixmap("./icon/goPict.jpeg"))

        btn = button('Click to launch game !', "rgb(212, 177, 147)")
        btn.setFixedSize(200,35)

        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_picture.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_picture)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        #btn.clicked.connect(self.launchGame)
        btn.clicked.connect(self.launchMenu)

        central_widget.setLayout(layout)
        self.setWindowTitle('Start Game')
        self.show()

    def drawWoodGrainBackground(self, painter):
        # Load a wood texture image
        wood_texture = QPixmap("./icon/woods.jpg")  # Replace with the path to your wood texture image

        # Create a brush with the wood texture
        brush = QBrush(wood_texture)
        painter.fillRect(self.rect(), brush)

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)

        self.drawWoodGrainBackground(painter)
        self.update()

    def launchMenu(self):
        self.hide()
        if not self.go_window:
            self.go_window = Menu()

        self.go_window.show()
    def launchGame(self):
        myGo = Go()
        myGo.show()
        self.hide()
