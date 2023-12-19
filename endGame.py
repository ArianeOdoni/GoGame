from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout


class EndGame(QDialog):
    def __init__(self, scoreBlack=0, scoreWhite=0):
        super().__init__()
        self.initUI(scoreBlack, scoreWhite)

    def initUI(self, scoreBlack, scoreWhite):
        endWind = QDialog()
        endWind.setWindowTitle("This is the end")

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

        lblPoint.setText("Final scores:\n\t- Black score: "+str(scoreBlack)+"\n\t- White score: "+str(scoreWhite))

        # layout
        layout = QVBoxLayout()
        icon_pixmap = QPixmap("./icon/victory.png")
        icon_label = QLabel()
        icon_label.setPixmap(icon_pixmap.scaledToWidth(40))  # Adjust the width as needed

        # Arrange icon and labels side by side using QHBoxLayout
        layoutH = QHBoxLayout()
        layoutH.addWidget(icon_label)
        layoutH.addStretch()  # Add some space between icon and text
        layoutH.addWidget(lblWinner)
        layout.addLayout(layoutH)
        layout.addWidget(lblLooser)
        layout.addWidget(lblPoint)

        endWind.setLayout(layout)

        # display window
        endWind.exec()


