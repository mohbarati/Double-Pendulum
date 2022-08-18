from math import sqrt, copysign

import pygame
from pygame.locals import *

pygame.init()

# create the display surface object
sc = pygame.display.set_mode((600, 600))

# set the pygame window name
pygame.display.set_caption("Double Pendulum")


def ceiling(x, y):
    """Draws the ceiling as a rectangle"""
    x += 300
    y += 300
    pygame.draw.polygon(
        sc,
        (100, 255, 30),
        [
            (x - 50, y - 50),
            (x + 50, y - 50),
            (x + 50, y),
            (x - 50, y),
        ],
    )


def distance(x, y):
    """Finding magnitude of a vector
    Args:
        x (float): x-component
        y (float): y-component
    Returns:
        float : vector size
    """
    return sqrt(x**2 + y**2)


def draw_circle(c, x, y, r):
    pygame.draw.circle(sc, c, (int(x + 300), int(y + 300)), r)


def draw_line(c, x1, y1, x2, y2):
    pygame.draw.line(
        sc, c, (int(x1 + 300), int(y1 + 300)), (int(x2 + 300), int(y2 + 300))
    )


# constants and initial condition
xb = 0
yb = 0
x1 = 50
y1 = -150
d1 = distance(x1, y1)
l1 = d1
k1 = 1000
m1 = 1
vx1 = 0
vy1 = 0
x2 = 150
y2 = -150
d2 = distance(x2 - x1, y2 - y1)
l2 = d2
k2 = 1000
m2 = 1
vx2 = 0
vy2 = 0
g = -1
dt = 0.01
r = 10
damping = 0.001


draw_circle((255, 0, 255), x1, y1, r)
draw_circle((0, 255, 0), x2, y2, r)
draw_line((100, 100, 100), x1, y1, x2, y2)

pygame.display.update()
cont = True
while cont:
    ceiling(xb, yb)
    draw_line((0, 0, 0), x1, y1, xb, yb)
    draw_line((0, 0, 0), x1, y1, x2, y2)
    draw_circle((0, 0, 0), x2, y2, r)
    draw_circle((0, 0, 0), x1, y1, r)

    d2 = distance(x2 - x1, y2 - y1)
    d1 = distance(x1, y1)

    T2 = -k2 * (d2 - l2)
    T1 = -k1 * (d1 - l1)

    ax2 = T2 / m2 * (x2 - x1) / d2 - damping * abs(vx2) * copysign(1, vx2)
    ay2 = T2 / m2 * (y2 - y1) / d2 - g - damping * abs(vx2) * copysign(1, vy2)
    ax1 = (
        T1 / m1 * (x1) / d1
        + T2 / m1 * (x1 - x2) / d2
        - damping * abs(vx2) * copysign(1, vx1)
    )
    ay1 = (
        T1 / m1 * (y1) / d1
        + T2 / m1 * (y1 - y2) / d2
        - g
        - damping * abs(vx2) * copysign(1, vy1)
    )

    vx2 += ax2 * dt
    vy2 += ay2 * dt
    vx1 += ax1 * dt
    vy1 += ay1 * dt

    x2 += vx2 * dt
    y2 += vy2 * dt
    x1 += vx1 * dt
    y1 += vy1 * dt
    draw_line((100, 100, 100), x1, y1, xb, yb)
    draw_line((100, 100, 100), x1, y1, x2, y2)
    draw_circle((0, 255, 0), x2, y2, r)
    draw_circle((255, 0, 255), x1, y1, r)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                cont = False
            if event.type == QUIT:
                cont = False
pygame.quit()
