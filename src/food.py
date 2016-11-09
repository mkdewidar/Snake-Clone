# Food Class
#
# this class is for the food in the snake game

import pygame, random, math

class Food(object):
    """Class that defines the attributes and functions for the snakes food"""

    def __init__(self, snakeBody):
        self.__radius = 5
        self.spawnFood()

    def spawnFood(self):
        # randomly chooses position, those values ensure the food will
        # be spawned in a position the player can move to
        # and also makes sure it doesn't create food over the player
        x = random.randrange(55, 705, 10)
        y = random.randrange(55, 505, 10)

        self.__centerPos = (x, y)

    def draw(self, screen):
        """Manages drawing the food onto the screen"""
        pygame.draw.circle(screen, (0, 255, 0), self.__centerPos, self.__radius)

    def eaten(self, player):
        """Checks whether its been eaten or not"""
        # creates a rect out of circle attributes to check collision
        # with the snakes body
        x = self.__centerPos[0] - self.__radius
        y = self.__centerPos[1] - self.__radius
        foodRect = pygame.rect.Rect(x, y, self.__radius * 2, self.__radius * 2)
        
        return player.bodyList[len(player.bodyList) - 1].colliderect(foodRect)


if __name__ == "__main__":
    print("This is a module, it should be imported not executed.")
    input("Press enter to exit...")
