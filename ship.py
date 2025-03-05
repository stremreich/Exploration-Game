import pygame
import math
from engine3d import Vector3, Camera, create_rotation_matrix, create_translation_matrix, project_point

class Ship:
    def __init__(self, x, y):
        # Ship dimensions
        self.width = 40
        self.height = 60
        
        # Ship position in spherical coordinates
        self.longitude = 0  # -180 to 180 degrees
        self.latitude = 0   # -90 to 90 degrees
        self.radius = 200   # radius of the sphere in world units
        
        # Ship movement
        self.speed = 2
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
        
        # Initialize camera
        self.camera = Camera()
        self.update_camera_position()
    
    def update_camera_position(self):
        # Convert spherical to cartesian coordinates for ship position
        ship_pos = self.get_position_3d()
        
        # Position camera above and behind ship
        camera_distance = self.radius * 1.5  # Reduced camera distance for better visibility
        self.camera.position = Vector3(
            ship_pos.x * camera_distance,
            ship_pos.y * camera_distance,
            ship_pos.z * camera_distance
        )
        self.camera.target = ship_pos
    
    def get_position_3d(self):
        # Convert spherical coordinates to 3D position
        lat_rad = math.radians(self.latitude)
        lon_rad = math.radians(self.longitude)
        
        x = self.radius * math.cos(lat_rad) * math.cos(lon_rad)
        y = self.radius * math.cos(lat_rad) * math.sin(lon_rad)
        z = self.radius * math.sin(lat_rad)
        
        return Vector3(x, y, z)
    
    def move(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            # Forward movement
            heading_rad = math.radians(self.rotation)
            lat_rad = math.radians(self.latitude)
            lon_rad = math.radians(self.longitude)
            
            # Calculate new position using great circle formulas
            new_lat_rad = math.asin(math.sin(lat_rad) * math.cos(self.speed * 0.01) + 
                                   math.cos(lat_rad) * math.sin(self.speed * 0.01) * math.cos(heading_rad))
            new_lon_rad = lon_rad + math.atan2(math.sin(heading_rad) * math.sin(self.speed * 0.01) * math.cos(lat_rad),
                                               math.cos(self.speed * 0.01) - math.sin(lat_rad) * math.sin(new_lat_rad))
            
            self.latitude = math.degrees(new_lat_rad)
            self.longitude = ((math.degrees(new_lon_rad) + 180) % 360) - 180
            
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            # Backward movement
            heading_rad = math.radians((self.rotation + 180) % 360)
            lat_rad = math.radians(self.latitude)
            lon_rad = math.radians(self.longitude)
            
            new_lat_rad = math.asin(math.sin(lat_rad) * math.cos(self.speed * 0.01) + 
                                   math.cos(lat_rad) * math.sin(self.speed * 0.01) * math.cos(heading_rad))
            new_lon_rad = lon_rad + math.atan2(math.sin(heading_rad) * math.sin(self.speed * 0.01) * math.cos(lat_rad),
                                               math.cos(self.speed * 0.01) - math.sin(lat_rad) * math.sin(new_lat_rad))
            
            self.latitude = math.degrees(new_lat_rad)
            self.longitude = ((math.degrees(new_lon_rad) + 180) % 360) - 180
            
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotation = (self.rotation - 3) % 360
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotation = (self.rotation + 3) % 360
            
        # Update camera position after movement
        self.update_camera_position()
    
    def draw(self, screen):
        # Get view and projection matrices
        view_matrix = self.camera.get_view_matrix()
        projection_matrix = self.camera.get_projection_matrix()
        
        # Create a surface for the planet with gradient
        planet_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        center = (screen.get_width() // 2, screen.get_height() // 2)
        radius = int(self.radius * 0.8)
        
        # Draw base ocean color
        pygame.draw.circle(planet_surface, (0, 105, 148), center, radius)
        
        # Add texture pattern
        for r in range(0, radius, 20):
            alpha = int(255 * (1 - r/radius))
            color = (0, 150, 200, alpha)
            pygame.draw.circle(planet_surface, color, 
                             (center[0] + int(10 * math.sin(self.longitude/30)), 
                              center[1] + int(10 * math.cos(self.latitude/30))), 
                             radius - r, 2)
        
        # Apply the planet surface
        screen.blit(planet_surface, (0, 0))
        
        # Draw ship
        scaled_surface = pygame.transform.scale(self.surface, (self.width, self.height))
        rotated_surface = pygame.transform.rotate(scaled_surface, -self.rotation)
        rect = rotated_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(rotated_surface, rect.topleft)
    
    def draw_grid(self, screen, view_matrix, projection_matrix):
        # Draw latitude lines
        for lat in range(-80, 81, 20):
            points = []
            for lon in range(-180, 181, 10):
                point = Vector3(
                    self.radius * math.cos(math.radians(lat)) * math.cos(math.radians(lon)),
                    self.radius * math.cos(math.radians(lat)) * math.sin(math.radians(lon)),
                    self.radius * math.sin(math.radians(lat))
                )
                
                screen_x, screen_y = project_point(
                    point, view_matrix, projection_matrix,
                    screen.get_width(), screen.get_height()
                )
                points.append((int(screen_x), int(screen_y)))
                
            if len(points) > 1:
                pygame.draw.lines(screen, (100, 200, 255), False, points, 2)
        
        # Draw longitude lines
        for lon in range(-180, 181, 20):
            points = []
            for lat in range(-80, 81, 10):
                point = Vector3(
                    self.radius * math.cos(math.radians(lat)) * math.cos(math.radians(lon)),
                    self.radius * math.cos(math.radians(lat)) * math.sin(math.radians(lon)),
                    self.radius * math.sin(math.radians(lat))
                )
                
                screen_x, screen_y = project_point(
                    point, view_matrix, projection_matrix,
                    screen.get_width(), screen.get_height()
                )
                points.append((int(screen_x), int(screen_y)))
                
            if len(points) > 1:
                pygame.draw.lines(screen, (100, 200, 255), False, points, 2)