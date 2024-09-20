from OpenGL.GL import *
import numpy as np

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
