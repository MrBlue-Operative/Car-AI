import pygame as py
import numpy as np

py.init()
py.font.init()

WIDTH, HEIGHT = 1200, 700
shift = 250
FPS = 60
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (225, 0, 0)
YELLOW = (225, 225, 0)

screen = py.display.set_mode((WIDTH, HEIGHT))

def check_collision(obj1, obj2):
    if not obj1.rotated_rect.colliderect(obj2.rotated_rect):
        return False
    offset_x = int(obj2.rotated_rect.left - obj1.rotated_rect.left)
    offset_y = int(obj2.rotated_rect.top - obj1.rotated_rect.top)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

def scale(value, length):
    return value + (length if value >= 0 else -length)

def distribute(startx, starty, endx, endy, num_points=10):
    x = np.linspace(startx, endx, num_points)
    y = np.linspace(starty, endy, num_points)
    return np.column_stack((x, y))

def inputs(w, a, s, d):
    size = 50
    thick = 3
    RED = (0, 122, 0)
    x = 300
    y = 100
    if w:
        py.draw.rect(screen, RED, (WIDTH/2 + x, HEIGHT/2 - 1 + y, size, size))
    else:
        py.draw.rect(screen, BLACK, (WIDTH/2 + x, HEIGHT/2 - 1 + y, size, size), thick)

    if a:
        py.draw.rect(screen, RED, (WIDTH/2 - size - 1 + x, HEIGHT/2 + size + y, size, size))
    else:
        py.draw.rect(screen, BLACK, (WIDTH/2 - size - 1 + x, HEIGHT/2 + size + y, size, size), thick)

    if s:
        py.draw.rect(screen, RED, (WIDTH/2 + x, HEIGHT/2 + size + y, size, size))
    else:
        py.draw.rect(screen, BLACK, (WIDTH/2 + x, HEIGHT/2 + size + y, size, size), thick)

    if d:
        py.draw.rect(screen, RED, (WIDTH/2 + size + 1 + x, HEIGHT/2 + size + y, size, size))
    else:
        py.draw.rect(screen, BLACK, (WIDTH/2 + size + 1 + x, HEIGHT/2 + size + y, size, size), thick)

