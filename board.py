from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint, QPointF
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QRadialGradient, QLinearGradient, QPixmap

from piece import Piece
from game_logic import GameLogic


class Board(QFrame):   # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when the timer is updated
    clickLocationSignal = pyqtSignal(tuple)  # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth = 9  # board is 0 squares wide # TODO this needs updating
    boardHeight = 9  #
    timerSpeed = 1000  # the timer updates every 1 second
    counter = 10  # the number the counter will count down from
    c = 0
    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()
        self.logic = GameLogic(self.boardArray)


    def initBoard(self):
        '''initiates board'''
        self.timer = QTimer(self)  # create a timer for the game
        self.timer.timeout.connect(self.timerEvent)  # connect timeout signal to timerEvent method
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer

        self.connect_signal()

        self.boardArray = [[Piece.NoPiece for _ in range(self.boardWidth)] for _ in range(self.boardHeight)]  # TODO - create a 2d int/Piece array to store the state of the game
        self.printBoardArray()    # TODO - uncomment this method after creating the array above

        #self.setStyleSheet("QFrame { border: 10px solid red; }")

    def drawWoodGrainBackground(self, painter):
        # Load a wood texture image
        wood_texture = QPixmap("./icon/woods.jpg")  # Replace with the path to your wood texture image

        # Create a brush with the wood texture
        brush = QBrush(wood_texture)
        painter.fillRect(self.rect(), brush)

    def connect_signal(self):
        self.clickLocationSignal.connect(self.mousePosToColRow)

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, pos):
        '''convert the mouse click event to a row and column'''

        width = self.squareWidth()
        height = self.squareHeight()

        col = round((pos[0] - width) / width)
        row = round((pos[1] - height) / height)

        self.colRowToMousePos((row, col))

        if self.c  %2 == 0:
            print(self.logic.place_piece(row=row, column=col, color=Piece.Black))

        else:
            print(self.logic.place_piece(row=row, column=col, color=Piece.White))

        self.c += 1

        if self.c % 2 == 0:
            print("Next piece: Black")
        else:
            print("Next piece: White")



        #self.printBoardArray()


    def colRowToMousePos(self, pos):
        '''convert a col and row position to a mouse position'''
        pos_x = pos[0] * self.squareWidth()
        pos_y = pos[1] * self.squareHeight()

        #print(pos_x, pos_y)

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / (self.boardWidth - 1 + 2)  # +2 to let space for the outline

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / (self.boardHeight - 1 + 2)  # +2 to let space for the outline

    def start(self):
        '''starts game'''
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapt this code to handle your timers
        if Board.counter == 0:
            print("Game over")
        self.counter -= 1
        #print('timerEvent()', self.counter)
        self.updateTimerSignal.emit(self.counter)

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)

        self.drawWoodGrainBackground(painter)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)
        self.update()

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = (event.pos().x(), event.pos().y())  # the location where a mouse click was registered
       # print("mousePressEvent() - " + str(clickLoc))
        # TODO you could call some game logic here
        self.clickLocationSignal.emit(clickLoc)

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game
        print("reset")

    def tryMove(self, newX, newY):
        '''tries to move a piece'''
        pass  # Implement this method according to your logic

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        squareWidth = self.squareWidth()
        squareHeight = self.squareHeight()
        for row in range(0, Board.boardHeight - 1):
            for col in range(0, Board.boardWidth - 1):
                painter.save()
                painter.translate(col * squareWidth + squareWidth, row * squareHeight + squareHeight)
                painter.setBrush(QBrush(QColor(212, 177, 147)))  # Set brush color
                #painter.setBrush(QBrush(QColor(255, 255, 255)))
                painter.drawRect(0, 0, int(squareWidth), int(squareHeight))  # Draw rectangles
                painter.restore()

    def drawPieces(self, painter):
        '''draw the pieces on the board'''
        for row in range(len(self.boardArray)):
            for col in range(len(self.boardArray[0])):
                painter.save()
                painter.translate(col * self.squareWidth() + self.squareWidth() / 2, row * self.squareHeight() + self.squareHeight() / 2)
                radius = (min(self.squareWidth(), self.squareHeight()) - 2) / 2
                center = QPoint(int(self.squareWidth() / 2), int(self.squareHeight() / 2))

                '''
                if self.boardArray[row][col] == Piece.Black:
                    # Draw a filled black circle for a black piece

                    painter.setBrush(QColor(0, 0, 0))  # Black color
                    painter.drawEllipse(center, int(radius), int(radius))

                elif self.boardArray[row][col] == Piece.White:
                    # Draw an outlined black ellipse for a white piece

                    painter.setBrush(Qt.BrushStyle.NoBrush)  # No fill
                    painter.setPen(QPen(QColor(0, 0, 0), 2))  # Black outline
                    painter.drawEllipse(center, int(radius), int(radius))'''
                # Change the type of center from QPoint to QPointF
                center = QPointF(self.squareWidth() / 2, self.squareHeight() / 2)

                if self.boardArray[row][col] == Piece.Black:
                    # Draw a filled black circle for a black piece
                    gradient = QRadialGradient(center, radius, center)
                    gradient.setColorAt(0, QColor(0, 0, 0))
                    gradient.setColorAt(1, QColor(50, 50, 50))  # Darker color for shading

                    # Add a radial gradient for the highlight
                    highlight_gradient = QRadialGradient(center, radius / 2, center)
                    highlight_gradient.setColorAt(0, QColor(0,0, 0, 150))  # Adjust the alpha for transparency
                    highlight_gradient.setColorAt(1, QColor(255, 255, 255, 0))

                    # Combine the main gradient with the highlight gradient
                    stops = gradient.stops() + highlight_gradient.stops()
                    combined_gradient = QRadialGradient(center, radius, center)
                    combined_gradient.setStops(stops)

                    painter.setBrush(QBrush(combined_gradient))
                    painter.setBrush(QBrush(gradient))
                    painter.drawEllipse(center, int(radius), int(radius))

                elif self.boardArray[row][col] == Piece.White:

                    # Draw a filled white circle for a white piece
                    gradient = QRadialGradient(center, radius, center)
                    gradient.setColorAt(0, QColor(255, 255, 255))
                    gradient.setColorAt(1, QColor(210, 210, 210))  # Lighter color for highlighting

                    # Add a radial gradient for the highlight
                    highlight_gradient = QRadialGradient(center, radius / 2, center)
                    highlight_gradient.setColorAt(0, QColor(255, 255, 255, 150))  # Adjust the alpha for transparency
                    highlight_gradient.setColorAt(1, QColor(255, 255, 255, 0))

                    # Combine the main gradient with the highlight gradient
                    stops = gradient.stops() + highlight_gradient.stops()
                    combined_gradient = QRadialGradient(center, radius, center)
                    combined_gradient.setStops(stops)

                    painter.setBrush(QBrush(combined_gradient))

                    painter.setBrush(QBrush(gradient))
                    painter.drawEllipse(center, int(radius), int(radius))

                painter.restore()