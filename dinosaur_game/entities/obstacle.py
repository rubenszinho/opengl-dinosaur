from OpenGL.GL import *
import random
import numpy as np
from ..graphics.utils import draw_cactus, draw_bird

class Obstacle:
    _obstacles = []

    def __init__(self, x, y, obj_type):
        self.x = x
        self.y = y
        self.obj_type = obj_type
        self.color = (0.0, 0.0, 1.0, 1.0)

    def get_bounding_box(self):
        if self.obj_type == 'cactus':
            return (self.y, self.x, 0.2, 0.2)
        else:
            return (self.y + 0.3, self.x, 0.2, 0.15)
        
    @classmethod
    def update_obstacles(cls):
        for obstacle in cls._obstacles:
            obstacle.x -= 0.01
            if obstacle.x < -2.5:
                cls._obstacles.remove(obstacle)

    @classmethod
    def generate_obstacle(cls):
        ground_height = -0.4
        obj_type = random.choice(['cactus', 'bird'])

        if obj_type == 'cactus':
            y = ground_height
        else:
            y = ground_height + 0.2

        cls._obstacles.append(Obstacle(2.5, y, obj_type))

    @classmethod
    def get_obstacles(cls):
        return cls._obstacles

    def draw(self, model_location, view_location, projection_location, color_location, color):
        glUniformMatrix4fv(model_location, 1, GL_FALSE, np.eye(4, dtype=np.float32))
        glUniformMatrix4fv(view_location, 1, GL_FALSE, np.eye(4, dtype=np.float32))
        glUniformMatrix4fv(projection_location, 1, GL_FALSE, np.eye(4, dtype=np.float32))
        if self.obj_type == 'cactus':
            draw_cactus(self.x, self.y, color_location, color)
        elif self.obj_type == 'bird':
            draw_bird(self.x, self.y, color_location, color)