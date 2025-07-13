import pygame
import random
import math
from pygame import mixer

# Initializing Pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

# Bullet
# Ready - you cant see bullet on the screen
# Fire - bullet is currently moving
bulletImg = pygame.image.load('beam.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

# Score
score_value = 0

font = pygame.font.Font('Minecraft.ttf', 32)

textX = 10
texty = 10

# Game over text
over_font = pygame.font.Font('Minecraft.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def restart_button():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_color = (50, 50, 50)
    hover_color = (100, 100, 100)
    text_color = (255, 255, 255)

    button_x = 255
    button_y = 320
    button_w = 280
    button_h = 60

    if button_x < mouse[0] < button_x + button_w and button_y < mouse[1] < button_y + button_h:
        pygame.draw.rect(screen, hover_color, (button_x, button_y, button_w, button_h))
        if click[0] == 1:
            restart_game()
    else:
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_w, button_h))

        # Button text
    restart_font = pygame.font.Font('Minecraft.ttf', 48)
    restart_text = restart_font.render("RESTART", True, text_color)
    screen.blit(restart_text, (button_x + 25, button_y + 10))


def restart_game():
    global playerX, playerY, playerX_change, bulletX, bulletY, bullet_state
    global enemyX, enemyY, enemyX_change, enemyY_change, score_value, running

    playerX = 370
    playerY = 480
    playerX_change = 0

    bulletX = 0
    bulletY = 480
    bullet_state = "ready"

    score_value = 0

    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 736)
        enemyY[i] = random.randint(50, 150)
        enemyX_change[i] = 0.5
        enemyY_change[i] = 40


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 4, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Get current x and y coordinates of ship
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerX += playerX_change

    # Checking for boundaries of spaceship so it doesn't go outside screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            restart_button()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, texty)
    pygame.display.update()
