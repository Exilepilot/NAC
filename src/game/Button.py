"""
Pygame button widget.
Author: Ricky Claven.
"""
# TODO: Mouse position from event queue is relative to screen.
import pygame
from pygame.locals import *



class Button:
    def __init__(self, pygSurface, font, width, height, x=0, y=0, text="",
                 centered=False,
                 bg=((0, 0, 0), (255, 255, 255)),
                 fg=((255, 255, 255), (0, 0, 0))):
        """
        Create button object on existing pygame.Surface
        Params: pygSurface, pygame.Surface, The surface to draw button onto.
        Params: font, pygame.font.Font, The font to render text with.
        Params: width, height, int, int, The dimensions of the button.
        Params: x, y, int, int, The position of the button.
        Params: text, str, The text rendered on the button.
        Params: centered, boolean, Center the button at position (x, y).
        Params: bg, tuple of (tuple, tuple),
            Contains the bg colours of the button including
            when the button is active (when mouse hovers over widget).
        Params: fg, tuple of (tuple, tuple)
            Contains the fg colours of the button including
            when the button is active (when mouse hovers over widget).
        """
        ###################
        # Check the types...
        ###################
        assert isinstance(pygSurface, pygame.Surface)
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert isinstance(text, str)
        assert isinstance(centered, bool)
        assert isinstance(bg, tuple) and 0 < len(bg) <= 2
        assert isinstance(fg, tuple) and 0 < len(fg) <= 2
        ###################
        # Attributes:
        ###################
        # Drawing stuff
        self.__master = pygSurface
        self.__font = font
        self.__pos = x, y
        self.__size = width, height
        # Button text.
        self.__text = text
        # Button positioning
        self.__centered = centered
        # Button colours.
        self.__bg = bg
        self.__fg = fg
        # True when mouse is hovered over widget.
        self.__active = False
        # True when mouse is clicked.
        self.__clicked = False
        # True when button is visible.
        self.__visible = True

        self.__button = pygame.Surface(self.__size)
        self.rect = self.__button.get_rect()

    def update(self, event):
        """
        Takes a pygame event and updates the buttons state.
        """
        # assert isinstance(event, pygame.event.Event)
        self.__clicked = self.__active = False

        if event.type == MOUSEMOTION:
            #event.pos = event.pos[0] - self.rect.x, event.pos[1] - self.rect.y
            if self.rect.collidepoint(event.pos):
                self.__active = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            # event.pos = event.pos[0] - self.rect.x, event.pos[1] - self.rect.y
            if self.rect.collidepoint(event.pos):
                self.__clicked = True

    def draw(self):
        ###################
        # Draw the button
        ###################
        if not self.__visible:
            return

        # Change colours when active.
        text_colour = self.__fg[0] if not self.__active else self.__fg[1]
        bg_colour = self.__bg[0] if not self.__active else self.__bg[1]

        # Create the button surface.
        self.__button.fill(bg_colour)

        # Place the button surface in the specified position.
        if self.__centered:
            self.rect.centerx = self.__pos[0]
            self.rect.centery = self.__pos[1]
        else:
            self.rect.x = self.__pos[0]
            self.rect.y = self.__pos[1]

        # Render the text.
        self.__button_text = self.__font.render(self.__text, 1, text_colour)
        self.__button_text_rect = self.__button_text.get_rect()

        width, height = self.__size
        # Place the text in the middle of the surface.
        self.__button_text_rect.centerx = width // 2
        self.__button_text_rect.centery = height // 2

        # Draw text on button surface.
        self.__button.blit(self.__button_text, self.__button_text_rect)

        # Draw button surface on pygame surface.
        self.__master.blit(self.__button, self.rect)

    def reset(self):
        self.__clicked = self.__active = False

    def set_visible(self, visible):
        if self.__visible != visible:
            self.__visible = visible

    @property
    def clicked(self):
        return self.__clicked

    @property
    def active(self):
        return self.__active
