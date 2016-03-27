import pygame
from pygame.locals import *

import game

from settings import *


class App:
    def __init__(self, window):
        self.window = window
        pygame.key.set_repeat(20, 20)

        self.running = False

        self.clock = pygame.time.Clock()

        w, h = self.window.get_width(), self.window.get_height()
        self.objects = [
            game.World(w, h, app=self),
            game.Character((255, 0, 0), (int(w / 4), int(h / 2)), app=self, id=1),
            game.Character((20, 255, 70), (int(3 * w / 4), int(h / 2)), app=self, id=2),
        ]

    def add_object(self, o):
        o.id = len(self.objects)
        self.objects.append(o)

    def remove_object(self, id):
        self.objects.pop(id)
        for o in self.objects[id:]:
            o.id -= 1

    def on_render(self):
        self.window.fill((0, 0, 0))
        for o in self.objects:
            o.on_render(self.window)

    def on_event(self, e):
        if e.type == QUIT:
            self.running = False
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                self.objects[1].forward()
            elif e.key == K_LEFT:
                self.objects[1].turn_left()
            elif e.key == K_RIGHT:
                self.objects[1].turn_right()
            elif e.key == K_SPACE:
                self.objects[1].shoot()

    def on_update(self):
        for o in self.objects:
            o.on_update()

    def on_mainloop(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_update()
            self.on_render()
            pygame.display.flip()
            pygame.display.set_caption(str(round(self.clock.get_fps(), 1)))
            self.clock.tick(60)

    def on_exit(self):
        pass


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    app = App(window)
    app.on_mainloop()
    app.on_exit()
    pygame.quit()
