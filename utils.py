import math
from OpenGL.GL import *
import numpy as np

def draw_rectangle(x, y, width, height):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

def draw_triangle(x, y, base, height):
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + base / 2, y + height)
    glVertex2f(x + base, y)
    glEnd()

def draw_shapes(objects, shader_program):
    glUseProgram(shader_program)

    color_location = glGetUniformLocation(shader_program, "color")
    model_location = glGetUniformLocation(shader_program, "model") 

    glUniform4f(color_location, 0, 1, 0, 1)
    glUniformMatrix4fv(model_location, 1, GL_FALSE, glGetFloatv(GL_MODELVIEW_MATRIX)) 
    objects[0].draw()  # Draw the ground

    glUniform4f(color_location, 0, 0, 1, 1)
    glPushMatrix() 
    glTranslatef(-1 + 0.25, objects[1].y + 0.25, 0) 
    glRotatef(objects[1].angle, 0, 0, 1) 
    glTranslatef(-(-1 + 0.25), -(objects[1].y + 0.25), 0) 
    glUniformMatrix4fv(model_location, 1, GL_FALSE, glGetFloatv(GL_MODELVIEW_MATRIX)) 
    objects[1].draw()  # Draw the dinosaur
    glPopMatrix() 

    glUniform4f(color_location, 1, 0, 0, 1)
    glUniformMatrix4fv(model_location, 1, GL_FALSE, glGetFloatv(GL_MODELVIEW_MATRIX)) 
    for obstacle in objects[2:]:
        obstacle.draw()  # Draw obstacles

    glUseProgram(0)

def draw_bird(x, y, color_location, color):
    glUniform4f(color_location, *color)
    
    # Head
    draw_triangle(x , y + 0.3, 0.35, 0.1)

    # Wing
    draw_triangle(x + 0.25, y + 0.3, 0.18, 0.15)

    # Body
    draw_triangle(x + 0.1 , y + 0.3, 0.5, -0.1)
    
def draw_cactus(x, y, color_location, color):
    glUniform4f(color_location, *color)

    # Main body
    draw_rectangle(x, y, 0.1, 0.3)
    
    # Arms
    draw_rectangle(x - 0.05, y + 0.1, 0.05, 0.1)
    draw_rectangle(x + 0.1, y + 0.1, 0.05, 0.1)

def draw_dinosaur(x, y, color_location, color):
    glUniform4f(color_location, *color)

    # Head
    draw_rectangle(x + 0.1, y + 0.4, 0.3, 0.2)
    # Body
    draw_rectangle(x + 0.1, y + 0.1, 0.2, 0.3)
    # Tail
    draw_triangle(x - 0.1 , y + 0.2, 0.3, -0.1)
    draw_triangle(x, y + 0.15, 0.2, 0.2)
    # Arm
    draw_rectangle(x + 0.3, y + 0.25, 0.05, 0.08)
    
    # Legs
    draw_rectangle(x + 0.1, y, 0.05, 0.1)
    draw_rectangle(x + 0.25, y, 0.05, 0.1)

def draw_ground(x, color_location, color):
    glUniform4f(color_location, *color)

    draw_rectangle(x, -0.5, 10, 0.1)

def draw_fireball(x, y, size, color_location, color):
    glUniform4f(color_location, *color)

    draw_circle(x, y, size)

def draw_circle(x, y, radius, num_segments=20):
    glBegin(GL_POLYGON)
    for i in range(num_segments):
        theta = 2.0 * 3.1415926 * float(i) / float(num_segments)
        dx = radius * math.cos(theta)
        dy = radius * math.sin(theta)
        glVertex2f(x + dx, y + dy)
    glEnd()