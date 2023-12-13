from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from custom_button import CustomButton as button
from board import Board


class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''

    passButtonClicked = pyqtSignal()
    resignButtonClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.setWindowTitle('ScoreBoard')

        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # create two labels which will be updated by signals
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")

        # create 2 buttons to skip turn and resign
        self.skip = button("PASS")

        self.resignBtn = button("RESIGN")

        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.mainLayout.addWidget(self.skip)
        self.mainLayout.addWidget(self.resignBtn)
        self.setWidget(self.mainWidget)

        self.skip.clicked.connect(self.skip_clicked)
        self.resignBtn.clicked.connect(self.resign_clicked)


    def skip_clicked(self):
        self.passButtonClicked.emit()

    def resign_clicked(self):
        self.resignButtonClicked.emit()

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)

    @pyqtSlot(str)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location: " + clickLoc)
        print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemaining):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining: " + str(timeRemaining)
        self.label_timeRemaining.setText(update)
        print('slot ' + str(timeRemaining))
        # self.redraw()