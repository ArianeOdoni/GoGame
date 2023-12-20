from PyQt6.QtWidgets import QApplication

from startGame import Start
import sys


app = QApplication([])
myStart = Start()


sys.exit(app.exec())