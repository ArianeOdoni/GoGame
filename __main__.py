from PyQt6.QtWidgets import QApplication
import sys
from startGame import Start


app = QApplication([])
myStart = Start()

sys.exit(app.exec())