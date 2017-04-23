import sys
import tkinter

# For checking if user has pygame package installed.
# Without pygame the program doesn't work.
try:
    import pygame
except ImportError:
    print("Could not find pygame 1.9.2")
    sys.exit()

from game.Locals import *
from game.Game import Game
from game.MainMenu import MainMenu
from game.AISettingsMenu import AISettingsMenu
from game.GameSettingsMenu import GameSettingsMenu
##################################
# Initialise modules in pygame.
##################################
pygame.init()

##################################
# Initialise display and give it a size.
##################################
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
##################################

def run():
    depth = MEDIUM_DEPTH
    option = None

    menu = MainMenu(SCREEN)
    settings = AISettingsMenu(SCREEN)
    game = Game(SCREEN)
    # Main game loop
    while True:
        # Get the button clicked from the main menu.
        option = menu.main()
        if option in (1, 2):
            print("HELLO WORLD")
            game.setup_game(option,2)
            game.play(depth)
        elif option == 3:
            depth = settings.main(depth)
        elif option == 4:
            break

run()
