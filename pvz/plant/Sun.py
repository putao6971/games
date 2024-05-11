import os

import pygame
import random

from pvz.common_func import get_base_path


class Sun(pygame.sprite.Sprite):
    def __init__(self, rect):
        super(Sun, self).__init__()
        self.image = pygame.image.load(os.path.join(get_base_path(), 'images/Sun/Sun_01.png')).convert_alpha()
        self.images = [
            pygame.image.load(os.path.join(get_base_path(), 'images/Sun/Sun_{:02d}.png'.format(i))).convert_alpha()
            for i in range(1, 14)]
        self.rect = self.images[1].get_rect()
        offset_top = random.randint(-25, 25)
        offset_left = random.randint(-25, 25)
        self.rect.top = rect.top + offset_top
        self.rect.left = rect.left + offset_left

    def update(self, *args):
        self.image = self.images[args[0] % len(self.images)]
