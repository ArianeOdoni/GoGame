from PyQt6.QtWidgets import QApplication

from startGame import Start
import sys

app = QApplication([])
myStart = Start()

# myGo = Go()
# myMenu = Menu()

sys.exit(app.exec())


