"""
The game board object.
"""
from game.Locals import *


class Board:
    def __init__(self):
        """
        Create the board.
        Params: prev_board - The previous board.
        Params: move - Apply a move to the board.
        """

        # Populate the board with 'EMPTY' cells.
        self.state = [[EMPTY]*COLUMNS for i in range(ROWS)]
        # No turns have been made yet.
        self.turns = 0

    @property
    def full(self):
        """
        Returns: True if the board is completely full.
        """
        return self.turns == (ROWS * COLUMNS)

    @property
    def empty(self):
        """
        Returns: True if the board is completely empty.
        """
        return self.turns == 0

    @property
    def game_over(self):
        """
        Checks if the game is at an end state.
        An end state means the board is full and cannot go on.
        """
        win = self.win(NOUGHT) or self.win(CROSS)
        draw = self.draw()
        return win or draw

    def active_player(self):
        """
        Get the peice which needs to move next.
        """
        return NOUGHT if self.turns % 2 == 0 else CROSS

    def check_rows(self, peice, n):
        """
        Counts each occurance of n peices in each row.
        Params: peice, int, The peice to check
        Params: n, int, The number of consecutive peices to count.
        Returns: total occurances, row indexes.
        """
        total = 0
        indexes = []
        for row in range(ROWS):
            count = 0
            for col in range(COLUMNS):
                if self.state[row][col] == peice:
                    count += 1
            if count == n:
                total += 1
                indexes.append(row)

        return total, indexes

    def check_cols(self, piece, n):
        """
        Counts every occurance of n peices in each row.
        Params: peice, int, The peice to check.
        Params: n, int, The number of consecutive peices to count.
        Returns: total occurances, column indexes.
        """
        total = 0  # Number of times it occurs
        indexes = []
        for col in range(ROWS):
            count = 0
            for row in range(COLUMNS):
                if self.state[row][col] == piece:
                    count += 1
            if count == n:
                total += 1
                indexes.append(col)

        return total, indexes

    def check_diagonals(self, peice, n):
        """
        Counts every occurance of n peices in each diagonal.
        Params: peice, int, The peice to check.
        Params: n, int, The number of consecutive peices to count.
        Returns: number of occurances, which diagonal it occured on.
        """
        count = total = 0
        indexes = []

        for row in range(ROWS):
            if self.state[row][row] == peice:
                count += 1

        # Occurred on 1st diagonal.
        if count == n:
            total += 1
            indexes.append(0)

        count = 0
        for row in range(ROWS):
            if self.state[(ROWS-1) - row][row] == peice:
                count += 1

        # Occurred on 2nd diagonal
        if count == n:
            total += 1
            indexes.append(1)

        return total, indexes

    def find(self, peice, n):
        """
        Counts the number of occurances of n peices in any row, column
        or diagonal.
        Returning an integer, the total number of times an occurance has been found.
        """
        rows = self.check_rows(peice, n)[0]
        cols = self.check_cols(peice, n)[0]
        diags = self.check_diagonals(peice, n)[0]
        return rows + cols + diags

    def win(self, peice):
        """
        Gets the row, column or diagonal which contains the win.
        Returns: 'XN', where X = {'R','C','D'} and N = {'0', '1', '2'}
        Returns: False if board hasn't won.
        """
        columns = self.check_cols(peice, 3)
        rows = self.check_rows(peice, 3)
        diagonals = self.check_diagonals(peice, 3)

        # Check columns
        if columns[0] == 1:
            return "{}{}".format("C", columns[1][0])
        # Check rows
        elif rows[0] == 1:
            return "{}{}".format("R", rows[1][0])
        # Check diagonals
        elif diagonals[0] == 1:
            return "{}{}".format("D", diagonals[1][0])

        return False

    def draw(self):
        """
        A draw occurs when no peice wins and the game board is full.
        Returns: True if the game has drawed.
        """
        # Check if either peice has won.
        noughts = self.win(NOUGHT)
        crosses = self.win(CROSS)

        # Check if the board is full.
        if not (noughts or crosses):
            return self.full
        return False

    def place_move(self, peice, move):
        """
        Place move on the board.
        Params: peice,int , The peice to add.
        Params: move, 2-tuple (x, y), The move to make.
        Returns: False, if attempt was unsuccessful, otherwise True.
        """
        assert isinstance(move, tuple), "Could not place move..."
        if self.move_valid(move):
            x, y = move
            self.state[y][x] = peice
            self.turns += 1
            return True
        return False

    def revert_move(self, move):
        """
        Flags a position on the board 'EMPTY'
        Params: move, tuple (x, y)
        """
        x, y = move
        self.state[y][x] = EMPTY
        self.turns -= 1

    def move_valid(self, move):
        """
        Checks if a move is valid on the board.
        Params: move, 2-tuple (x, y), the move to check.
        Returns: True if valid, False otherwise.
        """

        # Check if position exists.
        x, y = move
        if (0 <= x <= COLUMNS - 1) and (0 <= y <= ROWS - 1):
            if self.state[y][x] == EMPTY:
                return True

        return False

    def possible_moves(self):
        moves = []

        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.state[row][col] == EMPTY:
                    moves.append((col, row))
        return moves
