#Dev Patel
#ICS3U
#Mr. Greco
#Wednesday, January 22nd, 2020
#Yoda (User 1) and Chewbacca (User 2) must defeat every wave of Darth Vaders that come their way in outer space, using a laser gun! This program includes a menu, high score list, instructions page, and includes the game.

#------------------------------------------------------------------------
#Libraries
#------------------------------------------------------------------------
import pygame, sys, time
from pygame.locals import *
from pygame.constants import *
from pygame import mixer

import random
import math

#------------------------------------------------------------------------
#Initial Variables
#------------------------------------------------------------------------
programName = "YODA & CHEWBACCA vs. VADER ARMY!"
windowSize = (800, 575)
clock = pygame.time.Clock()
fps = 60 #FPS means "Frames per second".

#------------------------------------------------------------------------
#Initialization
#------------------------------------------------------------------------
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode(windowSize)
pygame.display.set_caption(programName)

#------------------------------------------------------------------------
#More Variables
#------------------------------------------------------------------------

#Font sizes that will be used on words based on significance.
titleFont = pygame.font.Font('freesansbold.ttf', 70)
primaryFont = pygame.font.Font('freesansbold.ttf', 55)
secondaryFont = pygame.font.Font('freesansbold.ttf', 40)
smallFont = pygame.font.Font('freesansbold.ttf', 35)

#Load the background and scale the image to fit the window size.
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (800, 575))

laserSound = pygame.mixer.Sound('laser.wav')

#Set the variable to display the menu to True and all other variables to display all other pages to False when the game starts. Other pages will be set to True when the user chooses to view the page.
showMenu = True
displayInstructions = False
playGame = False
playAgain = False
showHighScores = False

#COLOURS
colourRed = pygame.Color(255, 0, 0)
colourGreen = pygame.Color(0, 255, 0)
colourBlue = pygame.Color(0, 0, 255)
colourBlack = pygame.Color(0, 0, 0)
colourWhite = pygame.Color(255, 255, 255)

#Set a list of scores to be sorted and chosen from in the high scores listing. Set a variable to draw on the game screen as the high score.
scores = []
highScore = 0

scorePosX = 10
scorePosY = 10

#------------------------------------------------------------------------
#Functions
#------------------------------------------------------------------------
def windowUpdate():
    '''This function runs the functions that update the window. The purpose of this function is to avoid repeating the window update functions (less lines).'''

    pygame.display.update()
    clock.tick(fps)

def resetVariables():
    '''After one game is played, this function resets all of the variables that are changed while the user is playing so they can start a new game without the vaders already being in their territory and repeatedly making them lose.'''

    #Use global to be able to use all variables throughout the program (including within other functions)
    global yodaLaser, yoda, yodaPosX, yodaPosY, yodaVelocityY, chewbacca, chewbaccaPosX, chewbaccaPosY, chewbaccaVelocityY, yodaLaserPosX, yodaLaserPosY, shootYodaLaser, yodaLaserVelX, chewbaccaLaser, chewbaccaLaserNum, chewbaccaLaserPosX, chewbaccaLaserPosY, shootChewbaccaLaser, chewbaccaLaserVelX, score, vaderNumber, yodaLaserNum, vaderPosX, vaderPosY, vaderVelocityY, vader, vaderVelocityX

    #Set up a list of Darth Vaders and populate them with 5 images of Darth Vader to create 5 enemies. Load them in a random position on the page that is reasonable to make the game more interesting and less predictable. Initialize their x and y velocities.
    vader = []
    vaderImage = pygame.transform.scale(pygame.image.load('vader.png'), (100, 100))
    vaderNumber = 5
    vaderPosX = []
    vaderPosY = []
    vaderVelocityX = []
    vaderVelocityY = []

    for i in range(vaderNumber):
        vader.append(vaderImage)
        vaderPosX.append(random.randint(400, 700))
        vaderPosY.append(random.randint(0, 475))
        vaderVelocityX.append(-50)
        vaderVelocityY.append(25)

    #Load Yoda (Player 1) and initialize his position and y velocity (Yoda and Chewbacca can only move up and down, not side-to-side).
    yoda = pygame.transform.scale(pygame.image.load('yoda.png'), (100, 100))
    yodaPosX = 80
    yodaPosY = 192
    yodaVelocityY = 0

    #Load Chewbacca (Player 2) and initialize his position and y velocity.
    chewbacca = pygame.transform.scale(pygame.image.load('chewbacca.png'), (100, 100))
    chewbaccaPosX = 80
    chewbaccaPosY = 384
    chewbaccaVelocityY = 0

    #Make a list of all shadows/blur images of Yoda's laser scaled to a reasonable size, in order of speed from lowest to greatest (shown later in the program).
    yodaLaser = []
    yodaLaser.append(pygame.transform.scale(pygame.image.load('laser.png'), (50, 25)))
    yodaLaser.append(pygame.transform.scale(pygame.image.load('laser1.png'), (50, 25)))
    yodaLaser.append(pygame.transform.scale(pygame.image.load('laser2.png'), (50, 25)))
    yodaLaser.append(pygame.transform.scale(pygame.image.load('laser3.png'), (50, 25)))
    yodaLaser.append(pygame.transform.scale(pygame.image.load('laser4.png'), (50, 25)))
    yodaLaser.append(pygame.transform.scale(pygame.image.load('laser5.png'), (50, 25)))

    #Initilize the position, status, and velocity of Yoda's laser.
    yodaLaserNum = len(yodaLaser)
    yodaLaserPosX = 130
    yodaLaserPosY = yodaPosY + 50

    #The status of Yoda's laser is 0 when it hasn't been shot and 1 when it has.
    shootYodaLaser = 0
    yodaLaserVelX = 100

    #Make a list of all shadows/blur images of Chewbacca's laser scaled to a reasonable size (same as Yoda's list).
    chewbaccaLaser = yodaLaser

    #Initilize the position, status, and velocity of Chewbacca's laser.
    chewbaccaLaserNum = yodaLaserNum
    chewbaccaLaserPosX = 130
    chewbaccaLaserPosY = chewbaccaPosY + 50
    shootChewbaccaLaser = 0
    chewbaccaLaserVelX = 100

    #Start the score at 0 (will reset to 0 after every game).
    score = 0

    #Load the Star Wars sound track and play it as background music.
    mixer.music.load("background.mp3")
    mixer.music.play(-1)

