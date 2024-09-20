from OpenGL.GL import *
import numpy as np

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
