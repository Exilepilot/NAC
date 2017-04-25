"""
Contains global constants used throughout the project.
"""

# Window size.
SCREEN_SIZE = SCREEN_W, SCREEN_H = 600, 600
# Board size
BOARD_SIZE = BOARD_W, BOARD_H = 400, 400
# Board position on window.
BOARD_POS = BOARD_X, BOARD_Y = 100, 100
# Board rows and columns.
ROWS = COLUMNS = 3
# Peices on the board.
NOUGHT = 1
CROSS = 2
# Empty peice is represented by None.
EMPTY = None
# Maximum AI depth for each difficulty.
EASY_DEPTH = 1
MEDIUM_DEPTH = 2
HARD_DEPTH = 3
IMPOSSIBLE_DEPTH = 5 # 6-7 can be a really long wait.
# Gamemodes
SINGLEPLAYER = 1
MULTIPLAYER = 2
# Font family
FONTFAMILY = "Topaz-8"

###########################
# COLOURS
###########################
white = (255, 255, 255)
black = (0, 0, 0)

red = (255, 0, 0)
light_red = (255, 107, 120)

dark_red = (179, 0, 0)
darker_red = (103, 0, 0)

navy = (0, 30, 61)
light_navy = (50, 74, 99)

green = (0, 255, 0)
light_green = (30, 255, 141)

blue = (0, 0, 255)
light_blue = (30, 144, 255)

orange = (255, 79, 34)
light_orange = (255, 129, 15)

cyan = (0, 179, 179)
light_cyan = (0, 255, 255)
