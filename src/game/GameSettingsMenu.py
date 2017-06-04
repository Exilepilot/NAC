"""
A menu that lets the user choose who plays first.
"""
#TODO: Finish this and make sure it works.
import pygame

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

class GameSettingsMenu:
    left_button_fg = (light_red, red)
    left_button_bg = (black, white)
    right_button_fg = (light_orange, orange)
    right_button_bg = (black, white)
    def __init__(self, screen):
        """
        params: screen - The pygame.display surface.
        """
        self.__screen = screen
        self.__font = pygame.font.Font(pygame.font.match_font("Topaz-8"), 25)

        self.__title_font = pygame.font.Font(pygame.font.match_font("Topaz-8"), 30)
        self.__title = Title(self.__screen, self.__title_font,
                             "Who goes first?", 300, 50, True, True)
        # Create buttons
        self.__left_bttn = Button(self.__screen, self.__font, 190, 50, 200, 300,
                                  "YOU", True, self.left_button_bg,
                                  self.left_button_fg)

        self.__right_bttn = Button(self.__screen, self.__font, 190, 50, 400, 300,
                                  "COMPUTER", True, self.right_button_bg,
                                  self.right_button_fg)

    def draw(self):
        self.__screen.fill(blue)
        self.__title.draw()
        self.__left_bttn.draw()
        self.__right_bttn.draw()
        pygame.display.update()

    def update(self, event):
        # Reset state of the menu
        self.__clicked = False

        self.__left_bttn.update(event)
        self.__right_bttn.update(event)

        if self.__left_bttn.clicked:
            self.__clicked = 1
        elif self.__right_bttn.clicked:
            self.__clicked = 2

    def __clear(self):
        self.__screen.fill(black)
        self.__clicked = False

    def main(self):
        self.__clear()
        while not self.__clicked:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return False
                elif event.type == MOUSEMOTION or event.type == MOUSEBUTTONUP:
                    self.update(event)
            self.draw()
        return self.__clicked
