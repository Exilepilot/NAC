import pygame

class Title:
    """
    Description: A simple title widget class.
    """
    def __init__(self, pygSurface, font, text="", x=0, y=0,
                 centered=True, bold = True, fg=(255, 255, 255),
                 bg=None):
        """
        Params: pygSurface - A pygame surface the title will be drawn on.
                font - A pygame font which will be used to render the text.
                text - The title text.
                x, y - The position of title relative to the pygame surface given.
                centered - The title's centerx and centery will be positioned exactly on the x, y coordinates given.
                bold - Will the title's font be set to bold?
                fg - The foreground colour of the title, i.e. the text colour.
                bg - The background colour of the title, i.e. The surface which contains the text.
        """
        # Fields
        self.__root = pygSurface
        self.__title = None
        self.__title_rect = None
        self.__font = font
        self.text = text
        self.position = x, y
        self.centered = centered
        self.bold = bold
        self.colours = fg, bg

    def draw(self):
        """
        Draws one iteration of the title.
        """
        # Set the font bold, if true.
        self.__font.set_bold(self.bold)

        # Render the title.
        fg, bg = self.colours
        self.__title = self.__font.render(self.text, 1, fg, bg)
        self.__title_rect = self.__title.get_rect()

        x, y = self.position
        # Position the title.
        if self.centered:
            self.__title_rect.centerx = x
            self.__title_rect.centery = y
        else:
            self.__title_rect.x = x
            self.__title_rect.y = y

        # Blit to the root surface.
        self.__root.blit(self.__title, self.__title_rect)
