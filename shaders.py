from OpenGL.GL import *

def create_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader))

    return shader


def create_shader_program(vertex_shader_source, fragment_shader_source):
    vertex_shader = create_shader(GL_VERTEX_SHADER, vertex_shader_source)
    fragment_shader = create_shader(GL_FRAGMENT_SHADER, fragment_shader_source)

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(program))

    glDetachShader(program, vertex_shader)
    glDetachShader(program, fragment_shader)
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program