"""
A file containing functions for drawing various elements within the game, for e.g.
a nought or cross.
"""
try:
    import pygame
except ImportError:
    print("Could not find pygame 1.9.2")
    sys.exit()
from game.Locals import *


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

def draw_peices(master, board, nought_colour=(255, 0, 0),
                cross_colour=(0, 255, 0)):
    """
    Draws the peices on the board surface.
    Params: board, pygame.Surface to draw on.
            nought_colour, tuple (int r, int g, int b) for the colour of the nought.
            cross_colour, ^same as above^, for the colour of the cross.
    """
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
                peice = board.state[row][col]
                x, y = col * c_width, row * c_height

                if peice == CROSS:  # Draw a cross
                    pygame.draw.line(master, cross_colour, (x + padding, y + padding),
                                     (x + c_width - padding, y + c_height - padding),
                                     line_width)

                    pygame.draw.line(master, cross_colour,
                                     (x + padding, y + c_height - padding),
                                     (x + c_height - padding, y + padding), line_width)

                elif peice == NOUGHT:  # Draw a nought
                    radius = (c_height + c_width) // 4 # Avg then /2 again because r = d / 2
                    pygame.draw.circle(master, nought_colour, (x + (c_width // 2),
                                        (y + (c_height // 2))), radius - padding, line_width)

def draw_win(master, winfo, line_colour):
    """
    Draws a line through the row, column or diagonal to indicate a win.
    Params: master, pygame.Surface, surface to draw on.
    Params: winfo, string, Where on the board the win occurred.
    Params: line_colour, tuple (r, g, b), colour of the line to draw.
    Returns: None.
    """
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
