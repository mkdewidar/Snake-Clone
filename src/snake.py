# Snake Class
#
# a class for the snake

import pygame

class Snake(object):
    """A class for the snake that the player plays as"""

    def __init__(self):
        """Defines the snake attributes"""
        self.__displacement = (10, 0)
        # first element is the tail of the snake
        # last element is the head
        self.bodyList = [pygame.rect.Rect(50, 50, 10, 10),
                         pygame.rect.Rect(60, 50, 10, 10),
                         pygame.rect.Rect(70, 50, 10, 10)]
        self.grow = False

    def update(self, extend, sceneState, playArea):
        """Executes game logic, returns opposite of extend to show it grew"""
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sceneState = -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sceneState = -1
                if event.key == pygame.K_UP and self.__displacement != (0, 10):
                    self.__displacement = (0, -10)
                    break
                if event.key == pygame.K_LEFT and self.__displacement != (10, 0):
                    self.__displacement = (-10, 0)
                    break
                if event.key == pygame.K_DOWN and self.__displacement != (0, -10):
                    self.__displacement = (0, 10)
                    break
                if event.key == pygame.K_RIGHT and self.__displacement != (-10, 0):
                    self.__displacement = (10, 0)
                    break

        # pops the tail off
        # updates the coordinates such that it takes the lead
        # append it to the list so that it is the head.
        if extend:
            newHead = pygame.rect.Rect(0, 0, 10, 10)
            extend = False
        else:
            newHead = self.bodyList.pop(0)

        lastItemIndex = len(self.bodyList) - 1
        newHead.x = self.bodyList[lastItemIndex].x + self.__displacement[0]
        newHead.y = self.bodyList[lastItemIndex].y + self.__displacement[1]
            
        self.bodyList.append(newHead)

        # checks if the snake head overlaps another part of the body
        # or if snake leaves the play area
        if self.bodyList[lastItemIndex] in self.bodyList[:lastItemIndex] or not playArea.contains(self.bodyList[lastItemIndex]):
            sceneState = 2
                       
        return extend, sceneState

    def draw(self, screen):
        """"Function that handles drawing the snake to the screen"""
        for part in self.bodyList:
            pygame.draw.rect(screen, (0, 0, 0), part)



if __name__ == "__main__":
    print("This file is a class file, it should be imported not run")
    input("Press enter to exit...")
