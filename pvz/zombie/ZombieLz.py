import os

import pygame

from pvz.common_func import get_base_path
from pvz.zombie.Zombie import Zombie


class ZombieLz(Zombie):
    def __init__(self):
        super(ZombieLz, self).__init__()
        self.image = pygame.image.load(os.path.join(get_base_path(), 'images/Zombie/lz/Zombie_000.png')).convert_alpha()
        self.images_lz = [pygame.image.load(
            os.path.join(get_base_path(), 'images/Zombie/lz/Zombie_0{:02d}.png'.format(i))).convert_alpha()
                          for i in range(0, 47)]
        self.attack_lz = [pygame.image.load(
            os.path.join(get_base_path(), 'images/Zombie/lz/Zombie_{:03d}.png'.format(i))).convert_alpha()
                          for i in range(94, 134)]
        self.energy = 27

    def update(self, *args, **kwargs) -> None:
        if self.energy > 10:
            if self.GO:
                self.image = self.attack_lz[args[0] % len(self.attack_lz)]
            else:
                self.image = self.images_lz[args[0] % len(self.images_lz)]
            if self.rect.left > -120 and not self.GO:
                self.rect.left -= self.speed
        elif 0 < self.energy <= 10:
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
