"""
Pygame main menu
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


class MainMenu:
    """
    Decription: The main menu for the game.
    Usage: Once the main function is called, the main menu will display itself.
    When a user clicks on a button, the main function will return an integer value.
    The integer value will correspond to the button which the user clicked.
    """
    # Menu size, positioning, and colours.
    menu_size = 400, 300 # Dimensions of the surface containing the buttons.
    menu_pos = menu_x, menu_y = (100, 150) # The position of the menu surface.
    menu_bg = blue # Menu colours
    menu_fg = white

    # Multiplayer button colours.
    mp_button_bg = (light_red, red)
    mp_button_fg = (black, white)

    # Single player button colours.
    sp_button_bg = (light_green, green)
    sp_button_fg = (black, white)

    # Settings button colours.
    settings_button_bg =(light_navy, navy)
    settings_button_fg = (black, white)

    # Quit button colours.
    quit_button_bg = (light_orange, orange)
    quit_button_fg = (black, white)

    def __init__(self, screen):
        """
        Create pygame main menu widget.
        Params: screen, An initialised pygame.display.
        """
        self.__screen = screen
        self.__font = pygame.font.Font(pygame.font.match_font("Topaz-8"), 25)

        # Create the menu.
        self.__menu = pygame.Surface(self.menu_size)
        self.__menu_rect = self.__menu.get_rect()
        self.__menu_rect.x = self.menu_x
        self.__menu_rect.y = self.menu_y

        # Set the title bold to stand out.
        self.__title_font = pygame.font.Font(pygame.font.match_font("Topaz-8"), 50)

        # Create the title.
        self.__title = Title(self.__screen, self.__title_font, "TIC TAC TOE",
                             300, 50, True, True)

        # Positioning of the buttons
        x_offset = 20
        y_offset = 75
        b_width = 360
        b_height = 75

        # VERSUS AI BUTTON
        self.__sp = Button(self.__menu, self.__font, b_width, b_height, x_offset, 0,
                           "VERSUS A.I", False,
                           self.sp_button_bg, self.sp_button_fg)
        # VERSUS HUMAN BUTTON
        self.__mp = Button(self.__menu, self.__font, b_width, b_height,
                           x_offset, y_offset,
                           "VERSUS HUMAN", False,
                           self.mp_button_bg, self.mp_button_fg)
        # SETTINGS button
        self.__settings = Button(self.__menu, self.__font, b_width, b_height,
                                 x_offset, y_offset * 2 ,
                                 "A.I SETTINGS", False,
                                 self.settings_button_bg,
                                 self.settings_button_fg)
        # QUIT BUTTON
        self.__quit = Button(self.__menu, self.__font,
                             b_width, b_height, x_offset, y_offset * 3,
                             "QUIT", False,
                             self.quit_button_bg, self.quit_button_fg)

        # Set true if clicked.
        self.__clicked = False

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
        self.__sp.update(event)
        self.__mp.update(event)
        self.__settings.update(event)
        self.__quit.update(event)

        # Check if their states have changed and respectively change the state
        # of the menu.
        if self.__sp.clicked:
            self.__clicked = 1 # SINGLE PLAYER BUTTON CLICKED
        elif self.__mp.clicked:
            self.__clicked = 2 # MULTI PLAYER BUTTON CLICKED
        elif self.__settings.clicked:
            self.__clicked = 3
        elif self.__quit.clicked:
            self.__clicked = 4 # QUIT BUTTON CLICKED

    def draw(self):
        self.__screen.fill((0, 0, 85))
        self.__title.draw()
        self.__menu.fill(self.menu_bg)
        self.__sp.draw()
        self.__mp.draw()
        self.__settings.draw()
        self.__quit.draw()
        self.__screen.blit(self.__menu, self.__menu_rect)
        pygame.display.update()


    def __clear(self):
        self.__screen.fill(black)
        self.__clicked = False

    def main(self):
        """
        Displays the main menu and returns an int representing the button
        pressed.
        """
        self.__clear()
        while not self.__clicked:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == MOUSEMOTION or event.type == MOUSEBUTTONUP:
                    self.update(event)
            self.draw()
        return self.__clicked
