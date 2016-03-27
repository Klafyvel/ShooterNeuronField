from math import cos, sin, radians
import pygame
from pygame.locals import *

from settings import *


class GameObject:
    def __init__(self, pos=(0, 0), app=None, id=0):
        self.app = app
        self.surface = pygame.Surface((0, 0))
        self.pos = pos
        self.id = id

    def on_render(self, target):
        target.blit(self.surface, self.pos)

    def on_update(self):
        pass


class World(GameObject):
    def __init__(self, w, h, *args, **kwargs):
        super(World, self).__init__(*args, **kwargs)
        self.surface = pygame.Surface((w, h))
        self.surface.fill((200, 200, 200))
        pygame.draw.line(self.surface, (0, 0, 0), (w / 2 - w / 10, 0), (w / 2 - w / 10, h))
        pygame.draw.line(self.surface, (0, 0, 0), (w / 2 + w / 10, 0), (w / 2 + w / 10, h))


in_allowed_rec_w = lambda w: (w > 0 and w < 2 * WINDOW_WIDTH / 5) or (w > 3 * WINDOW_WIDTH / 5 and w < WINDOW_WIDTH)
in_allowed_rec_h = lambda h: (h > 0 and h < WINDOW_HEIGHT)

in_allowed_rec = lambda p: in_allowed_rec_w(p[0]) and in_allowed_rec_h(p[1])

in_window = lambda p: p[0] > 0 and p[0] < WINDOW_WIDTH and p[1] > 0 and p[1] < WINDOW_HEIGHT


class Character(GameObject):
    def __init__(self, color, *args, **kwargs):
        super(Character, self).__init__(*args, **kwargs)
        self.surface = pygame.Surface((64, 64))
        self.angle = 0

        self.field_angle = 30

        self.timer = pygame.time.Clock()

        self.color = color

    def reduce_field(self, v):
        n_v = self.field_angle - v
        if n_v >= 0:
            self.field_angle = n_v
        else:
            self.field_angle = 0

    def enlarge_field(self, v):
        n_v = self.field_angle + v
        if n_v <= 40:
            self.field_angle = n_v
        else:
            self.field_angle = 40

    def turn_left(self, v=CHARACTER_TURN_STEP):
        self.angle -= v

    def turn_right(self, v=CHARACTER_TURN_STEP):
        self.angle += v

    def shoot(self, v=None):
        self.timer.tick()
        if self.timer.get_time() >= BALL_SHOOT_PERIOD:
            vec = cos(radians(self.angle)), sin(radians(self.angle))
            self.app.add_object(Ball(vec, pos=self.pos, app=self.app))

    def forward(self, v=CHARACTER_MOVE_STEP):
        vec = (v * cos(radians(self.angle)), v * sin(radians(self.angle)))
        n_pos = int(self.pos[0] + vec[0]), int(self.pos[1] + vec[1])
        if in_allowed_rec(n_pos):
            self.pos = n_pos[:]

    def on_update(self):
        pass

    def on_render(self, target):
        pygame.draw.circle(target, self.color, self.pos, CHARACTER_SIZE)
        pos2 = (
            int(self.pos[0] + CHARACTER_SIZE / 2 * cos(radians(self.angle))),
            int(self.pos[1] + CHARACTER_SIZE / 2 * sin(radians(self.angle)))
        )
        pygame.draw.circle(target, (0, 0, 0), pos2, int(CHARACTER_SIZE / 2))


class Ball(GameObject):
    def __init__(self, dir, *args, **kwargs):
        super(Ball, self).__init__(*args, **kwargs)

        self.dir = dir

    def on_update(self):
        n_pos = int(self.dir[0] * V_BALL + self.pos[0]), int(self.dir[1] * V_BALL + self.pos[1])
        if in_window(n_pos):
            self.pos = n_pos[:]
        else:
            self.app.remove_object(self.id)

    def on_render(self, target):
        pygame.draw.circle(target, (0, 0, 0), self.pos, BALL_SIZE)
