from PyQt6.QtGui import QPixmap, QBrush, QPainter, QFont, QIcon
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QLabel, QPushButton, QMainWindow, QWidget, QVBoxLayout, QApplication
from go import Go
from custom_button import CustomButton as button


class Start(QMainWindow):
    def __init__(self):
        super().__init__()
        self.go_window=None
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.setWindowIcon(QIcon("./icon/goo.png"))

        layout = QVBoxLayout()

        lbl_title = QLabel("Go Game", self)
        self.setGeometry(200, 200, 800, 600)

        # resize the text size
        font = QFont()
        font.setPointSize(50)
        lbl_title.setFont(font)

        # create a label that show the picture
        lbl_picture = QLabel(self)
        lbl_picture.setPixmap(QPixmap("./icon/goPict.jpeg"))

        btn = button('Click to launch game !', "rgb(212, 177, 147)")
        btn.setFixedSize(200,80)

        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_picture.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_picture)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        #btn.clicked.connect(self.launchGame)
        btn.clicked.connect(self.launch)

        #self.go.homeButtonClicked.connect(self.showWind)

        central_widget.setLayout(layout)
        self.setWindowTitle('Start Game')
        self.center()
        self.show()

    def draw_wood_grain_background(self, painter):
        # Load a wood texture image
        wood_texture = QPixmap("./icon/woods.jpg")  # Replace with the path to your wood texture image

        # Create a brush with the wood texture
        brush = QBrush(wood_texture)
        painter.fillRect(self.rect(), brush)

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)

        self.draw_wood_grain_background(painter)
        self.update()

    def launch(self):
        self.hide()
        if not self.go_window:
            self.go_window = Go()
            self.go_window.homeButtonClicked.connect(self.showWind)
        self.go_window.show()

    def showWind(self):
        self.show()

    def center(self):
        '''Centers the window on the screen'''
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)