from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from custom_button import CustomButton as button
from rules import Rules


class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''

    passButtonClicked = pyqtSignal()
    resignButtonClicked = pyqtSignal()
    updateBlackCaptureSignal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.go_window = None
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.setWindowTitle('ScoreBoard')

        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # create two labels which will be updated by signals
        # self.label_clickLocation = QLabel("Click Location: ")
        # self.label_timeRemaining = QLabel("Time remaining: ")
        self.lbl_black = QLabel("Black player:")
        self.lbl_black_captured = QLabel("\n- number of stones captured: 0")
        self.lbl_black_territory = QLabel("\n- territories: ")

        self.lbl_white = QLabel("White player:")
        self.lbl_white_captured = QLabel("\n- number of stones captured: 0")
        self.lbl_white_territory = QLabel("\n- territories: ")

        # create buttons to display rules, skip turn and resign
        self.skipBtn = button("PASS")
        self.resignBtn = button("RESIGN")
        self.rulesBtn = button("See the rules")

        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.rulesBtn)
        self.mainLayout.addWidget(self.lbl_black)
        self.mainLayout.addWidget(self.lbl_black_captured)
        self.mainLayout.addWidget(self.lbl_white)
        self.mainLayout.addWidget(self.lbl_white_captured)
        self.mainLayout.addWidget(self.skipBtn)
        self.mainLayout.addWidget(self.resignBtn)
        self.setWidget(self.mainWidget)

        self.rulesBtn.clicked.connect(self.rules_clicked)
        self.skipBtn.clicked.connect(self.skip_clicked)
        self.resignBtn.clicked.connect(self.resign_clicked)

    def rules_clicked(self):
        if not self.go_window:
            self.go_window = Rules()

        self.go_window.show()

    def skip_clicked(self):
        self.passButtonClicked.emit()

    def resign_clicked(self):
        self.resignButtonClicked.emit()

    def update_lbl_black_captured(self, value):
        '''print("val back capture" + str(value))
        self.lbl_black_captured.setText("\n- number of stones captured: " + str(value))
        self.show()
        print("emit")'''
        self.updateBlackCaptureSignal.emit(value)

    def update_lbl_white_captured(self, value):
        print("val white captured" + str(value))
        self.lbl_white_captured.setText("\n- number of stones captured: " + str(value))



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
