import sys
import math
import random
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from shaders import create_shader_program

from game_objects import Dinosaur, Obstacle, Ground
from utils import draw_dinosaur, draw_fireball, draw_ground

def main():
    # Inicializa o pygame e define a resolução da janela
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

    # Cria e compila os shaders
    shader_program = create_shader_program(vertex_shader_source, fragment_shader_source)
    glUseProgram(shader_program)

    # Cria as matrizes de projeção e as passa para os shaders
    projection_matrix = np.eye(4, dtype=np.float32)
    gluPerspective(30, display[0] / display[1], 0.5, 100.0)


    # Busca a localização das variáveis uniformes nos shaders
    model_loc = glGetUniformLocation(shader_program, "model")
    view_loc = glGetUniformLocation(shader_program, "modelview")
    projection_loc = glGetUniformLocation(shader_program, "projection")
    color_loc = glGetUniformLocation(shader_program, "color")

    glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection_matrix)
    glUniformMatrix4fv(model_loc,  1, GL_FALSE, projection_matrix)
    
    # Cria os objetos do jogo
    ground = Ground()
    dinosaur = Dinosaur()

    clock = pygame.time.Clock()
    # Inicializa o contador de obstáculos e a lista de bolas de fogo
    obstacle_counter = 0
    fireballs = []
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # Loop principal do jogo
    while True:
        # Trata eventos do teclado
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

        # Atualiza os objetos do jogo e verifica colisões
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

        # Desenha os objetos na tela
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