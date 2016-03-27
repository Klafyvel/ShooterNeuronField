from math import cos, sin, radians
import pygame
from pygame.locals import *

from settings import *


class GameObject:
    """
    A generic object in the game.
    """
    def __init__(self, pos=(0, 0), app=None, id=0):
        self.app = app
        self.surface = pygame.Surface((0, 0))
        self.pos = pos
        self.id = id

    def on_render(self, target):
        """
        Render the object on the target.
        :param target: pygame.Surface on which the object is to be rendered.
        :return: None
        """
        target.blit(self.surface, self.pos)

    def on_update(self):
        """
        Updates the object.
        :return: None
        """
        pass


class World(GameObject):
    """
    A Simple object which doesn't interact whith the others objects.
    """
    def __init__(self, w, h, *args, **kwargs):
        super(World, self).__init__(*args, **kwargs)
        self.surface = pygame.Surface((w, h))
        self.surface.fill((200, 200, 200))
        pygame.draw.line(self.surface, (0, 0, 0), (w / 2 - w / 10, 0), (w / 2 - w / 10, h))
        pygame.draw.line(self.surface, (0, 0, 0), (w / 2 + w / 10, 0), (w / 2 + w / 10, h))


def in_allowed_rec_w(x):
    """
    Checks if the x coordinate is allowed for a character.
    :param x: The x coordinate which is to be tested.
    :return: Boolean
    """
    return (0 < x < 2 * WINDOW_WIDTH / 5) or (3 * WINDOW_WIDTH / 5 < x < WINDOW_WIDTH)


def in_allowed_rec_h(y):
    """
    Checks if the y coordinate is allowed for a character.
    :param y: The y coordinate which is to be tested.
    :return: Boolean
    """
    return 0 < y < WINDOW_HEIGHT


def in_allowed_rec(p):
    """
    Checks if a position is allowed for a character.
    :param p: The position which is to be tested.
    :return: Boolean
    """
    return in_allowed_rec_w(p[0]) and in_allowed_rec_h(p[1])


def in_window(p):
    """
    Checks if a position is in the window rectangle.
    :param p: The position which is to be tested.
    :return: Boolean
    """
    return 0 < p[0] < WINDOW_WIDTH and 0 < p[1] < WINDOW_HEIGHT


class Character(GameObject):
    """
    A Character in the game.
    """

    def __init__(self, character_color, *args, **kwargs):
        super(Character, self).__init__(*args, **kwargs)
        self.surface = pygame.Surface((64, 64))
        self.angle = 0

        self.field_angle = 30

        self.timer = pygame.time.Clock()

        self.color = character_color

    def reduce_field(self, v):
        """
        Reduces the vision field of the character by the given value.
        :param v: The value.
        :return: None
        """
        n_v = self.field_angle - v
        if n_v >= 0:
            self.field_angle = n_v
        else:
            self.field_angle = 0

    def enlarge_field(self, v):
        """
        Enlarges the vision of the character by the given value.
        :param v: The value.
        :return: None
        """
        n_v = self.field_angle + v
        if n_v <= 40:
            self.field_angle = n_v
        else:
            self.field_angle = 40

    def turn_left(self, v=CHARACTER_TURN_STEP):
        """
        Rotates in trigonometric direction the character by the given value.
        :param v: The value (default=settings.CHARACTER_TURN_STEP)
        :return: None
        """
        self.angle -= v

    def turn_right(self, v=CHARACTER_TURN_STEP):
        """
        Rotates in anti-trigonometric direction the character by the given value.
        :param v: The value (default=settings.CHARACTER_TURN_STEP)
        :return: None
        """
        self.angle += v

    def shoot(self, v=1):
        """
        Creates a Ball object in the application's objects list with the same direction as the player.
        :param v: Shoots only if v >= 1
        :return: None
        """
        if v <= 1:
            return
        self.timer.tick()
        if self.timer.get_time() >= BALL_SHOOT_PERIOD:
            vec = cos(radians(self.angle)), sin(radians(self.angle))
            self.app.add_object(Ball(vec, pos=self.pos, app=self.app))

    def forward(self, v=CHARACTER_MOVE_STEP):
        """
        Moves forward the character.
        :param v: The character move step. Cannot be > settings.CHARACTER_MOVE_STEP (default=CHARACTER_MOVE_STEP)
        :return: None
        """
        if v > CHARACTER_MOVE_STEP:
            v = CHARACTER_MOVE_STEP
        vec = (v * cos(radians(self.angle)), v * sin(radians(self.angle)))
        n_pos = int(self.pos[0] + vec[0]), int(self.pos[1] + vec[1])
        if in_allowed_rec(n_pos):
            self.pos = n_pos[:]

    def on_update(self):
        """
        Updates the character. (Currently unused)
        :return: None
        """
        pass

    def on_render(self, target):
        """
        Renders the character on the givent target.
        :param target: The target on which the character is to be rendered.
        :return: None
        """
        pygame.draw.circle(target, self.color, self.pos, CHARACTER_SIZE)
        pos2 = (
            int(self.pos[0] + CHARACTER_SIZE / 2 * cos(radians(self.angle))),
            int(self.pos[1] + CHARACTER_SIZE / 2 * sin(radians(self.angle)))
        )
        pygame.draw.circle(target, (0, 0, 0), pos2, int(CHARACTER_SIZE / 2))


class Ball(GameObject):
    """
    A Ball in the game.
    """
    def __init__(self, direction, *args, **kwargs):
        super(Ball, self).__init__(*args, **kwargs)

        self.direction = direction

    def on_update(self):
        """
        Updates the Ball.
        :return: None
        """
        n_pos = int(self.direction[0] * V_BALL + self.pos[0]), int(self.direction[1] * V_BALL + self.pos[1])
        if in_window(n_pos):
            self.pos = n_pos[:]
        else:
            self.app.remove_object(self.id)

    def on_render(self, target):
        """
        Renders the ball on the given target.
        :param target: The target on which the ball is to be rendered.
        :return: None
        """
        pygame.draw.circle(target, (0, 0, 0), self.pos, BALL_SIZE)
