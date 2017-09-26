import pygame
import random
import math

### -----CONSTANTS-----

# mainloop bool
running = True

# Time constants
clock = pygame.time.Clock() 
FPS = 30
playtime = 0.0

# Display constants
screen_width = 640
screen_length = 480
screen_size = (screen_width,screen_length)
background_color = (0,0,0)

### -----VARIABLES-----

# Ball variables
ball_size = (8,8)
ball_radius = 4
angle_seq = [20,160,200,340]
ball_angle = random.choice(angle_seq)
ball_angle_rad = ball_angle/360*2*math.pi
print (ball_angle)
ball_color = (255,255,255)
ball_x = 320.0
ball_y = 240.0
ball_speed = 1
ball_xspeed = 300.0*math.cos(ball_angle_rad)*ball_speed # in pixels per sec
ball_yspeed = -300.0*math.sin(ball_angle_rad)*ball_speed # in pixels per sec
dx = ball_xspeed / 30.0
dy = ball_yspeed / 30.0

### -----INITIALISE PYGAME MODULE AND BACKGROUND-----

pygame.init() 
screen = pygame.display.set_mode(screen_size)
background = pygame.Surface(screen_size)
background.fill(background_color)
background = background.convert()

### -----MAIN MODULE-----

while running:
    # Updating time component
    milliseconds = clock.tick(FPS)
    playtime += milliseconds / 1000.0

    # Quit event conditions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.set_caption("FPS: %.2f PLAYTIME: %.2f" % (clock.get_fps(), playtime))

    # Ball events
    ball_x += dx
    ball_y += dy
    if ball_x + ball_radius >= screen_width:
        ball_x = screen_width - ball_radius
        dx *= -1
    elif ball_x - ball_radius <= 0:
        ball_x = ball_radius
        dx *= -1
    elif ball_y + ball_radius >= screen_length:
        ball_y = screen_length - ball_radius
        dy *= -1
    elif ball_y - ball_radius <= 0:
        ball_y = ball_radius
        dy *= -1

    screen.blit(background, (0,0))
    pygame.draw.circle(screen, ball_color, (int(round(ball_x, 0)), int(round(ball_y,0))), ball_radius)
    pygame.display.flip()

### -----QUIT EVENT-----

pygame.quit()
