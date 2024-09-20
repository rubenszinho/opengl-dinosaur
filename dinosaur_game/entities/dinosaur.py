from OpenGL.GL import *
import numpy as np
from ..graphics.utils import draw_dinosaur
from .fireball import Fireball

# The dinosaur grows and shrinks with the keys 'o' and 'p' and can perform a double jump.
# On the second jump, it spins as required in the assignment and translates.
class Dinosaur:
    def __init__(self):
        self.x = -0.8
        self.y = -0.4
        self.angle = 0
        self.jump_height = 1.5
        self.is_jumping = False
        self.is_falling = False
        self.jump_count = 0
        self.jump_speed = 0.05
        self.color = (1.0, 0.0, 1.0, 1.0)
        self.scale = 1.0

    def set_scale(self, new_scale):
        self.scale = new_scale

    def jump(self):
        if self.jump_count < 2 and (self.jump_count == 0 or self.is_falling):
            self.is_jumping = True
            self.jump_speed = 0.04 if self.jump_count == 1 else 0.05
            self.jump_count += 1
            if self.is_falling:
                self.is_falling = False

    def update(self):
            if self.is_jumping:
                self.y += self.jump_speed
                if self.jump_count == 2:
                    self.angle += 30
                    if self.angle >= 360:
                        self.angle = 0

            if self.y >= self.jump_height:
                self.is_jumping = False
                self.is_falling = True
            if self.is_falling:
                self.y -= self.jump_speed
                if self.y <= -0.4:
                    self.y = -0.4
                    self.is_falling = False
                    self.jump_count = 0
                    self.angle = 0

    def draw(self, draw_dinosaur_func, model_location, view_location, projection_location, color_location, color):
        translate_to_origin = np.array([[1, 0, 0, -(self.x + 0.2)],
                                        [0, 1, 0, -(self.y + 0.25)],
                                        [0, 0, 1, 0],
                                        [0, 0, 0, 1]], dtype=np.float32)

        # Rotate to perform the backflip
        rotation_matrix = np.array([[np.cos(np.radians(self.angle)), -np.sin(np.radians(self.angle)), 0, 0],
                                    [np.sin(np.radians(self.angle)), np.cos(np.radians(self.angle)), 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]], dtype=np.float32)

        # Applying scale matrix
        scale_matrix = np.array([[self.scale, 0, 0, 0],
                                [0, self.scale, 0, 0],
                                [0, 0, self.scale, 0],
                                [0, 0, 0, 1]], dtype=np.float32)

        # Translate back to original position
        translate_back = np.array([[1, 0, 0, self.x + 0.2],
                                [0, 1, 0, self.y + 0.25],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]], dtype=np.float32)

        model = np.dot(translate_back, np.dot(rotation_matrix, np.dot(scale_matrix, translate_to_origin)))

        glUniformMatrix4fv(model_location, 1, GL_TRUE, model)
        glUniformMatrix4fv(view_location, 1, GL_FALSE, np.eye(4, dtype=np.float32))
        glUniformMatrix4fv(projection_location, 1, GL_TRUE, np.eye(4, dtype=np.float32))

        draw_dinosaur_func(self.x, self.y, color_location, color)
        
    def get_bounding_box(self):
            return (self.y + 0.1, -1 + 0.1, 0.4, 0.4)

    def is_colliding(self, obstacle):
        dinosaur_bb = self.get_bounding_box()
        obstacle_bb = obstacle.get_bounding_box()

        return (dinosaur_bb[0] < obstacle_bb[0] + obstacle_bb[2] and
                dinosaur_bb[0] + dinosaur_bb[2] > obstacle_bb[0] and
                dinosaur_bb[1] < obstacle_bb[1] + obstacle_bb[3] and
                dinosaur_bb[1] + dinosaur_bb[3] > obstacle_bb[1])

    def shoot_fireball(self):
        return Fireball(-0.65, self.y + 0.5)  # Create fireball from the dinosaur's position