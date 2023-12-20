from PyQt6.QtWidgets import QMessageBox

from confirmationWindow import Confirm

from piece import Piece
from PyQt6.QtCore import QObject, pyqtSignal
from score_board import ScoreBoard
from endGame import EndGame


def have_same_element(array1, array2):
    """Return True if the two array have the same element"""
    sorted_array1 = sorted(array1)
    sorted_array2 = sorted(array2)

    return all(a == b for a, b in zip(sorted_array1, sorted_array2))


def is_same_board(board1, board2):
    if len(board1) != len(board2):
        return False

    for i in range(len(board1)):
        for j in range(len(board1[0])):
            if board1[i][j] != board2[i][j]:
                return False
    return True


def print_board_array(board, txt):
    """prints the boardArray in an attractive way"""
    print(txt)
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in board]))


class GameLogic(QObject):
    print("Game Logic Object Created")
    blackCapturedChanged = pyqtSignal(int)
    whiteCapturedChanged = pyqtSignal(int)

    def __init__(self, board):
        super().__init__()
        self.end_game_dialog = None
        self.taille = 9
        self.plateau = board
        self.previous_boards = []
        self.groups = None
        self.pass_turn = False
        self.current_player = 2
        self.whiteCaptured = 0
        self.blackCaptured = 0
        self.blackTerritory = 0
        self.whiteTerritory = 0
        self.scoreBoard = ScoreBoard()

    '''getters'''

    def getBlackCaptured(self):
        return self.blackCaptured

    def getWhiteCaptured(self):
        return self.whiteCaptured

    def getBlackTerritory(self):
        return self.blackTerritory

    def getWhiteTerritory(self):
        return self.whiteTerritory

    def add_to_group(self, group):
        """Add a group of coordinates to the list of all groups"""

        if group == []:
            return

        if self.groups is None:
            self.groups = []
            self.groups.append(group)
            return True

        for g in self.groups:
            if sorted(g) == sorted(group):
                return False

        self.groups.append(group)

        return True

    def check_liberty_for_group(self, group, board=None):
        """Return False if at least one piece as 1 liberty degree or more"""

        if board is None:
            board = self.plateau

        for position in group:

            if 0 in self.get_surrounding_piece(position[0], position[1], board):
                return False

        return True

    def valid_position(self, row, column):
        '''Check if the position is on the board'''
        return 0 <= row < self.taille and 0 <= column < self.taille

    def position_empty(self, row, column, board=None):
        """Return True if this position is empty on the board"""

        if board is None:
            board = self.plateau

        return board[row][column] == 0

    def place_piece(self, row, column, color):
        """Place a piece if possible"""
        place_possibility = self.can_place(row, column, color)
        if place_possibility is False:
            return False

        for i, r in enumerate(place_possibility):
            for j, x in enumerate(r):
                self.plateau[i][j] = x

        # Reset the pass cycle
        self.pass_turn = False

        # Change the current player
        self.next_player()
        return True

    def can_place(self, row, column, color):
        """Return the new board if we can place a piece at this position, else return False"""

        if not self.valid_position(row, column):
            return False

        if not self.position_empty(row, column):
            return False

        current_board = self.simulate(row, column, color)

        if current_board is False:
            return False

        # KO rules
        if self.is_previous_board(current_board):
            return False

        self.previous_boards.append(current_board)
        return current_board

    def get_surrounding_piece(self, row, column, board=None):
        """Get all pieces around a piece"""
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        all_color = [-1, -1, -1, -1]

        if board is None:
            board = self.plateau

        for index, direction in enumerate(directions):

            if self.valid_position(row + direction[0], column + direction[1]):
                all_color[index] = board[row + direction[0]][column + direction[1]]

        return all_color

    def has_no_liberty(self, row, column, color, board=None):
        """Return true if the piece at this position have no liberty degrees"""

        if board is None:
            board = self.plateau

        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        for direction in directions:

            if self.valid_position(row + direction[0], column + direction[1]):

                # If there is no piece near our piece in a direction, it has at least 1 degree of liberty
                if board[row + direction[0]][column + direction[1]] == 0:
                    return False

                # If there is the same color piece near our piece in a direction, we consider this as 1 degree of
                # liberty
                if board[row + direction[0]][column + direction[1]] == color:
                    return False

        return True

    def make_group(self, row, column, color, visited=None, board=None):
        """Create group of same pieces side by side"""

        if visited is None:
            visited = []

        if board is None:
            board = self.plateau

        # If it's the first time we call the function, we need to know on which color we are working to create the group
        if color is None:
            if self.valid_position(row, column):
                color = board[row][column]

        # We don't want to make group of empty places, so we return an empty array if there is no piece here
        if color == Piece.NoPiece:
            return []

        # If we are not already visited this piece, we can add it to the group
        if (row, column) not in visited:
            visited.append((row, column))

        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        group = [(row, column)]

        # For all surrounding pieces with the same color as this current piece, we do the method to create a group
        for direction in directions:
            next_row, next_column = row + direction[0], column + direction[1]

            if self.valid_position(next_row, next_column) and board[next_row][next_column] == color:
                if (next_row, next_column) not in visited:
                    group += self.make_group(next_row, next_column, color, visited, board)

        return group

    def delete_group(self, group, color, board=None):
        """Delete a group of pieces from the board"""
        if board is None:
            board = self.plateau

        for piece in group:
            if self.valid_position(piece[0], piece[1]):
                board[piece[0]][piece[1]] = Piece.NoPiece
                if color == 1:
                    self.blackCaptured += 1
                if color == 2:
                    self.whiteCaptured += 1
        print("black have captured: " + str(self.whiteCaptured))
        print("white have captured: " + str(self.blackCaptured))

        '''update score board label'''
        self.scoreBoard.update_lbl_black_captured(self.whiteCaptured)
        self.scoreBoard.update_lbl_white_captured(self.blackCaptured)
        self.groups.remove(group)

    def simulate(self, row, column, color):
        """Suicide rules"""
        self.groups = []

        copied_board = []
        last_tro_try = []

        for i, r in enumerate(self.plateau):
            copied_board.append([])
            for x in r:
                copied_board[i].append(x)

        # Place the piece for the simulation
        copied_board[row][column] = color

        # Get the number of our color in the board
        number_before_simulation = self.get_number_of(color, copied_board)

        # Create groups from the copied board
        for i in range(len(copied_board)):
            for j in range(len(copied_board[i])):

                group = self.make_group(i, j, color=None, board=copied_board)

                added = self.add_to_group(group)
                if (row, column) in group and added:

                    for e in group:
                        last_tro_try.append(e)

        # Check if a group is surrounded and delete it if it's
        for g in self.groups:

            if not have_same_element(g, last_tro_try):
                if self.check_liberty_for_group(g, copied_board):
                    self.delete_group(g, color, copied_board)

        if self.check_liberty_for_group(last_tro_try, copied_board):
            self.delete_group(last_tro_try, 0, copied_board)

        number_after_simulation = self.get_number_of(color, copied_board)

        if number_before_simulation > number_after_simulation:  # suicide rules
            return False

        return copied_board

    def get_number_of(self, color, board=None):
        """Get the number of a color in a board"""
        counter = 0

        if board is None:
            board = self.plateau

        for row in board:
            counter += row.count(color)

        return counter

    def is_previous_board(self, board):

        if not self.previous_boards:
            return False

        for previous_board in self.previous_boards:

            if is_same_board(previous_board, board):
                return True

        return False

    def pass_this_turn(self):

        if self.pass_turn == True:
            self.end_of_the_game()
        else:
            self.next_player()
            self.pass_turn = True

    def get_current_player(self):
        return self.current_player

    def next_player(self):
        self.current_player = 3 - self.current_player
        if self.current_player % 2== 0:
            print("Next piece: Black")
        else:
            print("Next piece: White")

    def calculate_score(self):
        # self.countTerritory()
        # Calculate the final scores
        black_score = self.blackTerritory + self.blackCaptured
        white_score = self.whiteTerritory + self.whiteCaptured
        return black_score, white_score

    def end_of_the_game(self, resign=False):
        print("end of the game")

        if resign == True:
            # TODO : open a confirmation window
            confirm_dialog = Confirm()
            result = confirm_dialog.exec()

            if result == QMessageBox.StandardButton.Yes:

                black_score, white_score = self.calculate_score()
                print("Black score : " + str(black_score))
                print("White score :" + str(white_score))

                # TODO : cacher le plateau
                self.endWind = EndGame(black_score, white_score)
                self.endWind.exec()

            else:
                print("continue to play")
        else:
            black_score, white_score = self.calculate_score()
            print("Black score : " + str(black_score))
            print("White score :" + str(white_score))

            # TODO : cacher le plateau
            self.end_game_dialog = EndGame(black_score, white_score)
            self.end_game_dialog.exec()
