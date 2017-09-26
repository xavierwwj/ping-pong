import pygame
import random
import math

### -----CONSTANTS-----

# mainloop bool
running = True
game_pause = False

# Time constants
clock = pygame.time.Clock() 
FPS = 30
playtime = 0.0

# Display constants
screen_width = 640
screen_length = 480
screen_size = (screen_width,screen_length)
background_color = (0,0,0)

# Score constants
font_size = 100
font_color = (255,255,255)
a_score = 0
b_score = 0

### -----INITIALISE PYGAME MODULE AND BACKGROUND-----

pygame.init()
screen = pygame.display.set_mode(screen_size)
background = pygame.Surface(screen_size)
background.fill(background_color)
background = background.convert()

score_font = pygame.font.SysFont('Lucida Sans Typewriter', font_size, True)
score_surface_a = score_font.render(str(a_score), False, font_color)
score_surface_b = score_font.render(str(b_score), False, font_color)


### -----VARIABLES-----

# Ball variables
ball_size = (8,8)
ball_radius = 4
ball_color = (255,255,255)

angle_seq = [20,160,200,340]
ball_angle = random.choice(angle_seq)
ball_angle_rad = ball_angle/360.0*2.0*math.pi

ball_x = 320.0
ball_y = 240.0
ball_speed = 1.0
ball_xspeed = 300.0*math.cos(ball_angle_rad)*ball_speed # in pixels per sec
ball_yspeed = -300.0*math.sin(ball_angle_rad)*ball_speed # in pixels per sec
dx = ball_xspeed / 30.0
dy = ball_yspeed / 30.0

# Paddle variables
paddle_width = 4 # These are half widths/heights
paddle_height = 30
paddle_speed  = 15

A_pos = {'x': paddle_width + paddle_height, 'y': 240} # center coordinate
A_color = (255,0,0)
A_rect = pygame.Rect(A_pos['x']-paddle_width, A_pos['y']-paddle_height,2*paddle_width, 2*paddle_height)

B_pos = {'x': 640 - paddle_width - paddle_height, 'y': 240}
B_color = (0,0,255)
B_rect = pygame.Rect(B_pos['x']-paddle_width, B_pos['y']-paddle_height,2*paddle_width, 2*paddle_height)

### -----HELPER FUNCTIONS-----
def reset_ball(angle, speed):
    x = 320.0
    y = 240.0
    xspeed = 300.0*math.cos(angle)*speed # in pixels per sec
    yspeed = -300.0*math.sin(angle)*speed # in pixels per sec
    dx = xspeed / 30.0
    dy = yspeed / 30.0
    return x,y,xspeed,yspeed,dx,dy

### -----MAIN MODULE-----

while running:
    # --UPDATE TIME--
    milliseconds = clock.tick(FPS)
    playtime += milliseconds / 1000.0

    # --PAUSE GAME--
    pause_seconds = 0
    while game_pause:
        if pause_seconds == 0:
            string = "3"
        else:
            string = str(4-pause_seconds)

        pause_surface = score_font.render(string, False, font_color)
        screen.blit(background, (0,0))
        screen.blit(pause_surface,(290,30))
        pygame.display.flip()
        pygame.time.wait(1000)
        pause_seconds += 1

        if pause_seconds == 4: # if more than 3 seconds (1sec of delay)
            game_pause = False
            pause_surface = score_font.render("", False, font_color)
            score_surface_a = score_font.render(str(a_score), False, font_color)
            score_surface_b = score_font.render(str(b_score), False, font_color)

    # --QUIT EVENT CONDITIONS--
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.set_caption("FPS: %.2f PLAYTIME: %.2f" % (clock.get_fps(), playtime))

    # --PADDLE EVENTS--
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and A_pos['y']>=paddle_height+paddle_speed: # Ensures paddle never exceed window
        A_pos['y'] -= paddle_speed
    elif keys[pygame.K_s] and A_pos['y']<=480-paddle_height-paddle_speed:
        A_pos['y'] += paddle_speed
##    if keys[pygame.K_a]:
##        A_pos['x'] -= paddle_speed
##    elif keys[pygame.K_d]:
##        A_pos['x'] += paddle_speed

    if keys[pygame.K_UP] and B_pos['y']>=paddle_height+paddle_speed:
        B_pos['y'] -= paddle_speed
    elif keys[pygame.K_DOWN] and B_pos['y']<=480-paddle_height-paddle_speed:
        B_pos['y'] += paddle_speed
##    if keys[pygame.K_LEFT]:
##        B_pos['x'] -= paddle_speed
##    elif keys[pygame.K_RIGHT]:
##        B_pos['x'] += paddle_speed

    A_rect = pygame.Rect(A_pos['x']-paddle_width, A_pos['y']-paddle_height,2*paddle_width, 2*paddle_height)
    B_rect = pygame.Rect(B_pos['x']-paddle_width, B_pos['y']-paddle_height,2*paddle_width, 2*paddle_height)

    # --BALL EVENTS--
    ball_x += dx
    ball_y += dy
    if ball_x + ball_radius >= screen_width: # ball leaves area -> update/reset
        ball_x, ball_y, ball_xspeed, ball_yspeed, dx, dy = reset_ball(random.choice(angle_seq)/360.0*2.0*math.pi, ball_speed)
        A_pos = {'x': paddle_width + paddle_height, 'y': 240}
        B_pos = {'x': 640 - paddle_width - paddle_height, 'y': 240}
        a_score += 1
        score_surface_a = score_font.render("", False, font_color)
        score_surface_b = score_font.render("", False, font_color)
        game_pause = True
    elif ball_x - ball_radius <= 0:
        ball_x, ball_y, ball_xspeed, ball_yspeed, dx, dy = reset_ball(random.choice(angle_seq)/360.0*2.0*math.pi, ball_speed)        
        b_score += 1
        A_pos = {'x': paddle_width + paddle_height, 'y': 240}
        B_pos = {'x': 640 - paddle_width - paddle_height, 'y': 240}
        score_surface_a = score_font.render("", False, font_color)
        score_surface_b = score_font.render("", False, font_color)
        game_pause = True

    elif ball_y + ball_radius >= screen_length: # ball hit wall -> bounces
        ball_y = screen_length - ball_radius
        dy *= -1
    elif ball_y - ball_radius <= 0:
        ball_y = ball_radius
        dy *= -1

    # ball hits paddle -> reflect
    elif ball_x - ball_radius <= A_pos['x']+paddle_width and ball_x-ball_radius >= A_pos['x']-paddle_width and ball_y >= A_pos['y']-paddle_height and ball_y <= A_pos['y']+paddle_height:
        ball_x = A_pos['x'] + paddle_width
        dx *= -1
    elif ball_x + ball_radius >= B_pos['x']-paddle_width and ball_x+ball_radius <= B_pos['x']+paddle_width and ball_y >= B_pos['y']-paddle_height and ball_y <= B_pos['y']+paddle_height:
        ball_x = B_pos['x']-paddle_width
        dx *= -1
    
    # --Drawing, refreshing events--
    screen.blit(background, (0,0))
    screen.blit(score_surface_a, (30,30))
    screen.blit(score_surface_b, (640-font_size/2-20,30))
    pygame.draw.rect(screen, A_color, A_rect, 0)
    pygame.draw.rect(screen, B_color, B_rect, 0)
    pygame.draw.circle(screen, ball_color, (int(round(ball_x, 0)), int(round(ball_y,0))), ball_radius)
    pygame.display.flip()

### -----QUIT EVENT-----

pygame.quit()
