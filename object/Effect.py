import time

import pygame

from data.Defs import *
from object.Object import Object


class Effect(Object):
    # 모든 효과는 해당 클래스를 상속 받음
    
    # Attributes:
    # occurred : 효과 발생 시간 (float)
    # inc : 다음 애니메이션 프레임까지 지난 시간 (float)
    # anim_speed : 프레임 전환 속도 (float)
    def __init__(self, frames, frames_trans, size, velocity, anim_id):
        super().__init__("", size, velocity, frames, frames_trans, anim_id)
        self.occurred = time.time()
        self.inc = 0.0
        self.anim_speed = Default.effect.value["speed"]

    # 화면 상에서 효과를 이동시키고 다음 애니메이션 프레임으로 전환
    def move(self, game):
        if (game.size[0] != self.boundary[0]) or (game.size[1] != self.boundary[1]):
            self.on_resize(game)
        self.y += self.velocity
        self.inc += self.anim_speed
        self.inc = Utils.clamp(self.inc, 0.0, self.frame_count-1)
        self.current_frame = int(self.inc)
        self.img = self.frames[int(self.inc)]
        self.update_rect((self.x, self.y))

class Explosion(Effect):
    # 폭발 효과 객체
    
    # Attributes :
    # duration : 애니메이션 지속 시간
    def __init__(self, animation):
        super().__init__(animation.frames, animation.frames_trans, Default.effect.value["bomb"]["size"], Default.effect.value["velocity"], "bomb_effect")
        self.duration = Default.effect.value["bomb"]["duration"]
    
    # 폭발 효과 범위 내 있는 적과 보스에게 피해를 입힘
    def move(self, game):
        super().move(game)
        # 애니메이션이 끝나면 소멸
        if int(self.inc) >= self.frame_count-1:
            game.effect_list.remove(self)
        else:
            # 충돌하는 적을 파괴
            for enemy in list(game.mobList):
                if self.check_crash(enemy):
                    enemy.destroy(game)
                    game.score += 10
            # 충돌하는 보스 발사체 없앰
            if hasattr(game, "stage"):
                if game.stage.is_boss_stage:
                    for bullet in game.enemyBullets:
                        if self.rect_collide(bullet.rect):
                            if bullet in game.enemyBullets:
                                game.enemyBullets.remove(bullet)

class Boom(Effect):
    # 적 파괴 효과
    def __init__(self, animation):
        super().__init__(animation.frames, animation.frames_trans, Default.effect.value["boom"]["size"], Default.effect.value["velocity"], "destroy_effect")
        self.duration = Default.effect.value["boom"]["duration"]
    
    # 애니메이션이 끝나면 소멸
    def move(self, game):
        super().move(game)
        if int(self.inc) >= self.frame_count-1:
            game.effect_list.remove(self)
