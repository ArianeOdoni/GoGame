from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox


class Confirm(QMessageBox):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Confirmation')
        self.setText("Do you really want to stop the game?")
        self.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        self.setDefaultButton(QMessageBox.StandardButton.No)
