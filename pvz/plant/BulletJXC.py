import os

import pygame

from pvz.common_func import get_base_path


class BulletJXC(pygame.sprite.Sprite):
    def __init__(self, jxc_rect, background_size, life1):
        super(BulletJXC, self).__init__()
        self.image = pygame.image.load(os.path.join(get_base_path(), 'images/bullet_0.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = jxc_rect[0] + 50
        self.rect.top = jxc_rect[1]
        self.width = background_size[0]
        self.life2 = int(life1 / 120) - int(jxc_rect[1] / 200) - 4
        self.speed = 10 + self.life2
        self.a = 0

    def update(self, *args, **kwargs) -> None:
        if self.rect.right < self.width:
            self.rect.left += self.speed
            if self.a < 100:
                y = 12 - self.a
                self.rect.top -= int(y)
                self.a += 0.5
        else:
            self.kill()
