from PyQt6.QtWidgets import QApplication
from go import Go
from startGame import Start
from menu import Menu
import sys


app = QApplication([])
myStart = Start()
#myGo = Go()
#myMenu = Menu()

sys.exit(app.exec())