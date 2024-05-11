import os

import pygame

print(os.getcwd())


class SunFlower(pygame.sprite.Sprite):
    def __init__(self, last_time, rect):

        super(SunFlower, self).__init__()
        self.image = pygame.image.load(os.path.join(os.getcwd(), 'images/SunFlower/SunFlower00.png')).convert_alpha()
        self.images = [pygame.image.load(
            f"{os.path.join(os.getcwd(), 'images/SunFlower/SunFlower{:02d}.png')}".format(i)).convert_alpha() for i
                       in range(0, 25)]
        self.rect = self.images[0].get_rect()
        self.energy = 60
        self.rect.left = rect[0]
        self.rect.top = rect[1]
        self.last_time = last_time
        self.zombies = set()

    def update(self, *args):
        for zombie in self.zombies:
            if not zombie.Alive:
                self.energy += 0
            else:
                self.energy -= 1
        if self.energy <= 0:
            for zombie in self.zombies:
                zombie.GO = False
            self.kill()

        self.image = self.images[args[0] % len(self.images)]
