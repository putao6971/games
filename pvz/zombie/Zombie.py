import os
import random
import pygame

from pvz.common_func import get_base_path


class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super(Zombie, self).__init__()
        self.image = pygame.image.load(os.path.join(get_base_path(), 'images/Zombie/pt/Zombie_000.png')).convert_alpha()
        self.images = [pygame.image.load(
            os.path.join(get_base_path(), 'images/Zombie/pt/Zombie_0{:02d}.png'.format(i))).convert_alpha() for i
                       in range(0, 47)]
        self.die_images = [pygame.image.load(
            os.path.join(get_base_path(), 'images/Zombie/die/Zombie_{:03d}.png'.format(i))).convert_alpha() for i
                           in range(134, 172)]
        self.attack_images = [pygame.image.load(
            os.path.join(get_base_path(), 'images/Zombie/pt/Zombie_{:03d}.png'.format(i))).convert_alpha() for i in
                              range(94, 133)]
        self.rect = self.images[0].get_rect()
        self.rect.top = 50 + random.randrange(0, 5) * 96
        self.energy = 10
        self.rect.left = 820
        self.speed = 1
        self.die_times = 0
        self.GO = False
        self.Alive = True

    def update(self, *args, **kwargs) -> None:
        if self.energy > 0:
            if self.GO:
                self.image = self.attack_images[args[0] % len(self.attack_images)]
            else:
                self.image = self.images[args[0] % len(self.images)]
            if self.rect.left > -120 and not self.GO:
                self.rect.left -= self.speed
        else:
            if self.die_times < 38:
                self.image = self.die_images[self.die_times]
                self.die_times += 1
            else:
                if self.die_times == 38:
                    self.Alive = False
                    self.kill()
