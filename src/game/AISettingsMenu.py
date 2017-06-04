"""
Pygame settings menu.
"""
try:
    import pygame
    from pygame.locals import *
except ImportError:
    print("Could not find pygame 1.9.2...")
    print("Please install via pip.")
    input()  # Wait for user to press any key.
    exit()

from game.Locals import *
from game.Button import Button
from game.Title import Title

class AISettingsMenu:
    # Menu size, positioning, and colours.
    menu_size = 400, 300
    menu_pos = menu_x, menu_y = (100, 150)
    menu_bg = blue
    menu_fg = white

    # Easy button colours.
    easy_button_bg = (light_green, green)
    easy_button_fg = (black, white)

    # Medium button colours.
    medium_button_bg = (light_orange, orange)
    medium_button_fg = (black, white)

    # Hard button colours.
    hard_button_bg = (light_red, red)
    hard_button_fg = (black, white)

    # Impossible button colours.
    impossible_button_bg = (dark_red, darker_red)
    impossible_button_fg = (black, white)

    # Back button colours.
    back_button_bg = (light_cyan, cyan)
    back_button_fg = (black, white)

    def __init__(self, screen):
        """
        Create pygame main menu widget.
        Params: screen, An initialised pygame.display.
        """
        self.__screen = screen
        self.__font = pygame.font.Font(pygame.font.match_font("Topaz-8"), 15)

        # Create the menu.
        self.__menu = pygame.Surface(self.menu_size)
        self.__menu_rect = self.__menu.get_rect()
        self.__menu_rect.x = self.menu_x
        self.__menu_rect.y = self.menu_y

        # Set the title bold to stand out.
        self.__title_font = pygame.font.Font(pygame.font.match_font("Topaz-8"), 50)

        # Create the title.
        self.__title = Title(self.__screen, self.__title_font, "AI SETTINGS",
                             300, 50, True, True)

        # Create the sub title at the bottom to indicate what the difficulty is already set to.
        self.__sub_title_text = None
        self.__sub_title_font = pygame.font.Font(pygame.font.match_font("Topaz-8"), 20)
        self.__sub_title = Title(self.__screen, self.__sub_title_font,
                                 self.__sub_title_text, 300,
                                 550, True, True)

        # Button positioning
        x_offset = 20
        y_offset = 60
        b_width = 360
        b_height = 60

        # EASY BUTTON
        self.__easy = Button(self.__menu, self.__font, b_width,
                             b_height, x_offset, 0, "EASY", False,
                             self.easy_button_bg, self.easy_button_fg)
        # MEDIUM BUTTON
        self.__medium = Button(self.__menu, self.__font, b_width,
                               b_height, x_offset, y_offset,
                               "MEDIUM", False,
                               self.medium_button_bg, self.medium_button_fg)
        # HARD BUTTON
        self.__hard = Button(self.__menu, self.__font,
                             b_width, b_height, x_offset, 2 * y_offset,
                             "HARD", False,
                             self.hard_button_bg, self.hard_button_fg)
        # IMPOSSIBLE BUTTON
        self.__impossible = Button(self.__menu, self.__font,
                             b_width, b_height, x_offset, 3 * y_offset,
                             "IMPOSSIBLE", False,
                             self.impossible_button_bg, self.impossible_button_fg)
        # BACK BUTTON
        self.__back = Button(self.__menu, self.__font,
                             b_width, b_height, x_offset, 4 * y_offset,
                             "BACK", False,
                             self.back_button_bg, self.back_button_fg)


        self.__exit = False # When the user wants to go back.
        self.__clicked = False # When ther user has clicked on a button.

    def get_difficulty_from_depth(self, depth):
        """
        Convert the current depth to the name of the Difficulty
        Params: depth - int
        Returns: str message
        """
        if depth == EASY_DEPTH:
            return "EASY"
        elif depth == MEDIUM_DEPTH:
            return "MEDIUM"
        elif depth == HARD_DEPTH:
            return "HARD"
        elif depth == IMPOSSIBLE_DEPTH:
            return "IMPOSSIBLE"

    def update(self, event):
        """
        Description: Updates the main menu once a MOUSEBUTTONDOWN/MOUSEMOTION event
        has been triggered.
        - Check the state of the buttons (by updating them with a new event from the queue).
        - Change the look of each button if the cursor has hovered over it.
        - If the button has been clicked then update the state of the menu. (This causes something to happen)
        Params: event - The most recent event from the event queue.
        """

        # Reset the state of the menu.
        self.__clicked = False
        # Used for transforming the position of which the event occured: relative to the buttons.
        x, y = self.__menu_rect.x, self.__menu_rect.y
        # Convert x,position so that it is relative to the button.
        event.pos = (event.pos[0] - x, event.pos[1] - y)

        # Now update each button respectively.
        self.__easy.update(event)
        self.__medium.update(event)
        self.__hard.update(event)
        self.__impossible.update(event)
        self.__back.update(event)

        # Check if their states have changed and respectively change the state
        # of the menu.
        if self.__easy.clicked:
            self.__clicked = EASY_DEPTH # SINGLE PLAYER BUTTON CLICKED
        elif self.__medium.clicked:
            self.__clicked = MEDIUM_DEPTH # MULTI PLAYER BUTTON CLICKED
        elif self.__hard.clicked:
            self.__clicked = HARD_DEPTH # QUIT BUTTON CLICKED
        elif self.__impossible.clicked:
            self.__clicked = IMPOSSIBLE_DEPTH
        elif self.__back.clicked:
            self.__exit = True

    def draw(self):
        self.__screen.fill((0, 0, 85))
        self.__title.draw()
        self.__sub_title.draw()
        self.__menu.fill(self.menu_bg)
        self.__easy.draw()
        self.__medium.draw()
        self.__hard.draw()
        self.__impossible.draw()
        self.__back.draw()
        self.__screen.blit(self.__menu, self.__menu_rect)
        pygame.display.update()


    def __clear(self):
        self.__screen.fill(black)
        # Reset the state
        self.__clicked = False
        self.__exit = False

    def main(self, current_depth):
        """
        Displays the main menu and returns an int representing the button
        pressed.
        """
        # Clear the screen before drawing.
        self.__clear()

        # Change the sub title text
        self.__sub_title.text = "Current difficulty: {}".format(self.get_difficulty_from_depth(current_depth))

        while not (self.__clicked or self.__exit):
            for event in pygame.event.get():
                if event.type == QUIT: # User wants to exit the game.
                    exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.__exit = True
                elif event.type == MOUSEMOTION or event.type == MOUSEBUTTONUP:
                    self.update(event)
            self.draw()

        if self.__exit:
            return current_depth

        return self.__clicked
