from math import *

import pygame
from object.Object import Object
from pygame.math import Vector2

#보스의 발사체를 위한 총알 클래스 bullet class for boss bullet
class Bullet(Object): #extend Object
    def __init__(self, img_path, size, velocity, fire_loc, target_loc):
        super().__init__(img_path, size, velocity)
        #calculate direction from fire_loc to target_loc
        if((sqrt((target_loc[0] - fire_loc[0]) ** 2 + (target_loc[1] - fire_loc[1]) ** 2)) == 0):
            self.dx=1
            self.dy=1
        else:
            self.dx = int((velocity) * (target_loc[0] - fire_loc[0]) /
                            (sqrt((target_loc[0] - fire_loc[0]) ** 2 +
                                        (target_loc[1] - fire_loc[1]) ** 2)))
            self.dy = int((velocity) * (target_loc[1] - fire_loc[1]) /
                            (sqrt((target_loc[0] - fire_loc[0]) ** 2 +
                                        (target_loc[1] - fire_loc[1]) ** 2)))
        self.calc_dir(self.dx, self.dy)
        self.x = fire_loc[0]
        self.y = fire_loc[1]

    def move(self,boundary,game): #move bullet
        if (game.size[0] != self.boundary[0]) or (game.size[1] != self.boundary[1]):
            self.on_resize(game)
            self.calc_dir(self.dx, self.dy)
        self.x += self.dx
        self.y += self.dy
        self.update_rect((self.x, self.y))
        if self.y >= boundary[1] - self.sy or self.x>=boundary[0]-self.sx or self.x<0 or self.y< 0: #remove bullet if OOB
            game.enemyBullets.remove(self)

    def calc_dir(self, dx, dy):
        direction = Vector2(dx,dy)
        radius, angle = direction.as_polar()
        self.img = pygame.transform.rotozoom(self.img, -angle - 90.0, 1)



    
