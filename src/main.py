# Main game file
#
# this file has the main loop and the game code

import pygame, snake, food, text, highScores, sys

# first scene the player is greeted with
def mainMenuScene(state, screen, gameClock, diffSelection, difficulties):
    """the first scene the player sees, allows them to enter their name"""

    # center of the window
    CENTERX = screen.get_width() / 2
    CENTERY = screen.get_height() / 2

    # define the two colors used in the menu
    SELECTEDCOLOR = (0, 255, 100)
    BLACKCOLOR = (0, 0, 0)
    
    # defines index of currently selected item
    menuSelection = 0

    # title text with name of game
    titleText = text.Text("SNAKE", color=(0, 255, 0), size=50)
    titleText.rect.center = (CENTERX, 100)

    namePromptText = text.Text("Please enter your name:", color=SELECTEDCOLOR)
    namePromptText.rect.center = (CENTERX, 200)

    # text object for the name the user enters
    # string is made in nameString first, then given to name
    nameText = text.Text(pos=(CENTERX, 250))
    nameString = ""

    # define the text objects for the difficulty menu item
    # and it's selection, also diffSelection for identifying the
    # difficulty the player has chosen
    difficultyText = text.Text(text="Difficulty")
    difficultyText.rect.center = (CENTERX, CENTERY + 50)
    diffSelectionText = text.Text(text=difficulties[diffSelection])
    diffSelectionText.rect.center = (CENTERX, CENTERY + 100)

    # used to allow easy control of menu items, while being
    # expandable and flexible for more options
    menuItems = (namePromptText, difficultyText)

    # nice arrows on the side to show the user they can click
    # left and right to change the difficulty
    cx = diffSelectionText.rect.centerx
    cy = diffSelectionText.rect.centery
    leftTrianglePosList = [(cx - 75, cy), (cx - 50, cy - 10), (cx - 50, cy + 10)]
    rightTrianglePosList = [(cx + 75, cy), (cx + 50, cy + 10), (cx + 50, cy - 10)]

    noNameMsgText = None
    
    while state == 0:

        gameClock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = -1
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not len(nameString) == 0:
                        state = 1
                        break
                    noNameMsgText = text.Text("You must enter a name to continue")
                    noNameMsgText.rect.center = (CENTERX, 500)
                elif event.key == pygame.K_ESCAPE:
                    state = -1
                    break
                elif event.key == pygame.K_BACKSPACE:
                    nameString = nameString[:-1]
                elif event.key == pygame.K_SPACE:
                    nameString += " "
                # only letters and numbers allowed
                # only allow if string is not already too long
                # uppercase letters, lowercase letters, numbers
                elif event.key in range(97, 122) or event.key in range(48, 57):
                    if not len(nameString) == 10:
                        nameString += pygame.key.name(event.key)

                # manages the keyboard input when it comes to navigating the menu
                elif event.key == pygame.K_UP:
                    if menuSelection == 0:
                        menuItems[menuSelection].color = BLACKCOLOR
                        menuSelection = len(menuItems) - 1
                        menuItems[menuSelection].color = SELECTEDCOLOR
                    else:
                        menuItems[menuSelection].color = BLACKCOLOR
                        menuSelection -= 1
                        menuItems[menuSelection].color = SELECTEDCOLOR
                elif event.key == pygame.K_DOWN:
                    if menuSelection == (len(menuItems) - 1):
                        menuItems[menuSelection].color = BLACKCOLOR
                        menuSelection = 0
                        menuItems[menuSelection].color = SELECTEDCOLOR
                    else:
                        menuItems[menuSelection].color = BLACKCOLOR
                        menuSelection += 1
                        menuItems[menuSelection].color = SELECTEDCOLOR
                elif menuSelection == 1:
                    if event.key == pygame.K_LEFT:
                        if diffSelection == 0:
                            diffSelection = len(difficulties) - 1
                            diffSelectionText.text = difficulties[diffSelection]
                        else:
                            diffSelection -= 1
                            diffSelectionText.text = difficulties[diffSelection]
                    elif event.key == pygame.K_RIGHT:
                        if diffSelection == len(difficulties) - 1:
                            diffSelection = 0
                            diffSelectionText.text = difficulties[diffSelection]
                        else:
                            diffSelection += 1
                            diffSelectionText.text = difficulties[diffSelection]

        nameText.text = nameString
        # if the text has changed in size, this keeps it centered
        nameText.rect.centerx = CENTERX

        screen.fill((0, 150, 255))
        titleText.draw(screen)
        for option in menuItems:
            option.draw(screen)
        diffSelectionText.draw(screen)
        nameText.draw(screen)
        # if there is a noNameMsg object then call it's draw function
        if noNameMsgText:
            noNameMsgText.draw(screen)
        pygame.draw.polygon(screen, (0, 255, 0), leftTrianglePosList)
        pygame.draw.polygon(screen, (0, 255, 0), rightTrianglePosList)

        pygame.display.flip()

    return state, nameString, diffSelection

