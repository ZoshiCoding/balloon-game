# simple balloon game for python
import random
import math

import pygame

# color definitions
black = 0, 0, 0
white = 255, 255, 255

# screen

screen_size = screen_width, screen_height = 512, 256

# loading screen

pygame.display.set_caption("Balloon game")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# cannon

cannonImg = pygame.image.load('cannon.png')
cannonX = screen_width - 32
cannonY = screen_height / 2 - 16
cannon_movement = 0

# balloon

balloonImg = pygame.image.load('balloon.png')
balloonX = 0
balloonY = 112
balloon_speed = 0.1
balloon_movement = 0

# cannonball

cannonballImg = pygame.image.load('cannonball.png')
cannonballX = screen_width - 32
cannonballY = 112
cannonball_speed = 10 * balloon_speed
cannonball_state = "ready"

missed_counter = 0

def cannon(cannonX, cannonY):
    screen.blit(cannonImg, (cannonX, cannonY))

def balloon(balloonX, balloonY):
    screen.blit(balloonImg, (balloonX, balloonY))

def fire_cannon(x, y):
    global cannonball_state
    cannonball_state = "fire"
    screen.blit(cannonballImg, (x + 8, y + 8))

# Helper function to find if there is a collision
def collision(balloonX, balloonY, cannonballX, cannonballY):
    distance = math.sqrt(math.pow(balloonX - cannonballX, 2) + (math.pow(balloonY - cannonballY, 2)))
    if distance < 16:
        return True
    else:
        return False

def win_text():
    text = pygame.font.Font('freesansbold.ttf', 32).render("Missed shots: " + str(missed_counter), True, (black))
    screen.blit(text, (130, 100))

# game

pygame.init()
screen = pygame.display.set_mode(screen_size)
done = False
win = False
timer = 0
randBits = True

while not done:
    screen.fill(white)

    # inputs

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                cannon_movement = -0.1
            if event.key == pygame.K_DOWN:
                cannon_movement = 0.1
            if event.key == pygame.K_SPACE:
                if cannonball_state is "ready":
                    cannonballY = cannonY
                    fire_cannon(cannonballX, cannonballY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                cannon_movement = 0

    cannonY += cannon_movement

    # balloon movement
    if (timer <= 0):
        randBits = bool(random.getrandbits(1))
        timer = 500



    if randBits:
        balloonY += balloon_speed
    else:
        balloonY -= balloon_speed


    # checking for screen boundaries

    if cannonY > screen_height - 32:
        cannonY = screen_height - 32
    elif cannonY < 0:
        cannonY = 0

    if balloonY > screen_height - 32:
        balloonY = screen_height - 32
    elif balloonY < 0:
        balloonY = 0

    if collision(balloonX, balloonY, cannonballX, cannonballY):
        win = True
        cannonX = -100
        cannonY = -100
        balloonX = -100
        balloonY = -100

    # cannonball movement
    if cannonball_state is "fire" and win is False:
        fire_cannon(cannonballX, cannonballY)
        cannonballX -= cannonball_speed

    if cannonballX <= 0:
        cannonballX = screen_width - 32
        cannonball_state = "ready"
        missed_counter += 1


    if win is True:
        win_text()

    # update the positions 

    cannon(cannonX, cannonY)
    balloon(balloonX, balloonY)

    timer -= 1

    pygame.display.update()
