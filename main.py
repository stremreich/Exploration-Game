import pygame
import sys
from ship import Ship

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)

# Set up the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Ocean Explorer')

# Create player ship
player = Ship(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

# Game clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get keyboard input
    keys = pygame.key.get_pressed()
    player.move(keys)
    
    # Fill the screen with black color for space
    screen.fill(BLACK)
    
    # Draw the ship
    player.draw(screen)
    
    # Update the display
    pygame.display.flip()
    
    # Control game speed
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()