# runs when the game is running
def gameScene(state, screen, frameTime, gameClock, diff):
    """this is called when it's time to play the game,
returns the new screen state"""
    # set up player and the game map
    mapRect = pygame.rect.Rect(50, 50, 700, 500)
    player = snake.Snake()
    fruit = food.Food(player.bodyList)
    if diff == 0:
        cooldown = 100
    elif diff == 1:
        cooldown = 75
    elif diff == 2:
        cooldown = 50
    else:
        print("Difficulty selection failed, check the code")
    growSnake = False

    # initialises the score, as well as the font and the rect
    # which is used to define position and size of text (required for drawing)
    score = 0
    scoreText = text.Text("Score: " + str(score), color=(100, 0, 100))

    framesPerSec = text.Text()
    framesPerSec.rect.bottomleft = (0, 600)

    # main game loop of the game, only quits at change of game scene state
    while state == 1:

        frameTime += gameClock.tick(60)
        
        # logic updates
        if fruit.eaten(player):
            fruit.spawnFood()
            
            score += 10
            scoreText.text = "Score: " + str(score)

            growSnake = True

        # will only displace the snake if the cooldown is over
        if frameTime >= cooldown:    
            growSnake, state = player.update(growSnake, state, mapRect)
            frameTime = 0
        
        framesPerSec.text = str(gameClock.get_fps())[:6]

        # drawing to the screen
        screen.fill((0, 150, 255))
        
        pygame.draw.rect(screen, (0, 0, 0), mapRect, 3)
        
        player.draw(screen)
        fruit.draw(screen)
        scoreText.draw(screen)
        framesPerSec.draw(screen)
        
        pygame.display.flip()

    return state, score


