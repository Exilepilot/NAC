"""
The game board object.
"""
from game.Locals import *


class Board:
    def __init__(self, prev_board=None, move=None):
        """
        Create the board.
        Params: prev_board - The previous board.
        Params: move - Apply a move to the board.
        """
        self.state = [[EMPTY]*COLUMNS for i in range(ROWS)]
        self.turns = 0
        # If prev_board is not none
        # Then check if a move is present and apply it.
        if prev_board:
            self.turns = prev_board.turns
            self.state = prev_board.state
            if not move is None:
                x, y = move
                print(x, y)
                self.state[y][x] = self.active_player

    def __repr__(self):
        """
        Used for representing the board object in a user friendly way.
        """
        for row in range(ROWS):
            print("+---+---+---+\n")
            for column in range(COLUMNS):
                peice = self.state[row][column]
                if not peice:
                    peice = " "

                print("| {} ".format(peice))
            print("|")
            print("\n")
            print("+---+---+---+")
        print("Turns made: {}".format(self.__turns))
        print("Player to move: {}".format(self.active_player))

    def __str__(self):
        """
        Used when the object is casted into a string.
        """
        msg = ""
        for row in range(ROWS):
            msg += "+---+---+---+\n"
            for column in range(COLUMNS):
                peice = self.state[row][column]
                if not peice:
                    peice = " "
                msg += "| {} ".format(peice)
            msg += "|"

        msg += "+---+---+---+\n"
        msg += "Turns made: {}\n".format(self.turns)
        msg += "Player to move: {}\n".format(self.active_player)
        return msg

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
        win = self.win(PLAYER_ONE) or self.win(PLAYER_TWO)
        draw = self.draw()
        return win or draw

    @property
    def active_player(self):
        """
        Get the active player (i.e. the player to move) from board state.
        """
        return PLAYER_ONE if self.turns % 2 == 0 else PLAYER_TWO

    def check_rows(self, player, n):
        """
        Counts every occurance of n peices in each row.
        Params: board, 2d list, The board to check.
        Params: player, int, The player to check
        Params: n, int, The number of consecutive peices to count.
        Returns: total occurances, row indexes.
        Creation 8/1/17 Ricky Claven.
        """
        total = 0
        indexes = []
        for row in range(ROWS):
            count = 0
            for col in range(COLUMNS):
                if self.state[row][col] == player:
                    count += 1
            if count == n:
                total += 1
                indexes.append(row)

        return total, indexes

    def check_cols(self, player, n):
        """
        Counts every occurance of n peices in each row.
        Params: board, 2d list, The board to check.
        Params: player, int, The player to check.
        Params: n, int, The number of consecutive peices to count.
        Returns: total occurances, column indexes.
        Creation 8/1/17 Ricky Claven.
        """
        total = 0  # Number of times it occurs
        indexes = []
        for col in range(ROWS):
            count = 0
            for row in range(COLUMNS):
                if self.state[row][col] == player:
                    count += 1
            if count == n:
                total += 1
                indexes.append(col)

        return total, indexes

    def check_diagonals(self, player, n):
        """
        Counts every occurance of n peices in each diagonal.
        Params: board, 2d list, The board to check.
        Params: player, int, The player to check.
        Params: n, int, The number of consecutive peices to count.
        Returns: number of occurances, which diagonal it occured on.
        Creation 8/1/17 Ricky Claven.
        """
        count = total = 0
        indexes = []

        for row in range(ROWS):
            if self.state[row][row] == player:
                count += 1

        # Occurred on 1st diagonal.
        if count == n:
            total += 1
            indexes.append(0)

        count = 0
        for row in range(ROWS):
            if self.state[(ROWS-1) - row][row] == player:
                count += 1

        # Occurred on 2nd diagonal
        if count == n:
            total += 1
            indexes.append(1)

        return total, indexes

    def find(self, player, n):
        rows = self.check_rows(player, n)[0]
        cols = self.check_cols(player, n)[0]
        diags = self.check_diagonals(player, n)[0]
        return rows + cols + diags

    def win(self, player):
        """
        Gets the row, column or diagonal which contains the win.
        Returns: 'XN', where X = {'R','C','D'} and N = {'0', '1', '2'}
        Returns: False if board hasn't won.
        Creation 8/1/17 Ricky Claven
        """
        columns = self.check_cols(player, 3)
        rows = self.check_rows(player, 3)
        diagonals = self.check_diagonals(player, 3)

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
        A draw occurs when no player wins and the game board is full.
        Returns: True if the game has drawed.
        """
        # Check if either player has won.
        player_one = self.win(PLAYER_ONE)
        player_two = self.win(PLAYER_TWO)

        # If not, then check if the game is full.
        if not (player_one or player_two):
            return self.full
        return False

    def place_move(self, player, move):
        """
        Attempt placing on the board.
        Params: player,int ,  The player making the move.
        Params: move, 2-tuple (x, y), The move to make.
        Returns: False if attempt was unsuccessful, successful otherwise.
        """
        assert isinstance(move, tuple), "Could not place move..."
        if self.move_valid(move):
            x, y = move
            self.state[y][x] = player
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
