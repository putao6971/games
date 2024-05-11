import os

import pygame

from pvz.common_func import get_base_path


class Bullet(pygame.sprite.Sprite):
    def __init__(self, peashooter_rect, background_size):
        super(Bullet, self).__init__()
        self.image = pygame.image.load(os.path.join(get_base_path(), 'images/BulletPea1.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = peashooter_rect[0] + 65
        self.rect.top = peashooter_rect[1] + 13
        self.width = background_size[0]
        self.speed = 6

    def update(self, *args, **kwargs) -> None:
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.kill()
