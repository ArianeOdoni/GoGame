from logging import root
from tkinter import Frame

from PyQt5.QtWidgets import QApplication
from go import Go
from board import Board
import sys

app = QApplication([])
myGo = Go()

myBoard = Board(myGo)
sys.exit(app.exec_())
