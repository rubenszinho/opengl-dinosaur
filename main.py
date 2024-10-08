import sys
import math
import random
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from dinosaur_game.entities.dinosaur import Dinosaur
from dinosaur_game.entities.obstacle import Obstacle
from dinosaur_game.entities.ground import Ground
from dinosaur_game.entities.fireball import Fireball
from dinosaur_game.graphics.utils import draw_dinosaur, draw_fireball, draw_ground
from dinosaur_game.graphics.shaders import create_shader_program

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    vertex_shader_source = """
    #version 330 core
    layout (location = 0) in vec3 position;
    uniform mat4 modelview;
    uniform mat4 projection;
    uniform vec4 color;
    uniform float rotation;
    uniform mat4 model;

    void main()
    {
        float cosRot = cos(rotation);
        float sinRot = sin(rotation);
        vec4 rotatedPosition = vec4(position.x * cosRot - position.y * sinRot, position.y * cosRot + position.x * sinRot, position.z, 1.0);
        gl_Position = projection * modelview * model * rotatedPosition;
    }
    """

    fragment_shader_source = """
    #version 330 core
    uniform vec4 color;
    out vec4 FragColor;

    void main()
    {
        FragColor = color;
    }
    """

    # Create and compile the shaders
    shader_program = create_shader_program(vertex_shader_source, fragment_shader_source)
    glUseProgram(shader_program)

    # Create the projection matrices and pass them to the shaders
    projection_matrix = np.eye(4, dtype=np.float32)
    gluPerspective(30, display[0] / display[1], 0.5, 100.0)

    # Retrieve the location of the uniform variables in the shaders
    model_loc = glGetUniformLocation(shader_program, "model")
    view_loc = glGetUniformLocation(shader_program, "modelview")
    projection_loc = glGetUniformLocation(shader_program, "projection")
    color_loc = glGetUniformLocation(shader_program, "color")

    glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection_matrix)
    glUniformMatrix4fv(model_loc,  1, GL_FALSE, projection_matrix)
    
    # Create the game objects
    ground = Ground()
    dinosaur = Dinosaur()

    clock = pygame.time.Clock()

    # Initialize the obstacle counter and the list of fireballs
    obstacle_counter = 0
    fireballs = []
    glClearColor(1.0, 1.0, 1.0, 1.0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dinosaur.jump()
                if event.key == pygame.K_f:
                    fireballs.append(dinosaur.shoot_fireball())
                if event.key == pygame.K_o:
                    dinosaur.set_scale(dinosaur.scale + 0.1)
                elif event.key == pygame.K_p:
                    dinosaur.set_scale(max(dinosaur.scale - 0.1, 0.1))

        glClear(GL_COLOR_BUFFER_BIT)

        # Update game objects and check for collisions
        dinosaur.update()
        ground.update()
        Obstacle.update_obstacles()

        obstacle_counter += 1
        if obstacle_counter % 200 == 0:
            Obstacle.generate_obstacle()

        for fireball in fireballs:
            fireball.update()

        for fireball in fireballs:
            for obstacle in Obstacle.get_obstacles():
                if obstacle.obj_type == 'bird' and fireball.is_colliding(obstacle):
                    Obstacle._obstacles.remove(obstacle)
                    fireballs.remove(fireball)
                    break

        # Draw the game objects
        ground.draw(draw_ground, model_loc, view_loc, projection_loc, color_loc, ground.color)
        dinosaur.draw(draw_dinosaur, model_loc, view_loc, projection_loc, color_loc, dinosaur.color)

        for obstacle in Obstacle.get_obstacles():
            obstacle.draw(model_loc, view_loc, projection_loc, color_loc, obstacle.color)

        for fireball in fireballs:
            fireball.draw(draw_fireball, model_loc, view_loc, projection_loc, color_loc, fireball.color)

        pygame.display.flip()
        clock.tick(60)

        for obstacle in Obstacle.get_obstacles():
            if dinosaur.is_colliding(obstacle):
                print("Game Over!")
                pygame.quit()
                sys.exit()
                
if __name__ == "__main__":
    main()
