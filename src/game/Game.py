import tkinter
import os
import random

import pygame
from pygame.locals import *
from game.Locals import * # Global constants
from game.Button import Button # Button widget.
from game.Title import Title
from game.Board import Board # Board class for placing moves on.
from game.MiniMax import get_move # Contains function get_move which runs the minimax algorithm.
from game.Drawing import draw_board, draw_peices, draw_win, draw_msg


#TODO: Recomment each function to make sense.
#TODO: Add functionality to let the computer play first or second.
class Game:
    def __init__(self, screen):
        """
        Set up the game.
        Params: screen, root pygame surface.
        """
        # Create the main screen surface.
        self.__screen = screen
        self.__screen.fill((0, 0, 85))  # Fill the background with colour.

        # Initialize Board
        self.__board_surface = pygame.Surface(BOARD_SIZE)
        self.__board_rect = self.__board_surface.get_rect()
        self.__board_rect.x, self.__board_rect.y = BOARD_POS

        # Font filepath.
        topaz_filepath = pygame.font.match_font(FONTFAMILY)

        # Create the font for the title.
        self.__title_font = pygame.font.Font(topaz_filepath, 30)

        # Create the title and center it so that it displays above the board.
        self.__title = Title(self.__screen, self.__title_font, "", 300, 50,
                             True, True, red)

        # Creating the Buttons
        offset = 150
        x = SCREEN_W // 2
        y = SCREEN_H - 50

        # Font for the buttons.
        self.__button_font = pygame.font.Font(topaz_filepath, 15)

        # Restart button for restarting the game, but keeping the same gamemode.
        self.__restart_button = Button(self.__screen, self.__button_font,
                                       100, 30, x - offset, y,
                                       "RESTART", True, (light_red, red),
                                       (white, black))

        # Quit button for backing out into the main menu.
        self.__quit_button = Button(self.__screen, self.__button_font,
                                    100, 30, x + offset, y,
                                    "BACK", True, (light_red, red),
                                    (white, black))

        # Single player variables
        self.__computer_peice = None # The computer's peice.
        self.__player_peice = None # The player's peice.
        # State variables
        self.__board = Board()  # Create an empty 3x3 board.
        self.__win = self.__is_draw = self.__game_over = self.__visible = False
        self.__current_peice = NOUGHT # The first peice to make a move.

    def board_pos(self, mouse_pos):
        """
        Description: Get a valid board position from mouse position.
        Usage: Get the board cell clicked by the user.
        Params: mouse_pos, (x, y), the position of the mouse when clicked.
        Returns: x, y coordinates relative to the game board.
        """
        # Check if the cursor position has collided with the board surface.
        if self.__board_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            # Now convert this mouse position into a valid position on the board.
            y = int((mouse_pos[1] - self.__board_rect.y) / (self.__board_rect.height // ROWS))
            x = int((mouse_pos[0] - self.__board_rect.x) / (self.__board_rect.width // COLUMNS))
            return x, y
        return False

    def __setup(self, max_ai_depth, computer_first):
        """
        Setup the singleplayer gamemode so that either the computer or the
        user can play first.
        Params: max_ai_depth, int, The maximum recursion depth the minimax will go before stopping.
                computer_first, bool, Will the computer go first?
        """
        self.__max_ai_depth = max_ai_depth
        if computer_first:  # if computer starts first, then bost the computer and current peice are the same.
            self.__computer_peice = self.__current_peice = NOUGHT
            self.__player_peice = CROSS
        else:
            self.__computer_peice = CROSS
            self.__current_peice = self.__player_peice = NOUGHT # Player starts first.

    def __input(self):
        """
        Get input from the player.
        """
        # It's the computers turn when the current peice is equal to the
        # peice used by the computer.
        computers_turn = self.__current_peice == self.__computer_peice

        # When it's the computer's turn, make a move.
        if computers_turn:
            # Run the minimax algorithm and retrieve it's best move.
            move = get_move(self.__board, self.__max_ai_depth, self.__computer_peice, self.__player_peice)
            # Then place it.
            self.__board.place_move(self.__current_peice, move)

        # Check for any mouse input on the board.
        for event in pygame.event.get():
            # Check if user has clicked.
            # Don't do this unless it's the players turn and the game is not over.
            if not computers_turn and not self.__game_over and event.type == MOUSEBUTTONUP and event.button == 1:
                # Get the cell chosen and place.
                coords = self.board_pos(event.pos)
                # Are these coords valid?
                if coords:
                    self.__board.place_move(self.__current_peice, coords)
            # Update the state of the buttons.
            self.__restart_button.update(event)
            self.__quit_button.update(event)

    def __update(self):
        """
        Update the state
        """
        # Change the state.
        self.__winfo = self.__board.win(self.__current_peice)
        self.__win = (self.__winfo != False)
        self.__is_draw = self.__board.draw()
        self.__game_over = self.__win or self.__is_draw

        # Switch to the next peice if the game has not already ended.
        if not self.__game_over:
            self.__current_peice = self.__board.active_player()
            #print("Current peice is now: {}".format(self.__current_peice))

    def __draw(self):
        """
        Draws the current state of the game.
        """
        # Clear the screen.
        self.__screen.fill(black)

        # Draw board and peices.
        draw_board(self.__board_surface, self.__board, white, (17, 0, 34))
        draw_peices(self.__board_surface, self.__board, red, blue)

        # Reset the title message.
        self.__title.text = ""

        if self.__game_over:
            if self.__win:
                # Change the status messages appropriately.
                if self.__current_peice == self.__computer_peice:
                    self.__title.text = "Computer has won!"
                else:
                    self.__title.text = "Player {} has won!".format(self.__current_peice)
                # Set the colour based on the player.
                colour = red if self.__current_peice == NOUGHT else blue
                # Draw a line straight through the winning three.
                draw_win(self.__board_surface, self.__winfo, colour)
            elif self.__is_draw:
                self.__title.text = "Draw!"
        elif self.__current_peice == self.__computer_peice:
            self.__title.text = "Computer's turn!"
        else:
            self.__title.text = "Player {}'s turn!".format(self.__current_peice)

        self.__title.draw()
        self.__restart_button.draw()
        self.__quit_button.draw()
        self.__screen.blit(self.__board_surface, self.__board_rect)

    def __restart(self):
        """
        Restart the game state with the previous settings, i.e. computer_peice, player_peice stay the same.
        """
        self.__screen.fill(black)
        self.__board = Board()
        self.__winfo = self.__win = self.__is_draw = self.__game_over = False
        self.__current_peice = NOUGHT
        self.__restart_button.reset()
        self.__quit_button.reset()

    def __reset(self):
        """
        Completely reset the game state.
        """

        self.__screen.fill(black) # Fill the screen with black.
        self.__board = Board()  # Create an empty 3x3 board.
        self.__win = self.__is_draw = self.__game_over = self.__visible = False
        # Reset variables used in singleplayer
        self.__computer_peice = self.__player_peice = None
        # Reset to the default starting peice: Nought.
        self.__current_peice = NOUGHT
        # Reset the button state.
        self.__restart_button.reset()
        self.__quit_button.reset()

    def play(self, gamemode, max_ai_depth, computer_first = False):
        """
        Starts a loop displaying the game on the given surface
        until the game is over.
        Params: gamemode, int, 1 for singleplayer, 2 for multiplayer.
                max_ai_depth, int, The maximum recursion depth the minimax can go before stopping.
                computer_first, bool, Will the computer play first if the gamemode is single player?
        Returns: None
        """
        # If the gamemode is singleplayer.
        if gamemode == SINGLEPLAYER:
            self.__setup(max_ai_depth, computer_first)
        # Setup the pygame clock.
        exit = False
        # Main loop.
        while not exit:
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

        self.__reset()