def mainMenuScreen():
    '''This function renders and draws the text that will be displayed on the main menu.'''

    window.fill(colourBlack) #Colours screen black

    #Render the 3 parts of the title.
    title1 = titleFont.render("YODA & CHEWBACCA", True, colourBlue)
    title2 = titleFont.render("VS.", True, colourWhite)
    title3 = titleFont.render("VADER ARMY!", True, colourRed)

    #Render the 4 buttons on the main menu.
    instructionsButton = primaryFont.render("I for Instructions", True, colourWhite)
    gameButton = primaryFont.render("ENTER to Start", True, colourRed)
    highScoreButton = primaryFont.render("H for High Scores", True, colourGreen)
    exitButton = primaryFont.render("ESCAPE to Exit", True, colourBlue)

    #Draw the 3 parts of the game title onto the screen.
    window.blit(title1, (0, 0))
    window.blit(title2, (0, 70))
    window.blit(title3, (0, 140))

    #Draws the 4 buttons onto the screen
    window.blit(instructionsButton, (0, 355))
    window.blit(gameButton, (0, 410))
    window.blit(highScoreButton, (0, 465))
    window.blit(exitButton, (0, 520))

def mainMenu():
    '''This function creates the main menu page and draws it constantly in a while loop. The while loop has events that correspond to the button options displayed on screen, in order to move to different pages.'''

    global displayInstructions, playGame, playAgain, showHighScores, showMenu

    #Pygame menu loop
    while showMenu:

        #---------------------------------------------------------------------
        #Events
        #---------------------------------------------------------------------
        for event in pygame.event.get():

            #Quit the program if the user closes the window.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                #If the user presses I, quit the current while loop that displays the menu, and allow the while loop displaying the instructions page to run.
                if event.key == pygame.K_i:
                    showMenu = False
                    displayInstructions = True

                #If the user presses ENTER/RETURN, quit the while loops that display the menu and instructions pages (set all loops before the game to False), land allow the while loop that plays the game to run.
                if event.key == pygame.K_RETURN:
                    showMenu = False
                    displayInstructions = False
                    playGame = True

                #If the user presses H, quit the while loops that display the menu, instructions page, game, and play again page (set all loops before high score to False), and allow the while loop that displays the high scores to run.
                if event.key == pygame.K_h:
                    showMenu = False
                    displayInstructions = False
                    playGame = False
                    playAgain = False
                    showHighScores = True

                #If the user presses ESCAPE, close the window and quit the program.
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        #---------------------------------------------------------------------
        #Runtime - Use the function to draw all the elements onto the menu screen.
        #---------------------------------------------------------------------
        mainMenuScreen()

        #---------------------------------------------------------------------
        #Window Update
        #---------------------------------------------------------------------
        windowUpdate()

