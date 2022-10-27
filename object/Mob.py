import math
import random

import pygame
from data.Defs import *
from pygame.math import Vector2

from object.Effect import Boom
from object.Object import Object


class Mob(Object):
    def __init__(self, img_path, size, velocity, missile):
        super().__init__(img_path, size, velocity)
        self.missile = missile
        self.is_targeted = False
        self.direction = Vector2(1,1)
        self.rad = 1
        self.kill_sfx = pygame.mixer.Sound(Default.effect.value["boom"]["sound"])
        self.kill_sfx.set_volume(Default.sound.value["sfx"]["volume"])

    def move(self, boundary, game):
        if (game.size[0] != self.boundary[0]) or (game.size[1] != self.boundary[1]): #update when screen resized
            self.on_resize(game)

        self.x += self.direction.y
        self.y += self.direction.x
        self.rad+=0.04*self.velocity #속도에 적절한 값을 곱하여, 각도 변경
        self.direction.from_polar((self.velocity*3,math.cos(self.rad)*70)) #속도에 비례한 길이를 갖고, 방향 sin함수를 따르는 벡터를 다음 방향으로 지정

        if self.y >= boundary[1] - self.sy:
            game.mobList.remove(self)

    def destroy(self, game):
        self.kill_sfx.play()
        boom = Boom(game.animation.animations["destroy_effect"])
        mob_location = {"x":self.x+(self.sx/2), "y":self.y+(self.sy/2)}
        boom.set_XY((mob_location["x"] - boom.sx/2, mob_location["y"]- boom.sy/2))
        game.effect_list.append(boom)
        if self in game.mobList:
            game.mobList.remove(self)
                        

        