from PyQt5.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QBrush, QPainter
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
from custom_button import CustomButton
from rules import Rules

class EndGame(QDialog):
    def __init__(self, scoreBlack=0, scoreWhite=0):
        super().__init__()
        self.go_window = None
        self.initUI(scoreBlack, scoreWhite)

    def initUI(self, scoreBlack, scoreWhite):

        self.setWindowTitle("This is the end")
        self.setStyleSheet("background-color: rgb(212, 177, 147);")

        # enter txt
        lblWinner = QLabel()
        lblLooser = QLabel()
        lblPoint = QLabel()
        if scoreWhite > scoreBlack:  # White won
            lblWinner.setText("Well done White, you have won !")
            lblWinner.setStyleSheet("font-weight: bold;")
        elif scoreWhite == scoreBlack:  # player are ex aequo
            lblWinner.setText("Well done Black and White")
            lblWinner.setStyleSheet("font-weight: bold;")
            lblLooser.setText("restart a game to break the tie !")
        else:  # Black won
            lblWinner.setText("Well done Black, you have won !")
            lblWinner.setStyleSheet("font-weight: bold;")

        lblPoint.setText("Final scores:\n\t- Black score: " + str(scoreBlack) + "\n\t- White score: " + str(scoreWhite))

        # layout
        layout = QVBoxLayout()
        icon_pixmap = QPixmap("./icon/victory.png")
        icon_label = QLabel()
        icon_label.setPixmap(icon_pixmap.scaledToWidth(40))  # Adjust the width as needed

        # btn
        btnReplay = CustomButton("")
        icon = QIcon("./icon/replayb.png")
        resizedIcon = icon.pixmap(45, 45)
        btnReplay.setIcon(QIcon(resizedIcon))
        btnPlayAgain = CustomButton("")
        btnPlayAgain.setIcon(QIcon("./icon/againb.png"))
        btnMenu = CustomButton("")
        btnMenu.setIcon(QIcon("./icon/rules.png"))

        # Arrange icon and labels side by side using QHBoxLayout
        layoutH = QHBoxLayout()
        layoutH.addWidget(icon_label)
        layoutH.addStretch()  # Add some space between icon and text
        layoutH.addWidget(lblWinner)
        layout.addLayout(layoutH)
        layout.addWidget(lblLooser)
        layout.addWidget(lblPoint)
        layoutH2 = QHBoxLayout()
        layoutH2.addWidget(btnMenu)
        layoutH2.addWidget(btnReplay)
        layoutH2.addWidget(btnPlayAgain)
        layout.addLayout(layoutH2)

        self.setLayout(layout)

        # connect btn
        btnMenu.clicked.connect(self.rules_clicked)
        btnPlayAgain.clicked.connect(self.playAgain_clicked)

        self.show()

    def rules_clicked(self):
        if not self.go_window:
            self.go_window = Rules()
        self.go_window.show()

    def playAgain_clicked(self):
        self.close()
        if not self.go_window:
            self.go_window = Rules()
        self.go_window.show()