def instructionsScreen():
    '''This function renders and draws all elements for the instructions page.'''

    window.fill(colourBlack)

    #Render all text (including rules and button options) with the corresponding font and colour based on significance/aesthetic.
    startPlaying = primaryFont.render("PRESS ENTER TO PLAY", True, colourRed)

    generalInstructions1 = smallFont.render("Try to shoot as many Darth Vaders as possible!", True, colourWhite)
    generalInstructions2 = smallFont.render("One user is Yoda and the user is Chewbacca!", True, colourWhite)
    generalInstructions3 = smallFont.render("If the Vaders get too close, you lose!", True, colourWhite)

    yodaInstructions1 = smallFont.render("Yoda:", True, colourGreen)
    yodaInstructions2 = smallFont.render("Press 'W' to move up", True, colourGreen)
    yodaInstructions3 = smallFont.render("Press 'S' to move down", True, colourGreen)
    yodaInstructions4 = smallFont.render("Press SPACE bar to shoot!", True, colourGreen)

    chewbaccaInstructions1 = smallFont.render("Chewbacca:", True, colourBlue)
    chewbaccaInstructions2 = smallFont.render("Press UP arrow key to move up", True, colourBlue)
    chewbaccaInstructions3 = smallFont.render("Press DOWN arrow key to move down", True, colourBlue)
    chewbaccaInstructions4 = smallFont.render("Press RIGHT arrow key to shoot!", True, colourBlue)

    backToMenu = primaryFont.render("PRESS ESCAPE FOR MENU", True, colourRed)

    #Draw all rendered text onto the screen in an organized manner (y-values change by constant intervals based on font size of text).
    window.blit(startPlaying, (0, 0))

    window.blit(generalInstructions1, (0, 55))
    window.blit(generalInstructions2, (0, 90))
    window.blit(generalInstructions3, (0, 125))

    window.blit(yodaInstructions1, (0, 160))
    window.blit(yodaInstructions2, (0, 195))
    window.blit(yodaInstructions3, (0, 230))
    window.blit(yodaInstructions4, (0, 265))

    window.blit(chewbaccaInstructions1, (0, 300))
    window.blit(chewbaccaInstructions2, (0, 335))
    window.blit(chewbaccaInstructions3, (0, 370))
    window.blit(chewbaccaInstructions4, (0, 405))

    window.blit(backToMenu, (0, 440))

def showInstructions():
    global playGame, playAgain, showHighScores, showMenu, displayInstructions

    #Pygame instructions page loop
    while displayInstructions:

        #---------------------------------------------------------------------
        #Events
        #---------------------------------------------------------------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                #If the user presses return, exit the instructions page and play the game.
                if event.key == pygame.K_RETURN:
                    displayInstructions = False
                    playGame = True

                #If the user presses escape, exit the instructions page and go back to the main menu.
                if event.key == pygame.K_ESCAPE:
                    displayInstructions = False
                    playGame = False
                    playAgain = False
                    showHighScores = False
                    showMenu = True

        #---------------------------------------------------------------------
        #Runtime - Use the instructionsScreen() function to draw the instructions onto the screen.
        #---------------------------------------------------------------------
        instructionsScreen()

        #---------------------------------------------------------------------
        #Window Update
        #---------------------------------------------------------------------
        windowUpdate()

def drawYoda(x, y):
    '''This function draws Yoda with given arguments as x and y position parameters.'''

    window.blit(yoda, (x, y))

def drawChewbacca(x, y):
    '''This function draws Chewbacca with given arguments as x and y position parameters.'''

    window.blit(chewbacca, (x, y))

def drawVader(index, x, y):
    '''This function draws Darth Vader with given arguments as the index representing it as one of the Vaders in the game, as well as x and y position parameters.'''

    global vader
    window.blit(vader[index], (x, y))

def drawYodaLaser(index, x, y):
    '''This function draws Yoda's laser with given arguments as the index representing each blur image of the laser, as well as x and y position parameters.'''

    global yodaLaser
    window.blit(yodaLaser[index], (x, y))

def drawChewbaccaLaser(index, x, y):
    '''This function draws Chewbacca's laser with given arguments as the index representing each blur image of the laser, as well as x and y position parameters.'''

    window.blit(chewbaccaLaser[index], (x, y))

