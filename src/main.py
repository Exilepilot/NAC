import sys

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
    menu = MainMenu(SCREEN)
    AI_settings = AISettingsMenu(SCREEN)
    game_settings = GameSettingsMenu(SCREEN)
    game = Game(SCREEN)
    computer_first = False
    # Main game loop
    while True:
        # Get the button clicked from the main menu.
        bttn_opt = menu.main()
        if bttn_opt == 1:
            # Get the button pressed in the game settings form by the user.
            # Returning 1 for 'you' as in the user, 2 for 'computer' and
            # False which means that the user has pressed the escape key.
            first_player = game_settings.main()
            # Enter game loop.
            game.play(bttn_opt, depth, first_player == 2)
        elif bttn_opt == 2:
            game.play(bttn_opt, depth)
        elif bttn_opt == 3:
            depth = AI_settings.main(depth)
        elif bttn_opt == 4:
            break



run()
