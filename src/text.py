# Text Class
#
# this class defines an object which abstracts drawing text to the screen
# based on pygames text functionality
#
# created by MKD

import pygame

class Text(object):
    """Class which stores all attributes required to print text,
and abstracts drawing it to the screen"""

    def __init__(self, text="Text", font=None, size=25, aliasing=True,
                 color=(0, 0, 0), pos=(0, 0)):
        self.__text = text
        self.__font = pygame.font.Font(font, size)
        self.rect = pygame.rect.Rect(pos, (0, 0))
        self.__aliasing = aliasing
        self.__color = color

        self.__updateRender()

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, newText):
        self.__text = newText
        self.__updateRender()

    @property
    def color(self):
        return self.__color
    @color.setter
    def color(self, newColor):
        self.__color = newColor
        self.__updateRender()

    def __updateRender(self):
        """Recreates the surface and the rect defining it."""
        self.__surface = self.__font.render(self.__text, self.__aliasing,
                                            self.__color)
        self.rect.size = self.__surface.get_rect().size


    def draw(self, screen):
        """Draws the text to the screen based on attributes values"""
        screen.blit(self.__surface, self.rect)

if __name__ == "__main__":
    print("You ran this file instead of importing it, very bad...")
    input("Press enter to exit...")