def collision(vaderPosX, vaderPosY, laserPositionX, laserPositionY):
    '''This function calculates the distance from the laser to Darth Vader and returns True for collision if the distance is reasonably close to Darth Vader.'''

    #Adding 50 to the positions of the Vader identifies a position near the center of the Vader image since it is 100x100 pixels in size.
    distance = math.sqrt(((vaderPosX + 50) - (laserPositionX + 25))**2 + ((vaderPosY + 50) - laserPositionY)**2)

    if distance < 50:
        return True

    #Return False if collision is not reasonable.
    else:
        return False

def displayScore(x, y):
    '''This function renders and draws the scoreboard at the top-left of the screen while the game is being played'''

    scoreText = secondaryFont.render("Score : " + str(score), True, colourWhite)
    window.blit(scoreText, (x, y))

    highScoreText = secondaryFont.render("High Score : " + str(highScore), True, colourWhite)
    window.blit(highScoreText, (x, y + 40))

def game():
    '''This function consists of the Pygame game loop, using events and previous functions to run the game, and adding the finishing score to the list of scores.'''

    global playAgain, vaderNumber, vaderPosX, vaderPosY, vaderVelocityY, vaderVelocityX, yodaLaserNum, textPosX, playGame, yodaPosY, yodaVelocityY, chewbaccaPosY, chewbaccaVelocityY, vaderNumber, shootYodaLaser, shootChewbaccaLaser, yodaLaserPosX, chewbaccaLaserPosX, score, highScore, yodaLaserPosY, chewbaccaLaserPosY, scores, playGameConfirm

    #Initialize the variable that confirms the game being played to False.
    playGameConfirm = False

    #Pygame game loop
    while playGame:

        #When the game is played, set the confirmation variable to True.
        playGameConfirm = True

        #---------------------------------------------------------------------
        #Events
        #---------------------------------------------------------------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                #When the W key is pressed, make the velocity of Yoda negative so he moves upwards.
                if event.key == pygame.K_w:
                    yodaVelocityY = -25

                #When the S key is pressed, make the velocity of Yoda positive so he moves downwards.
                if event.key == pygame.K_s:
                    yodaVelocityY = 25

                #If the SPACE button is pressed and if Yoda's laser hasn't been shot already, update its y position corresponding to Yoda, confirm the laser has been shot, and play the laser sound.
                if event.key == pygame.K_SPACE:
                    if shootYodaLaser == 0:
                        yodaLaserPosY = yodaPosY + 50
                        shootYodaLaser = 1
                        laserSound.play()

                #When the UP arrow key is pressed, make the velocity of Chewbacca negative so he moves upwards.
                if event.key == pygame.K_UP:
                    chewbaccaVelocityY = -25

                #When the DOWN arrow key is pressed, make the velocity of Chewbacca positive so he moves downwards.
                if event.key == pygame.K_DOWN:
                    chewbaccaVelocityY = 25

                #If the RIGHT button is pressed and if Chewbacca's laser hasn't been shot already, update its y position corresponding to Chewbacca, confirm the laser has been shot, and play the laser sound.
                if event.key == pygame.K_RIGHT:
                    if shootChewbaccaLaser == 0:
                        chewbaccaLaserPosY = chewbaccaPosY + 50
                        shootChewbaccaLaser = 1
                        laserSound.play()

            if event.type == pygame.KEYUP:
                #Set Yoda's velocity back to 0 when the W or S keys have been released so the Yoda icon stops moving.
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    yodaVelocityY = 0

                #Set Chewbacca's velocity back to 0 when the UP or DOWN arrow keys have been released so the Chewbacca icon stops moving.
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    chewbaccaVelocityY = 0

        #---------------------------------------------------------------------
        #Runtime
        #---------------------------------------------------------------------

        #Draw the background onto the screen.
        window.blit(background, (0, 0))

        #Add Yoda's velocity to his y position so he can move up or down based on the key pressed.
        yodaPosY += yodaVelocityY

        #Set the y position of Yoda to 0 if his y position is less than 0, so he cannot leave from the top of the screen.
        if yodaPosY < 0:
            yodaPosY = 0

        #Set the y position of Yoda to 475 if his position is greater than 475 so he cannot leave from the top of the screen.
        elif yodaPosY > 475:
            yodaPosY = 475

        chewbaccaPosY += chewbaccaVelocityY

        if chewbaccaPosY < 0:
            chewbaccaPosY = 0

        elif chewbaccaPosY > 475:
            chewbaccaPosY = 475

        #For every vader (i represents the index of each element in the Vader list)...
        for i in range(vaderNumber):

            #End the game and start the playAgain page if the Vader army gets too close to Chewbacca and Yoda and infiltrates their base!
            if vaderPosX[i] < 180:
                playGame = False
                playAgain = True

            #Add the velocity of the Vaders to each vader to make them move up and down.
            vaderPosY[i] += vaderVelocityY[i]

            #If the Vader hits the top of the screen, add its x velocity to its x position to move it closer to Yoda and Chewbacca, and make its velocity positive to make it move downwards.
            if vaderPosY[i] < 0:
                vaderVelocityY[i] *= -1
                vaderPosX[i] += vaderVelocityX[i]

            #If the vader hits the bottom of the screen, do the same as above and make its velocity negative to make it move upwards.
            elif vaderPosY[i] > 475:
                vaderVelocityY[i] *= -1
                vaderPosX[i] += vaderVelocityX[i]

            #Determine if Yoda's laser is colling with the Vader.
            yodaLaserCollision = collision(vaderPosX[i], vaderPosY[i], yodaLaserPosX, yodaLaserPosY)

            #If Yoda's laser is colliding with Vader, reset the position of Yoda's laser, update its status to not being shot, add 1 to the score, and spawn the Vader in a random place on the window.
            if yodaLaserCollision:
                yodaLaserPosX = 130
                shootYodaLaser = 0
                score += 1
                vaderPosX[i] = random.randint(400, 700)
                vaderPosY[i] = random.randint(0, 475)

                #Each time a vader is hit, increase the velocity of all vaders by 1 (increases difficulty as the game goes on).
                for i in range(len(vaderVelocityY)):
                    if vaderVelocityY[i] > 0:
                        vaderVelocityY[i] += 1
                    else:
                        vaderVelocityY[i] -= 1

            chewbaccaLaserCollision = collision(vaderPosX[i], vaderPosY[i], chewbaccaLaserPosX, chewbaccaLaserPosY)

            if chewbaccaLaserCollision:
                chewbaccaLaserPosX = 130
                shootChewbaccaLaser = 0
                score += 1
                vaderPosX[i] = random.randint(400, 700)
                vaderPosY[i] = random.randint(0, 475)

                for i in range(len(vaderVelocityY)):
                    if vaderVelocityY[i] > 0:
                        vaderVelocityY[i] += 1
                    else:
                        vaderVelocityY[i] -= 1

            #Draw the vader using its updated positions.
            drawVader(i, vaderPosX[i], vaderPosY[i])

        #If the laser has been shot, add its velocity to its position to make it move toward the Vaders.
        if shootYodaLaser == 1:
            yodaLaserPosX += yodaLaserVelX

            #Draw each blur image of the laser, with the darkest blurs slower than the lighter blurs to create a motion blur effect.
            for i in range(yodaLaserNum):
                drawYodaLaser(i, yodaLaserPosX - int(i * yodaLaserPosX * 0.075) - (i * 12), yodaLaserPosY)

        if shootChewbaccaLaser == 1:
            chewbaccaLaserPosX += chewbaccaLaserVelX

            for i in range(chewbaccaLaserNum):
                drawChewbaccaLaser(i, chewbaccaLaserPosX - int(i * chewbaccaLaserPosX * 0.075) - (i * 12), chewbaccaLaserPosY)

        #If the laser exits out of the screen, reset its x position and status to not being shot so it can be shot again (so it doesn't continue infinitely and inhibit the user from shooting another laser).
        if yodaLaserPosX > 800:
            yodaLaserPosX = 130
            shootYodaLaser = 0

        if chewbaccaLaserPosX > 800:
            chewbaccaLaserPosX = 130
            shootChewbaccaLaser = 0

        #If the current score is greater than the high score, set the high score as the current score.
        if score > highScore:
            highScore = score

        #Draw yoda, chewbacca, and display the scoreboard.
        drawYoda(yodaPosX, yodaPosY)
        drawChewbacca(chewbaccaPosX, chewbaccaPosY)
        displayScore(scorePosX, scorePosY)

        #---------------------------------------------------------------------
        #Window Update
        #---------------------------------------------------------------------
        windowUpdate()

    #If the game has been played, add the score to the list of scores (avoids adding random scores of 0 to the list without playing the game).
    if playGameConfirm == True:
        scores.append(score)

    #Set the confirmation to False so it does not stay True and make the game continue to add scores of 0 to the high scores list every time the program loops.
    playGameConfirm = False

