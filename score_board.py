from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QPushButton, QSpacerItem
from PyQt6.QtCore import pyqtSlot, pyqtSignal, Qt
from custom_button import CustomButton as button
from rules import Rules


class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''

    passButtonClicked = pyqtSignal()
    resignButtonClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.go_window = None
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.setWindowTitle('ScoreBoard')
        self.setWindowIcon(QIcon("./icon/goo.png"))

        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # create two labels which will be updated by signals
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")

        self.black_box = QVBoxLayout()
        self.white_box = QVBoxLayout()

        self.white_territory = QLabel("White Territory : 0")
        self.black_territory = QLabel("Black Territory : 0")
        self.black_captured = QLabel("Black captured : 0")
        self.white_captured = QLabel("White captured : 0")

        self.black_box.addWidget(self.black_territory, alignment=Qt.AlignmentFlag.AlignBottom)
        self.black_box.addWidget(self.white_captured, alignment=Qt.AlignmentFlag.AlignTop)
        self.white_box.addWidget(self.white_territory, alignment=Qt.AlignmentFlag.AlignBottom)
        self.white_box.addWidget(self.black_captured, alignment=Qt.AlignmentFlag.AlignTop)

        # create 2 buttons to skip turn and resign
        self.skip_btn = button("PASS")
        self.resign_btn = button("RESIGN")
        self.rules_btn = button("")
        self.rules_btn.setIcon((QIcon("./icon/rules.png")))

        self.space = QSpacerItem(1, 100)

        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.rules_btn)
        # self.mainLayout.addWidget(self.label_clickLocation)
        # self.mainLayout.addWidget(self.label_timeRemaining)
        self.mainLayout.addLayout(self.black_box)
        self.mainLayout.addLayout(self.white_box)
        self.mainLayout.addWidget(self.skip_btn)
        self.mainLayout.addWidget(self.resign_btn)
        self.setWidget(self.mainWidget)

        self.rules_btn.clicked.connect(self.rules_clicked)
        self.skip_btn.clicked.connect(self.skip_clicked)
        self.resign_btn.clicked.connect(self.resign_clicked)

    @pyqtSlot(int)
    def update_black_territory(self, territory):
        self.black_territory.setText("Black Territory : " + str(territory))

    @pyqtSlot(int)
    def update_white_territory(self, territory):
        self.white_territory.setText("White Territory : " + str(territory))

    @pyqtSlot(int)
    def update_black_captured(self, captured):
        self.black_captured.setText("Black captured : " + str(captured))

    @pyqtSlot(int)
    def update_white_captured(self, captured):
        self.white_captured.setText("White captured : " + str(captured))

    def skip_clicked(self):
        self.passButtonClicked.emit()

    def resign_clicked(self):
        self.resignButtonClicked.emit()


    def rules_clicked(self):
        if not self.go_window:
            self.go_window = Rules()
        self.go_window.show()

    def hide_buttons(self):
        self.skip_btn.hide()
        self.resign_btn.hide()

    def show_buttons(self):
        self.skip_btn.show()
        self.resign_btn.show()

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
