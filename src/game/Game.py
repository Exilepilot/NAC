import tkinter
import os
import random

import pygame
from pygame.locals import *
from game.Locals import * # Globals.
from game.Button import Button # Button widget.
from game.Board import Board # Board class for placing moves on.
from game.MiniMax import get_move # Contains function get_move which runs the minimax algorithm.
from game.Drawing import draw_board, draw_peices, draw_win, draw_msg

FPS = 60
###########################
# DRAWING
###########################

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
        self.__computer_peice = None # The computer's peice.
        self.__player_peice = None # The player's peice. This is for singleplayer mode only!
        self.__current_peice = NOUGHT # The first peice to make a move.

    def board_pos(self, mouse_pos):
        """
        Description: Get a valid board position from mouse position.
        Usage: Get the board cell clicked by the user.
        Params: mouse_pos, (x, y), the position of the mouse when clicked.
        Returns: x, y coordinates relative to the game board.
        """
        if self.__board_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            y = int((mouse_pos[1] - self.__board_rect.y) / (self.__board_rect.height // ROWS))
            x = int((mouse_pos[0] - self.__board_rect.x) / (self.__board_rect.width // COLUMNS))
            return x, y
        return False

    def __setup(self, gamemode, computer_first = False):
        """
        Sets the game mode.
        Params: gamemode, int, 1 for singleplayer, 2 for multiplayer
                computer_first, a boolean, when set true will make the computer start first.
        """
        if gamemode == 1:
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
        # Check if it's the computer's turn.
        computers_turn = self.__current_peice == self.__computer_peice
        print("COMPUTERS TURN {}".format(computers_turn))
        # Get the computers move.
        if computers_turn:
            # Run the minimax algorithm and retrieve it's best move.
            move = get_move(self.__board, self.__ai_depth, self.__computer_peice, self.__player_peice)
            # Place the move.
            self.__board.place_move(self.__current_peice, move)

        # Check for any mouse input on the board.
        for event in pygame.event.get():
            # Check if user has clicked.
            # Don't do this unless it's the players turn and the game is not over.
            if not self.__game_over and event.type == MOUSEBUTTONUP and event.button == 1:
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
            print("Current peice is now: {}".format(self.__current_peice))

    def __draw(self):
        """
        Draws the current state of the game.
        """
        # Draw the board.
        self.__screen.fill(black)
        draw_board(self.__board_surface, self.__board, white, (17, 0, 34))
        draw_peices(self.__board_surface, self.__board, red, blue)

        status_msg = ""
        if self.__game_over:
            # Set the status message to default value.
            if self.__win:
                if self.__current_peice == self.__computer_peice:
                    status_msg = "Computer has won!"
                else:
                    status_msg = "Player {} has won!".format(self.__current_peice)
                # Set the colour based on the player.
                colour = red if self.__current_peice == NOUGHT else blue
                # Draw a line straight through the winning three.
                draw_win(self.__board_surface, self.__winfo, colour)
            elif self.__is_draw:
                status_msg = "Draw!"
        elif self.__current_peice != self.__computer_peice:
                status_msg = "Player {}'s turn!".format(self.__current_peice)
        else:
            status_msg = "Computer's turn!"

        # Draw a status message on the very top of the frame.
        draw_msg(self.__screen, self.__font, status_msg, red, 300, 50)
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
        self.__screen.fill(black)
        self.__board = Board()  # Create an empty 3x3 board.
        self.__win = self.__is_draw = self.__game_over = self.__visible = False
        self.__computer_peice = None # The computer's peice.
        self.__player_peiece = None # The player's peice. This is for singleplayer mode only!
        self.__current_peice = NOUGHT # The first peice to make a move.
        self.__restart_button.reset()
        self.__quit_button.reset()



    def play(self, gamemode, max_ai_depth, computer_first = False):
        """
        Starts a loop displaying the game on the given surface
        until the game is over.
        Params: max_ai_depth - The maximum depth the minimax algorithm can go before stopping.
        """
        self.__ai_depth = max_ai_depth
        self.__setup(gamemode, computer_first)
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

        self.__reset()
