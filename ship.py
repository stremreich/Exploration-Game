import pygame
import math

class Ship:
    def __init__(self, x, y):
        # Ship dimensions
        self.width = 40
        self.height = 60
        
        # Ship position
        self.x = x
        self.y = y
        
        # Ship movement
        self.speed = 5
        self.rotation = 0
        
        # Create ship surface
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw triangular ship
        points = [
            (self.width // 2, 0),  # top point
            (0, self.height),  # bottom left
            (self.width, self.height)  # bottom right
        ]
        pygame.draw.polygon(self.surface, (200, 200, 200), points)
    
    def move(self, keys):
        # Handle keyboard input for movement
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            # Move forward in the direction of rotation
            self.x += self.speed * -math.sin(math.radians(self.rotation))
            self.y += self.speed * -math.cos(math.radians(self.rotation))
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            # Move backward
            self.x -= self.speed * -math.sin(math.radians(self.rotation))
            self.y -= self.speed * -math.cos(math.radians(self.rotation))
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            # Rotate left
            self.rotation = (self.rotation - 3) % 360
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            # Rotate right
            self.rotation = (self.rotation + 3) % 360
    
    def draw(self, screen):
        # Create a rotated copy of the ship surface
        rotated_surface = pygame.transform.rotate(self.surface, self.rotation)
        # Get the rectangle for the rotated surface
        rect = rotated_surface.get_rect(center=(self.x, self.y))
        # Draw the rotated ship
        screen.blit(rotated_surface, rect.topleft)