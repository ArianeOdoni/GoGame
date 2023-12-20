from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout

from custom_button import CustomButton


class EndGame(QDialog):

    def __init__(self, score_black=0, score_white=0):
        super().__init__()
        self.replay = False
        self.initUI(score_black, score_white)

    def initUI(self, score_black, score_white):
        self.end_wind = QDialog()
        self.end_wind.setWindowIcon(QIcon("./icon/goo.png"))
        self.end_wind.setWindowTitle("This is the end")
        self.end_wind.setStyleSheet("background-color: rgb(212, 177, 147);")

        # enter txt
        lblWinner = QLabel()
        lblLooser = QLabel()
        lblPoint = QLabel()

        if score_white > score_black:  # White won
            lblWinner.setText("Well done White, you have won !")
            lblWinner.setStyleSheet("font-weight: bold;")
        elif score_white == score_black:  # player are ex aequo
            lblWinner.setText("Well done Black and White")
            lblWinner.setStyleSheet("font-weight: bold;")
            lblLooser.setText("restart a game to break the tie !")
        else:  # Black won
            lblWinner.setText("Well done Black, you have won !")
            lblWinner.setStyleSheet("font-weight: bold;")

        lblPoint.setText(
            "Final scores:\n\t- Black score: " + str(score_black) + "\n\t- White score: " + str(score_white))

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

        # Arrange icon and labels side by side using QHBoxLayout
        layoutH = QHBoxLayout()
        layoutH.addWidget(icon_label)
        layoutH.addStretch()  # Add some space between icon and text
        layoutH.addWidget(lblWinner)
        layout.addLayout(layoutH)
        layout.addWidget(lblLooser)
        layout.addWidget(lblPoint)
        layout.addWidget(btnReplay)

        self.end_wind.setLayout(layout)

        # connect button
        btnReplay.clicked.connect(self.replay_clicked)

        # display window
        self.end_wind.exec()

    def replay_clicked(self):
        self.end_wind.close()
        self.replay = True

