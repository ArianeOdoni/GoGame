from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QSpacerItem, QGridLayout, QVBoxLayout, QLabel, \
    QPushButton
from PyQt6.QtCore import Qt

from board import Board
from score_board import ScoreBoard


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''Initiates application UI'''

        self.board = Board(self)
        self.scoreBoard = ScoreBoard()
        self.setCentralWidget(self.board)

        # Set the background color of the QVBoxLayout
        self.setStyleSheet("background-color: rgb(212, 177, 147);")

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        #self.scoreBoard.make_connection(self.board)

        self.scoreBoard.passButtonClicked.connect(self.board.logic.pass_this_turn)
        self.scoreBoard.resignButtonClicked.connect(lambda: self.board.logic.end_of_the_game(resign=True))

        self.scoreBoard.updateBlackCaptureSignal.connect(self.updateBlackCapture)

        self.resize(800, 800)
        self.center()
        self.setWindowTitle('Go')
        self.show()

    def updateBlackCapture(self, value):
        print("eee")
        self.scoreBoard.lbl_black_captured.setText("\n- number of stones captured: " + str(value))

    def center(self):
        '''Centers the window on the screen'''
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)