def playAgainScreen():
    '''This function renders and draws text for the play again screen.'''
    window.fill(colourBlack)

    gameOver = titleFont.render("GAME OVER!", True, colourRed)

    playAgainText1 = primaryFont.render("Press ENTER to play again!", True, colourGreen)
    playAgainText2 = primaryFont.render("Press ESCAPE for the menu!", True, colourBlue)
    playAgainText3 = primaryFont.render("Close the window to stop", True, colourWhite)
    playAgainText4 = primaryFont.render("playing!", True, colourWhite)

    window.blit(gameOver, (0, 0))

    window.blit(playAgainText1, (0, 70))
    window.blit(playAgainText2, (0, 125))
    window.blit(playAgainText3, (0, 180))
    window.blit(playAgainText4, (0, 235))

def playMore():
    '''This function runs the playAgain screen, with events described on screen that are used to navigate the program.'''

    global showHighScores, showMenu, displayInstructions, playGame, playAgain

    #Pygame play again page loop
    while playAgain:

        #---------------------------------------------------------------------
        #Events
        #---------------------------------------------------------------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                #If the user presses enter, play the game again.
                if event.key == pygame.K_RETURN:
                    playAgain = False
                    showHighScores = False
                    showMenu = False
                    displayInstructions = False
                    playGame = True

                #If the user presses escape, go back to the main menu.
                if event.key == pygame.K_ESCAPE:
                    playAgain = False
                    showHighScores = False
                    showMenu = True

        #---------------------------------------------------------------------
        #Runtime - Draw the play again elements to the screen.
        #---------------------------------------------------------------------
        playAgainScreen()

        #---------------------------------------------------------------------
        #Window Update
        #---------------------------------------------------------------------
        windowUpdate()

