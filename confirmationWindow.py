from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox


class Confirm(QMessageBox):
    def __init__(self, txt):
        super().__init__()
        self.initUI(txt)

    def initUI(self, txt):
        self.setWindowTitle('Confirmation')
        self.setWindowIcon(QIcon("./icon/goo.png"))
        self.setText(txt)
        self.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        self.setDefaultButton(QMessageBox.StandardButton.No)
