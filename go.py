from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QSpacerItem, QGridLayout, QVBoxLayout, QLabel, \
    QPushButton, QSlider, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal

from board import Board
from score_board import ScoreBoard
from custom_button import CustomButton as button



class Go(QMainWindow):
    replayModeActivated = pyqtSignal()
    homeButtonClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.go_window = None
        self.initUI()

    def initUI(self):
        # sound = SoundManager()

        '''Initiates application UI'''
        self.board = Board(self)
        self.setCentralWidget(self.board)

        # Set the background color of the QVBoxLayout
        self.setStyleSheet("background-color: rgb(212, 177, 147);")

        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        # self.scoreBoard.make_connection(self.board)

        self.previous = button("<")
        self.next = button(">")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMaximumWidth(int(self.width() * 0.7))

        self.previous.hide()
        self.next.hide()
        self.slider.hide()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.previous)
        button_layout.addWidget(self.slider)
        button_layout.addWidget(self.next)

        #add button
        self.btnHome = button("")
        icon = QIcon("./icon/home.png")
        resizedIcon = icon.pixmap(45, 45)
        self.btnHome.setIcon(QIcon(resizedIcon))
        self.btnRestart = button("")
        icon2 = QIcon("./icon/againb.png")
        resizedIcon2 = icon2.pixmap(45, 45)
        self.btnRestart.setIcon(QIcon(resizedIcon2))

        self.btnHome.hide()
        self.btnRestart.hide()

        down_layout = QHBoxLayout()
        down_layout.addWidget(self.btnHome)
        down_layout.addWidget(self.btnRestart)

        self.central_layout = QVBoxLayout()

        self.lbl_pict = QLabel(self)
        self.lbl_pict.setPixmap(QPixmap("./icon/goPict.jpeg"))
        self.lbl_pict.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_pict.hide()

        self.central_layout.addWidget(self.lbl_pict)
        self.central_layout.addWidget(self.board)
        self.central_layout.addLayout(button_layout)
        self.central_layout.addLayout(down_layout)

        central_widget = QWidget()
        central_widget.setLayout(self.central_layout)
        self.setCentralWidget(central_widget)

        self.scoreBoard.passButtonClicked.connect(self.board.logic.pass_this_turn)
        self.scoreBoard.resignButtonClicked.connect(lambda: self.board.logic.end_of_the_game(resign=True))
        self.board.logic.calculateTerritory.connect(
            lambda: self.scoreBoard.update_black_territory(self.board.logic.black_territory))
        self.board.logic.calculateTerritory.connect(
            lambda: self.scoreBoard.update_white_territory(self.board.logic.white_territory))
        self.board.logic.calculateTerritory.connect(
            lambda: self.scoreBoard.update_white_captured(self.board.logic.white_captured))
        self.board.logic.calculateTerritory.connect(
            lambda: self.scoreBoard.update_black_captured(self.board.logic.black_captured))

        self.board.logic.replayGame.connect(self.init_replay_mode)
        self.board.logic.noReplayGame.connect(self.init_no_replay_mode)

        self.previous.clicked.connect(self.down_slider)
        self.next.clicked.connect(self.up_slider)

        self.btnHome.clicked.connect(self.home)
        self.btnRestart.clicked.connect(self.restart)

        self.slider.valueChanged.connect(self.slider_moved)

        self.resize(800, 800)
        self.center()
        self.setWindowTitle('Go')
        self.setWindowIcon(QIcon("./icon/goo.png"))
        self.show()

    def center(self):
        '''Centers the window on the screen'''
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def resizeEvent(self, event):
        """Resize the slider when we resize the window"""
        new_size = event.size()
        new_slider_width = int(new_size.width() * 0.7)
        self.slider.setFixedWidth(new_slider_width)
        self.slider.setMaximumWidth(new_slider_width)

    def home(self):
        self.restart()
        self.close()
        self.homeButtonClicked.emit()

    def restart(self):
        self.scoreBoard.hide()
        self.initUI()

    """For replay mode"""

    def up_slider(self):
        """Add 1 from the slider value"""
        self.slider.setValue(self.slider.value() + 1)

    def down_slider(self):
        """Remove 1 from the slider value"""
        self.slider.setValue(self.slider.value() - 1)


    def slider_moved(self):
        """Get the current slider value when it moved for the current_state value"""
        index = self.slider.value()
        self.board.set_board(index)
        self.scoreBoard.update_black_captured(self.board.logic.blacks_captured[index])
        self.scoreBoard.update_white_captured(self.board.logic.whites_captured[index])
        self.scoreBoard.update_white_territory(self.board.logic.white_territorys[index])
        self.scoreBoard.update_black_territory(self.board.logic.black_territorys[index])

    def init_replay_mode(self):
        """"Init the replay mode when the game is finish"""
        self.replayModeActivated.emit()
        self.previous.show()
        self.slider.show()
        self.next.show()
        self.btnHome.show()
        self.btnRestart.show()
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self.board.logic.previous_boards) - 1)
        self.slider.setValue(0)
        self.board.start_replay_mode()
        self.scoreBoard.hide_buttons()

        self.slider_moved()

        self.board.set_board(0)

    def init_no_replay_mode(self):
        """"Init the replay mode when the game is finish"""
        self.replayModeActivated.emit()
        self.board.hide()
        self.lbl_pict.show()

        self.btnRestart.show()
        self.btnHome.show()
        self.scoreBoard.hide()
