import numpy as np
from dataclasses import dataclass

@dataclass
class Vector3:
    x: float
    y: float
    z: float

    def to_array(self):
        return np.array([self.x, self.y, self.z, 1.0])

    @staticmethod
    def from_array(arr):
        return Vector3(arr[0], arr[1], arr[2])

class Camera:
    def __init__(self):
        self.position = Vector3(0, 0, 10)
        self.target = Vector3(0, 0, 0)
        self.up = Vector3(0, 1, 0)
        self.fov = 90  # Increased FOV for wider view
        self.aspect = 4/3
        self.near = 0.1
        self.far = 2000.0  # Increased far plane for better visibility

    def get_view_matrix(self):
        z = normalize(subtract_vectors(self.position, self.target))
        x = normalize(cross_product(self.up, z))
        y = cross_product(z, x)

        view = np.identity(4)
        view[0, 0:3] = x
        view[1, 0:3] = y
        view[2, 0:3] = z
        view[0:3, 3] = [-dot_product(x, self.position), 
                        -dot_product(y, self.position),
                        -dot_product(z, self.position)]
        return view

    def get_projection_matrix(self):
        f = 1.0 / np.tan(np.radians(self.fov) / 2)
        proj = np.zeros((4, 4))
        proj[0, 0] = f / self.aspect
        proj[1, 1] = f
        proj[2, 2] = (self.far + self.near) / (self.near - self.far)
        proj[2, 3] = 2 * self.far * self.near / (self.near - self.far)
        proj[3, 2] = -1
        return proj

def normalize(v):
    if isinstance(v, Vector3):
        v = np.array([v.x, v.y, v.z])
    norm = np.sqrt(np.sum(v * v))
    if norm != 0:
        if isinstance(v, np.ndarray):
            return v / norm
        else:
            return Vector3(v.x/norm, v.y/norm, v.z/norm)
    return v

def cross_product(a, b):
    if isinstance(a, Vector3):
        a = a.to_array()[:3]
    if isinstance(b, Vector3):
        b = b.to_array()[:3]
    return np.cross(a, b)

def dot_product(a, b):
    if isinstance(a, Vector3):
        a = a.to_array()[:3]
    if isinstance(b, Vector3):
        b = b.to_array()[:3]
    return np.dot(a, b)

def subtract_vectors(a, b):
    if isinstance(a, Vector3) and isinstance(b, Vector3):
        return Vector3(a.x - b.x, a.y - b.y, a.z - b.z)
    return a - b

def create_rotation_matrix(angle, axis):
    c = np.cos(np.radians(angle))
    s = np.sin(np.radians(angle))
    t = 1 - c
    x, y, z = normalize(axis)
    
    return np.array([
        [t*x*x + c,    t*x*y - z*s,  t*x*z + y*s,  0],
        [t*x*y + z*s,  t*y*y + c,    t*y*z - x*s,  0],
        [t*x*z - y*s,  t*y*z + x*s,  t*z*z + c,    0],
        [0,           0,            0,             1]
    ])

def create_translation_matrix(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])

def project_point(point, view_matrix, projection_matrix, screen_width, screen_height):
    if isinstance(point, Vector3):
        point = point.to_array()
    
    # Apply view and projection transformations
    clip_space = projection_matrix @ view_matrix @ point
    
    # Perspective divide
    if clip_space[3] != 0:
        ndc = clip_space[:3] / clip_space[3]
    else:
        ndc = clip_space[:3]
    
    # Convert to screen coordinates
    screen_x = (ndc[0] + 1) * screen_width / 2
    screen_y = (1 - ndc[1]) * screen_height / 2
    
    return screen_x, screen_y