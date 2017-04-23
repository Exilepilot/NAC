import tkinter
import os
import random

import pygame
from pygame.locals import *
from game.Locals import * # Globals.
from game.Button import Button # Button widget.
from game.Board import Board # Board class for placing moves on.
from game.MiniMax import get_move # Contains function get_move which runs the minimax algorithm.


FPS = 60
###########################
# DRAWING
###########################


def draw_board(master, board, fg=(0, 0, 0), bg=(255, 255, 255)):
    """
    Draws a tic tac toe board, which is then blit onto the master surface.
    Params: master,     pygame.Surface , Is the main surface to be drawn on.
    Params: board,      2d list        , The state of the tic tac toe board.
    Params: fg, tuple (r, g, b), The foreground colour.
    Params: bg, tuple (r, g, b), The background colour.
    """
    # Clear previous surface.
    master.fill(bg)

    # Get the surface width and height.
    rect = master.get_rect()
    width = rect.width
    height = rect.height

    # Get the average cell width and height.
    c_width = width // COLUMNS
    c_height = height // ROWS

    # Draw each row and column separator.
    line_width = 3
    for i in range(1, ROWS):
        pygame.draw.line(master, fg, (0, i * c_height),
                         (width, i * c_height), line_width)
        pygame.draw.line(master, fg, (i * c_width, 0),
                         (i * c_width, height), line_width)


