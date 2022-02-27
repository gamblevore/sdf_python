import numpy as np
import sys
import pygame
print(sys.version)

def length(x):
    return np.sqrt(np.dot(x, x))
def clamp(x, a, b):
    return max(min(x, b), a)
def normalize(vector):
    return vector / length(vector)
def distance(a, b):
    return length(a-b)
def reflect(ray, plane):
    return ray - 2 * np.dot(ray, plane) * plane


WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
Camera = np.array([0, 0, -1])
Sun = normalize(np.array([1000, 1000, -50]))
Obj = np.array([0.5, 1, 2])
Box = np.array([0.7, 0.3, 0.4])*2.0
yspeed = 0

def range_shift(x, a, a2, b, b2):
    return x*(b-a)+(a2+b2)


def length0(a, b, c):
    r = 0
    if a > 0:
        r += a*a
    if b > 0:
        r += b*b
    if c > 0:
        r += c*c
    return np.sqrt(r)


def max0(a,b,c):
    return min(max(a, b, c), 0)

def sdBoxFrame( p, b, e ):
    p = np.abs(p)-b
    q = np.abs(p+e)-e
    return min(
        length0(p[0], q[1], q[2]) + max0(p[0], q[1], q[2]),
        length0(q[0], p[1], q[2]) + max0(q[0], p[1], q[2]),
        length0(q[0], q[1], p[2]) + max0(q[0], q[1], p[2])
    )


def super_awesome_sdf(P, D):
    P -= Obj
    y = P[1]
    P[1] = y*0.5
    dist = sdBoxFrame(P, Box, 0.05)
    if dist > 0:
        return dist, None

    refl = reflect(Sun, normalize(P))
    strength = np.dot(refl, D)
    strength = clamp(strength, 0.0, 1.0)
    strength += 0.2

    oof = int(strength*255.0)
    oof = clamp(oof, 0, 255)
    return dist, pygame.Color(oof, oof//2, oof//4)


def sdf_caller(O, D):
    t = 0
    for step in range(30):
        curr = O + D*t
        move, col = super_awesome_sdf(curr, D)
        if col is not None:
            return col
        t += move + 0.0001

    return BLACK


def fill_frame(w, h, Surface):
    scale = 2.0 / np.array([w, h, 1.0])
    O = Camera
    for y in range(h):
        for x in range(w):
            P = np.array([x, y, 1]) * scale - 1.0
            col = sdf_caller(O, normalize(P))
            Surface.set_at((x, (h-1)-y), col)


def frame_action():
    global yspeed
    yspeed -= 0.05
    Obj[1] += yspeed
    if Obj[1] <= 0.0:
        yspeed = yspeed*-0.9


def frame_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    frame_action()
    return True


def run_game():
    print(sys.version)
    pygame.init()
    Dest = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("SDF")

    w = 100
    h = 100
    Surface = pygame.Surface((w, h))

    while frame_events():
        fill_frame(w, h, Surface)
        pygame.transform.scale(Surface, (600,600), Dest)
        pygame.display.flip()
    print("finished")


run_game()
