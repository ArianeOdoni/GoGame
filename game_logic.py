import piece
from piece import Piece


class GameLogic:
    print("Game Logic Object Created")

    def __init__(self, board):
        self.taille = 9
        self.plateau = board
        self.visited = []  # all the visited coordonnate

        self.groups = None

    def add_to_group(self, group):
        '''Add a group of coordinates to the list of all groups'''

        if group == []:
            return

        if self.groups == None:
            self.groups = []
            self.groups.append(group)
            return True

        for g in self.groups:
            if sorted(g) == sorted(group):
                return False

        self.groups.append(group)
        print("Group added : ", group)
        return True

    def check_liberty_for_group(self, group, board=None):
        '''Return False if at least one piece as 1 liberty degree or more'''

        if board is None:
            board = self.plateau

        for piece in group:

            if 0 in self.get_surrounding_piece(piece[0], piece[1], board):
                return False

        print("encerclement détecté pour le group ", group)
        return True

    def valide_position(self, ligne, colonne):
        '''Check if the position is on the board'''
        return 0 <= ligne < self.taille and 0 <= colonne < self.taille

    def position_empty(self, ligne, colonne, board=None):
        '''Check if this position is empty'''

        if board is None:
            board = self.plateau

        return board[ligne][colonne] == 0

    def place_piece(self, row, column, color):
        '''Place a piece on the board if possible'''

        # TODO : a modifier

        if self.can_place(row, column, color):

            self.plateau[row][column] = color

            self.groups = None
            for i in range(9):
                for j in range(9):
                    self.visited = []

                    group = self.make_group(i, j, None)
                    self.add_to_group(group)

            for g in self.groups:
                print(g)
                if self.check_liberty_for_group(g):
                    self.delete_group(g)

            return True
        return False

    def can_place(self, row, column, color):
        """Return True if we can place a piece at this position"""

        if not self.valide_position(row, column):
            return False

        if not self.position_empty(row, column):
            return False

        return self.simulate(row, column, color)
        # if self.has_no_liberty(row, column, color):

        return True

    def get_surrounding_piece(self, row, column, board=None):
        """Get all pieces around a piece"""
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        all_color = [-1, -1, -1, -1]

        if board is None:
            board = self.plateau

        for index, direction in enumerate(directions):

            if self.valide_position(row + direction[0], column + direction[1]):
                all_color[index] = board[row + direction[0]][column + direction[1]]

        return all_color

    def has_no_liberty(self, row, column, color, board=None):
        '''Return true if the piece at this position have no liberty degrees'''

        if board is None:
            board = self.plateau

        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        for direction in directions:

            if self.valide_position(row + direction[0], column + direction[1]):

                # print("pos : ", self.plateau[row + direction[0]][column + direction[1]])

                if board[row + direction[0]][column + direction[1]] == 0:
                    return False

                if board[row + direction[0]][column + direction[1]] == color:
                    return False

        return True

    def make_group(self, row, column, color, visited=None, board=None):
        """Create group of same pieces"""

        if visited is None:
            visited = []

        if board is None:
            board = self.plateau

        if color is None:
            if self.valide_position(row, column):
                color = board[row][column]

        if color == Piece.NoPiece:
            return []

        if (row, column) not in visited:
            visited.append((row, column))

        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        group = [(row, column)]

        for direction in directions:
            next_row, next_column = row + direction[0], column + direction[1]

            if self.valide_position(next_row, next_column) and board[next_row][next_column] == color:
                if (next_row, next_column) not in visited:
                    group += self.make_group(next_row, next_column, color, visited, board)

        return group

    def delete_group(self, group, board=None):

        if board is None:
            board = self.plateau

        for piece in group:

            if self.valide_position(piece[0], piece[1]):
                board[piece[0]][piece[1]] = Piece.NoPiece

        self.groups.remove(group)

    def simulate3(self, row, column, color):

        self.groups = []

        copied_board = []

        for i, r in enumerate(self.plateau):
            copied_board.append([])
            for x in r:
                copied_board[i].append(x)

        copied_board[row][column] = color

        self.printBoardArray(copied_board, "Copied board : ")

        # get the number of our color in the board
        number_before_simulation = self.get_number_of(color, copied_board)

        group = self.make_group(row, column, color=None, board=copied_board)

        self.add_to_group(group)

        if self.check_liberty_for_group(group, copied_board):
            self.delete_group(group, copied_board)
            print("Group deleted : ", group)

        number_after_simulation = self.get_number_of(color, copied_board)

        self.printBoardArray(copied_board, "Copied board after simulation")

        print("number before", number_before_simulation)
        print("number after", number_after_simulation)

        if number_before_simulation > number_after_simulation:  # suicide rules
            print("IMPOSSIBLE PCK ON A PERDU DES PIECES")
            copied_board = []
            return False

        # return if our piece have now some liberty degrees
        # return 0 in self.get_surrounding_piece(row, column, copied_board)
        return True

    def simulate(self, row, column, color):
        """Suicide rules"""
        self.groups = []

        copied_board = []
        last_tro_try = []

        for i, r in enumerate(self.plateau):
            copied_board.append([])
            for x in r:
                copied_board[i].append(x)

        # get a copie a the board
        # copied_board = self.plateau[:]

        # place the piece for the simulation
        copied_board[row][column] = color

        self.printBoardArray(copied_board, "Copied board : ")

        # get the number of our color in the board
        number_before_simulation = self.get_number_of(color, copied_board)

        # create groupe from the copied board
        for i in range(len(copied_board)):
            for j in range(len(copied_board[i])):

                group = self.make_group(i, j, color=None, board=copied_board)

                if (row, column) in group and self.add_to_group(group):

                    for e in group:
                        last_tro_try.append(e)

        print("\nALl groups before simulation")
        for r in self.groups:
            print(r)

        # check if a group is surrounded and delete it if it's
        for g in self.groups:

            if sorted(g) != sorted(last_tro_try):

                if self.check_liberty_for_group(g, copied_board):
                    self.delete_group(g, copied_board)
                    print("Group deleted : ", g)

        print("\nALl groups after simulation")
        for r2 in self.groups:
            print(r2)

        number_after_simulation = self.get_number_of(color, copied_board)

        self.printBoardArray(copied_board, "Copied board after simulation")

        print("number before", number_before_simulation)
        print("number after", number_after_simulation)

        if number_before_simulation > number_after_simulation:  # suicide rules
            print("IMPOSSIBLE PCK ON A PERDU DES PIECES")
            copied_board = []
            return False

        # return if our piece have now some liberty degrees
        # return 0 in self.get_surrounding_piece(row, column, copied_board)
        return True

    def simulateFONCTION(self, row, column, color):
        """Suicide rules"""
        self.groups = []

        copied_board = []

        for i, r in enumerate(self.plateau):
            copied_board.append([])
            for x in r:
                copied_board[i].append(x)

        # get a copie a the board
        # copied_board = self.plateau[:]

        # place the piece for the simulation
        copied_board[row][column] = color

        self.printBoardArray(copied_board, "Copied board : ")

        # get the number of our color in the board
        number_before_simulation = self.get_number_of(color, copied_board)

        # create groupe from the copied board
        for i in range(len(copied_board)):
            for j in range(len(copied_board[i])):
                group = self.make_group(i, j, color=None, board=copied_board)

                self.add_to_group(group)

        print("\nALl groups before simulation")
        for r in self.groups:
            print(r)

        # check if a group is surrounded and delete it if it's
        for g in self.groups:

            if self.check_liberty_for_group(g, copied_board):
                self.delete_group(g, copied_board)
                print("Group deleted : ", g)

        print("\nALl groups after simulation")
        for r2 in self.groups:
            print(r2)

        number_after_simulation = self.get_number_of(color, copied_board)

        self.printBoardArray(copied_board, "Copied board after simulation")

        print("number before", number_before_simulation)
        print("number after", number_after_simulation)

        if number_before_simulation > number_after_simulation:  # suicide rules
            print("IMPOSSIBLE PCK ON A PERDU DES PIECES")
            copied_board = []
            return False

        # return if our piece have now some liberty degrees
        # return 0 in self.get_surrounding_piece(row, column, copied_board)
        return True

    def get_number_of(self, color, board=None):
        """Get the number of a color in a board"""
        counter = 0

        if board is None:
            board = self.plateau

        for row in board:
            counter += row.count(color)

        return counter

    def printBoardArray(self, board, txt):
        '''prints the boardArray in an attractive way'''
        print(txt)
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in board]))