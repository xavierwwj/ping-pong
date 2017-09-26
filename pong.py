import pygame

### -----CONSTANTS-----

# mainloop bool
running = True

# Time constants
clock = pygame.time.Clock() 
FPS = 30
playtime = 0.0

# Display constants
screen_size = (640,480)
background_color = (0,0,0)

### -----INITIALISE PYGAME MODULE AND BACKGROUND-----

pygame.init() 
screen = pygame.display.set_mode(screen_size)
background = pygame.Surface(screen_size)
background.fill(background_color)
background = background.convert()
screen.blit(background, (0,0))
pygame.display.flip()

### -----MAIN MODULE-----

while running:
    # Updating time component
    milliseconds = clock.tick(FPS)
    playtime += milliseconds / 1000.0

    # Quit event conditions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.set_caption("FPS: %.2f" % (clock.get_fps()))


### -----QUIT EVENT-----

pygame.quit()
