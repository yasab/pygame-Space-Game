import pygame
#weneed this model to use sqrt() and pow() in collition function
import math
#we need this model to random numbers
import random 
#we need this to put music in our game
from pygame import mixer


#This will attempt to initialize all programe modules for you
pygame.init()


#Create the screen:
screen = pygame.display.set_mode((800, 600))
# screen into a variable
width = screen.get_width()
  
# stores the height of the
# screen into a variable
height = screen.get_height()
  

#Title and Icon
pygame.display.set_caption('Space Game')
icon = pygame.image.load('SpaceGameLogo.png')
pygame.display.set_icon(icon)

#background
bg = pygame.image.load('background.jpg')
bg =pygame.transform.scale(bg, (800, 600))

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

#player image and Scale
playerImg = pygame.image.load('SpaceGameLogo.png')
playerImg = pygame.transform.scale(playerImg, (50, 50))

#Player
playerX = 370
playerY = 480
PmoveX = 0
Pspeed = 3

#Enemy
enemyImg = []
enemyX = []
enemyY = []
EmoveX = []
EmoveY = []
enemyHP = []
enemyN = 3

for i  in range (enemyN) :
    #Enemy image and Scale
    enemyImg.append(pygame.image.load('EnemyImg.png'))
    #Enemy
    enemyX.append(random.randint(0, 730))
    enemyY.append(random.randint(0, 50))
    EmoveX.append(4)
    EmoveY.append(110)
    enemyHP.append(0)

#change the scale of the enemies
for i  in range (enemyN) :
    enemyImg[i] = pygame.transform.scale(enemyImg[i], (100, 100))

#Bullet image and Scale
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (30, 30))

#bullet
bulletX = playerX 
bulletY = playerY
BmoveX = 0
BmoveY = 0
Bspeed = 13

#score
kills = 0
font = pygame.font.Font('GameFont.ttf',32)

#Best score
best_score = 0
best_score_font = pygame.font.Font('GameFont.ttf',32)

#show the score on the screen
def show_score(x, y):
    score = font.render("Kills : " + str(kills), True, (255,255,255))
    screen.blit(score, (x, y))

#show the best score on the screen
def show_best_score():
    Bestscore = font.render("Best Score : " + str(best_score), True, (255,255,255))
    screen.blit(Bestscore, (250, 160))

#GameOver
end_the_game = False
GameOver_font = pygame.font.Font('GameFont.ttf',100)

#restart the game button
restart_the_game = False
restart_font = pygame.font.Font('GameFont.ttf',70)
R = 255
G = 255
B = 255


#show the GameOver on the screen
def game_over():
    GameOver = GameOver_font.render("Game Over" , True, (255,255,255))
    screen.blit(GameOver, (120, 200))

#show the restart button on the screen
def restart_button():
    restart = restart_font.render("Restart" , True, (R,G,B))
    screen.blit(restart, (240, 350))

#Draw the player on the screen
def player(x, y):
    screen.blit(playerImg, (x, y))

#Draw the enemy on the screen
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

#Draw the bullet on the screen
def bullet(x, y):
    screen.blit(bulletImg, (x, y))
    #bullet sound
    bullet_sound = mixer.Sound('laser.wav')
    bullet_sound.set_volume(0.1)
    bullet_sound.play()

#collision methode
def collision(x, y, a, b):
    distence = math.sqrt(math.pow(x - a, 2) + math.pow(y - b, 2))
    if distence < 50:
        return True
    else:
        return False

#Game loop
running = True
shoot = False
showB = False
show_enemies = True
while running:

    #Screen Background 
    screen.fill((0,0,0))
    
    #Draw the background image
    screen.blit(bg, (0,0))

    #check every event the user do or happen in the screen
    for event in pygame.event.get():

        #Quit the screen if the user want to
        if event.type == pygame.QUIT:
            running = False
        

        
        #check if key is pressed
        if event.type == pygame.KEYDOWN:
            #Move left
            if event.key == pygame.K_LEFT:
                PmoveX = -Pspeed
            #Move right
            if event.key == pygame.K_RIGHT:
                PmoveX = Pspeed   
            #Shoot
            if event.key == pygame.K_SPACE and end_the_game == False:
                shoot = True
                BmoveY = Bspeed
    
        #check if key is released
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PmoveX = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                PmoveY = 0 
            if event.key == pygame.K_SPACE and end_the_game == False:
                showB = True
        
        #checks if a mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 240 <= mouse[0] <= 540 and 350 <= mouse[1] <= 490 and show_enemies == False:
                restart_the_game = True
                for i in range(enemyN):
                    enemyX[i] = random.randint(0, 730)
                    enemyY[i] = random.randint(0, 50)
                end_the_game = False
                show_enemies = True
                kills = 0

            

                

    #Player Movement
    playerX += PmoveX    

    #Player Space borders
    if playerX < 0 : playerX = 0 

    elif playerX >= 750 : playerX = 750

    #Enemy movement
    
    for i in range(enemyN):
            enemyX[i] += EmoveX[i]

            if enemyX[i] < 0 : 
                EmoveX[i] *= -1
                enemyY[i] += EmoveY[i]

            elif enemyX[i] > 730 : 
                EmoveX[i] *= -1
                enemyY[i] += EmoveY[i]

            #enemyHP and enemy respown
            if enemyHP[i] < 1 and show_enemies:
                enemy(enemyX[i], enemyY[i], i)
            elif enemyHP[i] >= 1 : 
                enemyX[i] = 0
                enemyY[i] = random.randint(0, 50)
                enemyHP[i] = 0
                kills += 1
                

            #what is going to happent is the bullet and the enemy collied
            if collision(enemyX[i], enemyY[i], bulletX, bulletY) and collision(enemyX[i], enemyY[i], playerX, playerY) == False:
                showB = False
                enemyHP[i] += 1
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.set_volume(1.0)
                explosion_sound.play()

        #game_over
            if collision(enemyX[i], enemyY[i], playerX, playerY) :
                show_enemies = False
                end_the_game = True
                
                

            if  end_the_game and show_enemies == False:
                game_over()
                restart_button()
                show_best_score()

            #highlight the restart button with red color
            mouse = pygame.mouse.get_pos()
            if 240 <= mouse[0] <= 540 and 350 <= mouse[1] <= 490:
                G = 0
                B = 0
            else :
                G = 255
                B = 255



        

        
    #Bullet Movement
    if shoot:
        bulletY -= BmoveY
    if showB:
        bullet(bulletX + 10.5, bulletY)
    else: 
        bulletX = playerX
        bulletY = playerY
        showB = False

    if bulletY < 0:
        showB = False

    


    
    
        
    #show the score on the screen on every frame of the game
    show_score(playerX - 40, playerY + 50)

    #draw the player on the screen on every frame of the game
    player(playerX, playerY)

    #calculate the best score
    if kills > best_score:
        best_score = kills

    
    


    pygame.display.update()