# runs when the high score scene is showing
def highScoreScene(state, screen, name, newScore, gameClock, diff, difficulties):
    """manages the high score scene, returns the new screen state"""

    # since diff is passed by value, it is used for representing which
    # diffculty table the player is on and changing it won't cause any problems

    # center of the window
    CENTERX = screen.get_width() / 2
    CENTERY = screen.get_height() / 2
    
    # surface for the title, it is centered and is of greater font size
    title = text.Text("HIGH SCORES", size=40, pos=(0, 100), color=(0, 255, 0))
    title.rect.x = CENTERX - (title.rect.w / 2)

    # text objects for player info, shows players name and score
    playerInfoString = "Name: " + name + "    Score: " + str(newScore) + "  on " + difficulties[diff]
    playerInfoText = text.Text(playerInfoString, size=30)
    playerInfoText.rect.center = (CENTERX, 150)

    # surface for the play again prompt
    spaceToCont = text.Text("Press Space to play again", size=30,
                            pos=(0, 550))
    spaceToCont.rect.x = CENTERX - (spaceToCont.rect.w / 2)

    # if the players score gets added to list then create
    # a congratulation message otherwsie a get better message
    highScores.addNewScore(name, newScore, difficulties[diff])

    tableSurface = createHighScoresTable(difficulties[diff])

    # nice arrows on the side to show the user they can click
    # left and right to change the difficulty
    leftTrianglePosList = [(CENTERX - 175, CENTERY), (CENTERX - 150, CENTERY - 10), (CENTERX - 150, CENTERY + 10)]
    rightTrianglePosList = [(CENTERX + 175, CENTERY), (CENTERX + 150, CENTERY + 10), (CENTERX + 150, CENTERY - 10)]

    while state == 2:

        gameClock.tick(60)

        # checks for key entries to play again or exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = -1
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = -1
                elif event.key == pygame.K_SPACE:
                    state = 0

                elif event.key == pygame.K_LEFT:
                    if diff == 0:
                        diff = len(difficulties) - 1
                    else:
                        diff -= 1
                    tableSurface = createHighScoresTable(difficulties[diff])
                elif event.key == pygame.K_RIGHT:
                    if diff == len(difficulties) - 1:
                        diff = 0
                    else:
                        diff += 1
                    tableSurface = createHighScoresTable(difficulties[diff])


        screen.fill((0, 150, 255))
        
        title.draw(screen)
        playerInfoText.draw(screen)
        # passing the parameter below to get_rect makes the rect center
        # at those coordinates
        screen.blit(tableSurface, tableSurface.get_rect(center=(CENTERX, CENTERY)))
        pygame.draw.polygon(screen, (0, 255, 0), leftTrianglePosList)
        pygame.draw.polygon(screen, (0, 255, 0), rightTrianglePosList)
        spaceToCont.draw(screen)

        pygame.display.flip()

    return state

def createHighScoresTable(level):
    """goes through every high score in shelf level and blits each one to
    one surface to be rendered in one go"""
    # surface for the scores, only one surface is needed
    # and all scores are blitted to that surface
    # they are then blitted to the window surface at once
    # there are 5 texts of size 25, 1 of size 30
    # the large one is seprated by 15 pixels
    surface = pygame.Surface((300, 30 * 6 + 15))
    surface.fill((0, 150, 255))
    # this is for showing the difficulty level of the table
    # at the top of the table, it is centered at the top (see code below)
    levelText = text.Text(level, size=30)

    leaderboards = highScores.getScores()
    TABLECENTERX = surface.get_width() / 2
    # accomodates for the size of the font
    scorePosY = 15
    
    levelText.rect.center = (TABLECENTERX, scorePosY)
    levelText.draw(surface)
    # spacing between this text and the actual table
    scorePosY += 30
    for score in leaderboards[level]:
        # positions are set relative to the tableSurface
        nameText = text.Text(text=score[0])
        nameText.rect.topright = (TABLECENTERX - 10, scorePosY)
        
        scoreText = text.Text(text=str(score[1]))
        scoreText.rect.topleft = (TABLECENTERX + 10, scorePosY)

        nameText.draw(surface)
        scoreText.draw(surface)

        scorePosY += 30

    return surface

# main function which runs the game loop
def main():
    """This function has the main loop of the program"""
    pygame.init()

    # clock object that is used for time of the game
    clock = pygame.time.Clock()
    frameTime = 0

    # initialise the surface of the game
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snake")

    # defines the game screen state
    screenState = 0

    # strings of all difficulties, required in main menu
    # and in high score to access shelf
    diffOptions = ("Slow", "Medium", "Fast")
    difficulty = 1

    # initialise the high scores file
    highScores.initScores(diffOptions)
    playerName = ""
    playerScore = 0

    # when the screenState is < 0 the game quits
    while not (screenState < 0):
        # when screenState is 0 it's main menu
        if screenState == 0:
            screenState, playerName, difficulty = mainMenuScene(screenState, screen, clock, difficulty, diffOptions)
        # when screenState is 1 time to play
        if screenState == 1:
            screenState, playerScore = gameScene(screenState, screen, frameTime, clock, difficulty)
        # when screenState is 2 high score screen
        if screenState == 2:
            screenState = highScoreScene(screenState, screen, playerName, playerScore, clock, difficulty, diffOptions)

    pygame.quit()


main()