def highScoresScreen():
    '''This program renders and draws the words on the high scores page, and neatly organizes, renders, and draws the high scores, along with their rankings (#1, #2...).'''

    window.fill(colourBlack)

    highScoresTitle = titleFont.render("HIGH SCORES", True, colourRed)
    highScoresPlay = primaryFont.render("Press ENTER to play!", True, colourGreen)
    highScoresMenu = primaryFont.render("Press ESCAPE for the menu!", True, colourBlue)

    window.blit(highScoresTitle, (0, 0))
    window.blit(highScoresPlay, (0, 465))
    window.blit(highScoresMenu, (0, 520))

    #Sort the list of scores in descending order so the ranking starts with highest score to the lowest score, hence a high score ranking.
    scores.sort(reverse=True)

    #x and y position of the first high score ranking.
    highScoresX = 0
    highScoresY = 70

    #Ranking of top 27 to be fit onto the screen
    for i in range(27):

        #This is statement is used so the program oesn't draw more scores than there are in the list
        if i < len(scores):

            #If i is greater than 0 and can be evenly divided by 9, start a new line of rankings so more rankings can be fit onto the page. Since there are 9 rankings per column for a total of 27 rankings, there will be 3 columns of high scores on the page.
            if i > 0:

                if i % 9 == 0:
                    highScoresX += 270
                    highScoresY = 70

            #Render and draw the score, wtih its corresponding ranking and at its corresponding position, onto the page.
            score = secondaryFont.render("#" + str(i + 1) + ": " + str(scores[i]), True, colourWhite)
            window.blit(score, (highScoresX, highScoresY))

            #Add 40 to the y position of the next highest score to organize the text without overlapping.
            highScoresY += 40

def highScores():
    '''This function runs the high scores page with events to navigate out of the page and around the program.'''

    global showMenu, displayInstructions, playGame, showHighScores

    #Pygame high scores page loop
    while showHighScores:

        #---------------------------------------------------------------------
        #Events
        #---------------------------------------------------------------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                #If the user presses ENTER, run the game.
                if event.key == pygame.K_RETURN:
                    showHighScores = False
                    showMenu = False
                    displayInstructions = False
                    playGame = True

                #If the user presses ESCAPE, go back to the main menu.
                if event.key == pygame.K_ESCAPE:
                    showHighScores = False
                    showMenu = True

        #---------------------------------------------------------------------
        #Runtime - Render and draw the text to be displayed onto the high scores screen.
        #---------------------------------------------------------------------
        highScoresScreen()

        #---------------------------------------------------------------------
        #Window Update
        #---------------------------------------------------------------------
        windowUpdate()

#Pygame main loop - loops continuously as user switches between pages and ends when user presses the quit button or presses ESCAPE while on the main menu.
while True:
    resetVariables()
    mainMenu()
    showInstructions()
    game()
    playMore()
    highScores()