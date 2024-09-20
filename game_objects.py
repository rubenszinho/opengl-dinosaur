import random
from OpenGL.GL import *
import numpy as np
from utils import draw_cactus, draw_bird

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
            
class Ground:
    def __init__(self):
        self.x = -5
        self.color = (0.0, 0.0, 0.0, 0.0)


    def update(self):
        self.x += 0.01
        if self.x >= -3:
            self.x = -5

    def draw(self, draw_ground_func, model_location, view_location, projection_location, color_location, color):
        glUniformMatrix4fv(model_location, 1, GL_FALSE, np.eye(4, dtype=np.float32))
        glUniformMatrix4fv(view_location, 1, GL_FALSE, np.eye(4, dtype=np.float32))
        glUniformMatrix4fv(projection_location, 1, GL_FALSE, np.eye(4, dtype=np.float32))
        draw_ground_func(self.x, color_location, color)

class Fireball:
    def __init__(self, x, y):
        self.x = x + 0.45
        self.y = y - 0.04
        self.speed = 0.005
        self.size = 0.01
        self.max_size = 0.3
        self.color = (1.0, 0.0, 0.0, 1.0)

    def update(self):
        self.x += self.speed
        self.size += 0.001  # Increase the size of the fireball each frame

    def draw(self, draw_fireball_func, model_location, view_location, projection_location, color_location, color):
        model = np.eye(4, dtype=np.float32)
        model = np.dot(model, np.array([[1, 0, 0, self.x],
                                         [0, 1, 0, self.y],
                                         [0, 0, 1, 0],
                                         [0, 0, 0, 1]], dtype=np.float32))
        glUniformMatrix4fv(model_location, 1, GL_TRUE, model)
        glUniformMatrix4fv(view_location, 1, GL_FALSE, np.eye(4, dtype=np.float32))
        glUniformMatrix4fv(projection_location, 1, GL_FALSE, np.eye(4, dtype=np.float32))
        draw_fireball_func(self.x, self.y, self.size, color_location, color)

    def get_bounding_box(self):
        return (self.y, self.x, self.size, self.size)

    def is_gone(self):
        return self.size >= self.max_size

    def is_colliding(self, bird):
        fireball_bb = self.get_bounding_box()
        bird_bb = bird.get_bounding_box()

        return (fireball_bb[0] < bird_bb[0] + bird_bb[2] and
                fireball_bb[0] + fireball_bb[2] > bird_bb[0] and
                fireball_bb[1] < bird_bb[1] + bird_bb[3] and
                fireball_bb[1] + fireball_bb[3] > bird_bb[1])