def draw_peices(master, board, player1=(255, 0, 0), player2=(0, 255, 0)):
    # Get the surface width and height.
    rect = master.get_rect()
    width = rect.width
    height = rect.height

    # Get the average cell width and height.
    c_width = width // COLUMNS
    c_height = height // ROWS

    # Draw each peice, unless the board is empty.
    if not board.empty:
        padding = 30    # ten pixel padding for each peice.
        line_width = 7  # line width

        for row in range(ROWS):
            for col in range(COLUMNS):
                player = board.state[row][col]
                x, y = col * c_width, row * c_height

                if player == PLAYER_ONE:  # Draw a naught
                    pygame.draw.line(master, player1, (x + padding, y + padding),
                                     (x + c_width - padding, y + c_height - padding),
                                     line_width)

                    pygame.draw.line(master, player1,
                                     (x + padding, y + c_height - padding),
                                     (x + c_height - padding, y + padding), line_width)

                elif player == PLAYER_TWO:  # Draw a cross
                    radius = (c_height + c_width) // 4 # Avg then /2 again because r = d / 2
                    pygame.draw.circle(master, player2, (x + (c_width // 2),
                                        (y + (c_height // 2))), radius - padding, line_width)


def draw_win(master, winfo, line_colour):
    """
    Draws a line through the row, column or diagonal to indicate a win.
    Params: master, pygame.Surface, surface to draw on.
    Params: winfo, string, Where on the board the win occurred.
    Params: line_colour, tuple (r, g, b), colour of the line to draw.
    Returns: None.
    Creation: 8/1/17 Ricky Claven
    """
    print(winfo)
    # Get the width and height of the surface.
    rect = master.get_rect()
    width = rect.width
    height = rect.height

    # Get the average cell width and height.
    c_width = width // COLUMNS
    c_height = height // ROWS

    # Get half width/height of the cell.
    half_c_width = c_width // 2
    half_c_height = c_height // 2

    # Use our win-info.
    orientation = winfo[0]  # Row, column or diagonal
    pos = int(winfo[1])  # Which row, column or diagonal.

    # Line width
    line_width = 15

    if orientation == "R":  # ROWS
        # Get the y position in the middle of the cell.
        y1 = half_c_height + (pos * c_height)
        x1 = 0
        x2 = width

        pygame.draw.line(master, line_colour, (x1, y1), (x2, y1), line_width)
    elif orientation == "C":  # COLUMNS
        x1 = half_c_width + (pos * c_width)
        y1 = 0
        y2 = height

        pygame.draw.line(master, line_colour, (x1, y1), (x1, y2), line_width)
    else:   # DIAGONALS
        x1 = 0
        y1 = 0 if pos == 0 else height
        x2 = width
        y2 = height if pos == 0 else 0

        pygame.draw.line(master, line_colour, (x1, y1), (x2, y2), line_width)


def draw_msg(master, font, text, colour, x, y, bgcolour=None):
    """
    Draws text on surface.
    Params: master, pygame.Surface, surface to place text on.
    Params: font, pygame.font.Font, font to render with.
    Params: text, string, string to draw.
    Params: x, int, x position (centered)
    Params: y, int, y position (centered)
    Returns: None
    Creation: 8/1/17
    """

    msg = font.render(text, True, colour, bgcolour)
    msg_rect = msg.get_rect()
    msg_rect.centerx = x
    msg_rect.centery = y

    master.blit(msg, msg_rect)


## TODO: Rename this function.
def get_board_pos(board_rect, mouse_pos):
    """
    Get a valid board position from mouse position.
    Params: master, pygame.Rect, the surface that has been clicked.
    Params: mouse_pos, (x, y), the position of the mouse when clicked.
    Returns: x, y coordinates relative to the game board.
    Creation: 8/1/17
    """
    if board_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
        y = int((mouse_pos[1] - board_rect.y) / (board_rect.height // ROWS))
        x = int((mouse_pos[0] - board_rect.x) / (board_rect.width // COLUMNS))
        return x, y
    return False


def get_random_pos(board):
    """
    Pick a random position on the board.
    Params: board, 2d list, Board to get a valid position from.
    Returns: x, y position relative to the game board.
    Creation: 9/1/17
    """
    valid = False
    while not valid:
        random.seed()
        x = random.randint(0, COLUMNS - 1)
        y = random.randint(0, ROWS - 1)
        valid = board.move_valid((x, y))
    return x, y


class Game:
    def __init__(self, screen):
        """
        Set up the game.
        Params: screen, root pygame surface.
        Params: gamemode, int, 0 for singleplayer, 1 for multiplayer.
        Params: computer, peice, The board peice the computer will use.
        """
        # Create the main screen surface.
        self.__screen = screen
        self.__screen.fill((0, 0, 85))  # Fill the background with colour.

        # Initialize Board
        self.__board_surface = pygame.Surface(BOARD_SIZE)
        self.__board_rect = self.__board_surface.get_rect()
        self.__board_rect.x, self.__board_rect.y = BOARD_POS

        # Font filepath.
        topaz_filepath = pygame.font.match_font("Topaz-8")

        # Create the font for messages.
        self.__font = pygame.font.Font(topaz_filepath, 30)

        # Buttons
        offset = 150
        x = SCREEN_W // 2
        y = SCREEN_H - 50

        self.__button_font = pygame.font.Font(topaz_filepath, 15)
        self.__restart_button = Button(self.__screen, self.__button_font,
                                       100, 30, x - offset, y,
                                       "RESTART", True, (light_red, red),
                                       (white, black))

        self.__quit_button = Button(self.__screen, self.__button_font,
                                    100, 30, x + offset, y,
                                    "BACK", True, (light_red, red),
                                    (white, black))

        # State variables
        self.__board = Board()  # Create an empty 3x3 board.
        self.__win = self.__is_draw = self.__game_over = self.__visible = False
        self.__computer = None
        self.__player = PLAYER_TWO  # Player one starts.

    def setup_game(self, gamemode, first_player):
        """
        Sets the game mode.
        Params: gamemode, int, 1 for singleplayer, 2 for multiplayer
        """
        self.__first_player = first_player
        self.__player = first_player

        if gamemode == 1:
            self.__computer = 2
        elif gamemode == 2:
            self.__computer = None

    def __input(self):
        """
        Get input from the player.
        """
        #########################################
        # When it's computers turn to move, retrieve a move generated
        # from the minimax algorithm.
        #########################################

        if self.__player == self.__computer:
            move = get_move(self.__board, self.__ai_depth)
            self.__board.place_move(self.__board.active_player, move)


        for event in pygame.event.get():
            # Check if user has clicked.
            if not self.__game_over and event.type == MOUSEBUTTONUP and event.button == 1:
                # Get the cell chosen and place.
                coords = get_board_pos(self.__board_rect, event.pos)
                if coords:
                    self.__board.place_move(self.__board.active_player, coords)
            self.__restart_button.update(event)
            self.__quit_button.update(event)

    def __update(self):
        """
        Update the state
        """
        # Change the state.
        self.__winfo = self.__board.win(self.__player)
        self.__win = (self.__winfo != False)
        self.__is_draw = self.__board.draw()
        self.__game_over = self.__win or self.__is_draw

        # Switch the player if the game has not already ended.
        if not self.__game_over:
            self.__player = self.__board.active_player

    def __draw(self):
        """
        Draws the current state of the game.
        """
        # Draw the board.
        self.__clear()
        draw_board(self.__board_surface, self.__board, white, (17, 0, 34))
        draw_peices(self.__board_surface, self.__board, red, blue)

        status_msg = ""
        if self.__game_over:
            # Set the status message to default value.
            if self.__win:
                if self.__player == self.__computer:
                    status_msg = "Computer has won!"
                else:
                    status_msg = "Player {} has won!".format(self.__player)
                # Set the colour based on the player.
                colour = red if self.__player == PLAYER_ONE else blue
                # Draw a line straight through the winning three.
                draw_win(self.__board_surface, self.__winfo, colour)
            elif self.__is_draw:
                status_msg = "Draw!"
        elif self.__player != self.__computer:
                status_msg = "Player {}'s turn!".format(self.__player)
        else:
            status_msg = "Computer's turn!"

        # Draw a status message on the very top of the frame.
        draw_msg(self.__screen, self.__font, status_msg, red, 300, 50)
        self.__restart_button.draw()
        self.__quit_button.draw()
        self.__screen.blit(self.__board_surface, self.__board_rect)

    def __restart(self):
        """
        Restart the game state
        """
        self.__first_time = True
        self.__board = Board()
        self.__winfo = self.__win = self.__is_draw = self.__game_over = False
        self.__player = self.__first_player
        self.__restart_button.reset()
        self.__quit_button.reset()
        self.__clear()

    def __clear(self):
        self.__screen.fill(black)

    def play(self, depth):
        """
        Starts a loop displaying the game on the given surface
        until the game is over.
        Params: depth - The maximum depth the minimax algorithm can go before stopping.
        """
        self.__ai_depth = depth
        self.__clear()
        # Setup the pygame clock.
        clock = pygame.time.Clock()
        exit = False
        # Main loop.
        while not exit:
            # Set FPS limit to 60.
            clock.tick(FPS)
            if self.__restart_button.clicked:
                self.__restart()
            elif self.__quit_button.clicked:
                exit = True
            # Poll the event queue for input.
            self.__input()
            # Update the game state
            self.__update()
            # Draw
            self.__draw()
            pygame.display.update()
        # Reset the state.
        self.__restart()
