import random
import time

import pygame
from data.Defs import *

from object.Character import Character
from object.Effect import Effect
from object.Object import Object


# 아이템 기본 클래스
class Item(Object):
    # 각 아이템은 해당 클래스를 상속 받음
    
    # Attributes :
    # self.x_inv : x축 이동방향의 반전 여부 (bool)
    # self.y_inv : y축 이동방향의 반전 여부 (bool)
    # self.spawned : 아이템 생성된 시간 (float)
    # self.blink_count : 깜빡임 애니메이션 중 다음 프레임까지 지난 시간 (float)
    # self.inc : 다음 애니메이션까지 지난 시간 (float)
    # self.inc_delay : 애니메이션 사이클이 끝나고 다시 반복할 때까지 걸리는 시간 (float)
    # self.sfx : 아이템 획득 효과음 (sound)
    def __init__(self, frames, frames_trans, anim_id):
        super().__init__("", Default.item.value["size"], Default.item.value["velocity"], frames, frames_trans, anim_id)
        self.x_inv = random.choice([True, False])
        self.y_inv = False
        self.spawned = time.time()
        self.blink_count = 0.0
        self.inc = 0.0
        self.inc_delay = 0.0
        self.sfx = pygame.mixer.Sound(Default.item.value["sound"])
        self.sfx.set_volume(Default.sound.value["sfx"]["volume"])

    # 아이템 이동 메소드
    def move(self, game): 
        if (game.size[0] != self.boundary[0]) or (game.size[1] != self.boundary[1]):
            self.on_resize(game)
        if self.x_inv == False:
            self.x += self.velocity
        else:
            self.x -= self.velocity
        if self.y_inv == False:
            self.y += self.velocity
        else:
            self.y -= self.velocity
        if self.x <= 0:
            self.x_inv = False
        elif self.y <= 0:
            self.y_inv = False
        elif self.x >= self.boundary[0] - self.sx:
            self.x_inv = True
        elif self.y >= self.boundary[1] - self.sy:
            self.y_inv = True
        # rect 위치 업데이트
        self.update_rect((self.x, self.y))
        # 애니메이션 재생
        self.inc += Default.animation.value["speed"]
        self.inc = Utils.clamp(self.inc, 0.0, self.frame_count-1)
        if self.inc >= self.frame_count-1:
            self.inc_delay += Default.animation.value["speed"]
            if self.inc_delay >= Default.animation.value["interval"]:
                self.inc = 0.0
                self.inc_delay = 0.0
        self.current_frame = int(self.inc)
        if self.is_transparent == False:
            self.img = self.frames[int(self.inc)]
        else:
            self.img = self.frames_trans[int(self.inc)]
        # 아이템 생성 후 일정 시간 경과 시 깜빡이면서 소멸
        time_passed = time.time() - self.spawned
        time_left = Default.item.value["duration"] - time_passed 
        if time_left > 0:
            if time_left <= Default.animation.value["blink"]["duration"]:
                self.blink_count += Default.animation.value["blink"]["speed"]
                if(self.blink_count >= Default.animation.value["blink"]["frame"]):
                    if self.is_transparent == False:
                        self.img = self.frames_trans[int(self.inc)]
                        self.blink_count = 0.0
                        self.is_transparent = True
                    else:
                        self.img = self.frames[int(self.inc)]
                        self.blink_count = 0.0
                        self.is_transparent = False
        else:
            game.item_list.remove(self)

class Bomb(Item):
    # 폭탄 아이템: 획득 시 폭탄 카운터 증가
    def __init__(self, animation):
        super().__init__(animation.frames, animation.frames_trans, "bomb")

    # 캐릭터와 충돌 시  바로 실행
    def use(self, game):
        if self.is_collidable == True:
            self.sfx.play()
            game.character.bomb_count+=1
            self.is_collidable = False
            game.item_list.remove(self)

class Coin(Item):
    # 코인 아이템: 획득 시 보유하고 있는 코인 증가
    def __init__(self, animation):
        super().__init__(animation.frames, animation.frames_trans, "coin")

    # 캐릭터와 충돌 시  바로 실행
    def use(self, game):
        if self.is_collidable == True:
            self.sfx.play()
            game.coin += 1
            self.is_collidable = False
            game.item_list.remove(self)

class Health(Item):
    # 목숨 아이템: 획득 시 목숨 증가
    def __init__(self, animation):
        super().__init__(animation.frames, animation.frames_trans, "health")

    # 캐릭터와 충돌 시  바로 실행
    def use(self, game):
        if self.is_collidable == True:
            self.sfx.play()
            game.life += 1
            self.is_collidable = False
            game.item_list.remove(self)

class PowerUp(Item):
    # 파워업 아이템: 획득 시 캐릭터 발사체 개수 증가
    def __init__(self, animation):
        super().__init__(animation.frames, animation.frames_trans, "powerup")

    # 캐릭터와 충돌 시  바로 실행
    def use(self, game):
        if self.is_collidable == True:
            self.sfx.play()
            fire_count = game.character.fire_count + 1
            n_min = Default.character.value["missile"]["min"]
            n_max = Default.character.value["missile"]["max"]
            if fire_count > n_max:
                game.character.auto_target = True
            game.character.fire_count  = Utils.clamp(fire_count, n_min, n_max)
            self.is_collidable = False
            game.item_list.remove(self)

class SpeedUp(Item):
    # 스피드업 아이템: 획득 시 캐릭터 이동/발사 속도 증가
    def __init__(self, animation):
        super().__init__(animation.frames, animation.frames_trans, "speedup")
        
    # 캐릭터와 충돌 시  바로 실행
    def use(self, game):
        if self.is_collidable == True:
            self.sfx.play()
            self.used = time.time()
            self.org_velocity = game.character.velocity
            self.org_fire_interval = game.character.fire_interval
            game.character.speed_up()
            self.is_collidable = False
            game.item_list.remove(self)
