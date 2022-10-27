import time

import pygame

from data.Defs import *
from object.Effect import Explosion
from object.Missile import *
from object.Object import Object


class Character(Object):
    # 플레이어가 조종하는 캐릭터 객체

    # Attributes :
    # name : 캐릭터 이름 (string)
    # velocity : 캐릭터 이동 속도 (int)
    # org_velocity : 캐릭터 이동 속도 기본값 (int)
    # missile_img : 발사체 이미지 경로 (string)
    # missile_size : 발사체 이미지 크기 (dict)
    # missile_sfx_path : 미사일 효과음 경로 (string)
    # missile_sfx : 미사일 효과음 (sound)
    # bomb_sfx : 폭탄 효과음 (sound)
    # missile_power : 미사일의 공격력 (int)
    # org_fire_interval : 발사 간격 기본값 (float)
    # fire_interval : 발사 간격(값이 작을 수록 발사속도 빠름) (float)
    # price : 캐릭터 가격 (int)
    # bomb_count : 현재 소지하고 있는 폭탄 개수 (int)
    # fire_count : 현재 발사체 개수 (int)
    # missiles_fired : 발사된 미사일 리스트 (list)
    # last_fired : 마지막으로 공격한 시간 (float)
    # last_bomb : 마지막으로 폭탄 사용한 시간 (float)
    # last_crashed : 마지막으로 충돌한 시간 (float)
    # blink_count : 깜빡임 애니메이션을 위해 다음 프레임까지 지난 시간 (float)
    # auto_target : 유도탄 발사 여부 (bool)
    # is_booasted : 속도 증가 여부 (bool)
    def __init__(self, name, img_path, velocity, missile_img, missile_size, 
                missile_sfx, missile_power, fire_interval, price):
        super().__init__(img_path, Default.character.value["size"], velocity)
        self.name = name
        self.org_velocity = velocity
        self.missile_img = missile_img
        self.missile_size = missile_size
        self.missile_sfx_path = missile_sfx
        self.missile_sfx =  pygame.mixer.Sound(missile_sfx)
        self.missile_sfx.set_volume(Default.sound.value["sfx"]["volume"])
        self.bomb_sfx = pygame.mixer.Sound(Default.effect.value["bomb"]["sound"])
        self.bomb_sfx.set_volume(Default.sound.value["sfx"]["volume"])
        self.missile_power = missile_power
        self.org_fire_interval = fire_interval
        self.fire_interval = fire_interval
        self.price = price

    # 게임 시작 시 캐릭터 초기화를 위해 필수적으로 실행
    def reinitialize(self, game):
        size = game.size
        # 캐릭터 사이즈/위치 초기화
        self.on_resize(game)
        self.set_XY((size[0]/2-(self.sx/2),size[1]-self.sy))
        # 폭탄/발사체 관련 변수 초기화
        self.bomb_count = 0
        self.fire_count = Default.character.value["missile"]["min"]
        self.missiles_fired = []
        # 발사속도, 폭탄 사용 간격, 충돌 후 무적기간 판단을 위해 시간 초기화
        self.last_fired = 0.0
        self.last_bomb = 0.0
        self.last_crashed = 0.0
        # 깜빡임 애니메이션 카운터 초기화
        self.blink_count = 0.0
        # 유도탄 발사 여부 초기화(발사체를 최대치 이상으로 증가시켰을 때 True)
        self.auto_target = False
        # 이동/발사 속도 초기화
        self.is_boosted = False
        self.velocity = self.org_velocity
        self.fire_interval = self.org_fire_interval

# pvp게임 시작 시 캐릭터 초기화를 위해 필수적으로 실행
    def pvp_reinitialize1(self, game):
        size = game.size
        # 캐릭터 사이즈/위치 초기화
        self.on_resize(game)
        self.set_XY((size[0]/4-(self.sx/2),size[1]-self.sy))
        # 폭탄/발사체 관련 변수 초기화
        self.bomb_count = 0
        self.fire_count = Default.character.value["missile"]["min"]
        self.missiles_fired = []
        # 발사속도, 폭탄 사용 간격, 충돌 후 무적기간 판단을 위해 시간 초기화
        self.last_fired = 0.0
        self.last_bomb = 0.0
        self.last_crashed = 0.0
        # 깜빡임 애니메이션 카운터 초기화
        self.blink_count = 0.0
        # 유도탄 발사 여부 초기화(발사체를 최대치 이상으로 증가시켰을 때 True)
        self.auto_target = False
        # 이동/발사 속도 초기화
        self.is_boosted = False
        self.velocity = self.org_velocity
        self.fire_interval = self.org_fire_interval

# pvp게임 시작 시 캐릭터 초기화를 위해 필수적으로 실행
    def pvp_reinitialize2(self, game):
        size = game.size
        # 캐릭터 사이즈/위치 초기화
        self.on_resize(game)
        self.set_XY(((size[0]/4)*3-(self.sx/2),size[1]-self.sy))
        # 폭탄/발사체 관련 변수 초기화
        self.bomb_count = 0
        self.fire_count = Default.character.value["missile"]["min"]
        self.missiles_fired = []
        # 발사속도, 폭탄 사용 간격, 충돌 후 무적기간 판단을 위해 시간 초기화
        self.last_fired = 0.0
        self.last_bomb = 0.0
        self.last_crashed = 0.0
        # 깜빡임 애니메이션 카운터 초기화
        self.blink_count = 0.0
        # 유도탄 발사 여부 초기화(발사체를 최대치 이상으로 증가시켰을 때 True)
        self.auto_target = False
        # 이동/발사 속도 초기화
        self.is_boosted = False
        self.velocity = self.org_velocity
        self.fire_interval = self.org_fire_interval

    # 게임 실행 중 입력 키에 따라 캐릭터 이동, 발사 등의 액션을 수행
    def update(self, game):
        if (game.size[0] != self.boundary[0]) or (game.size[1] != self.boundary[1]):
            self.on_resize(game)
        # 키 입력 감지
        key_pressed = pygame.key.get_pressed()
        # 캐릭터 이동(방향키)
        # 캐릭터가 창 밖으로 이동할 수 없도록 boundary 값과 비교
        if key_pressed[pygame.K_LEFT]:
            self.x -= self.velocity
            if self.x < 0:
                self.x = 0
        if key_pressed[pygame.K_RIGHT]:
            self.x += self.velocity
            if self.x >= self.boundary[0] - self.sx:
                self.x = self.boundary[0] - self.sx
        if key_pressed[pygame.K_UP]:
            self.y -= self.velocity
            if self.y < 0:
                self.y = 0
        if key_pressed[pygame.K_DOWN]:
            self.y += self.velocity
            if self.y >= self.boundary[1] - self.sy:
                self.y = self.boundary[1] - self.sy
        if key_pressed[pygame.K_SPACE]:
            if time.time() - self.last_fired > self.fire_interval:
                self.shoot()
                if self.auto_target:
                    self.shoot_targeted(game)
        if key_pressed[pygame.K_a]:
            if self.bomb_count > 0:
                if time.time() - self.last_bomb > Default.item.value["bomb"]["interval"]:
                    self.use_bomb(game)
                    self.bomb_count-=1
        # 속도 증가 아이템을 얻고 일정 시간 이후 능력치를 다시 원래대로 초기화
        if self.is_boosted == True:
            if time.time() - self.boosted > Default.item.value["powerup"]["duration"]:
                self.velocity = self.org_velocity
                self.fire_interval = self.org_fire_interval
                self.is_boosted = False
        # 무적상태인 경우 깜빡임 효과 적용
        if self.is_collidable == False:
            time_passed = time.time() - self.last_crashed
            self.blink_count += Default.animation.value["blink"]["speed"]
            if game.life > 0:
                if(self.blink_count >= Default.animation.value["blink"]["frame"]):
                    if(self.is_transparent == False):
                        self.img = self.img_trans
                        self.blink_count = 0.0
                        self.is_transparent = True
                    else:
                        self.img = self.img_copy
                        self.blink_count = 0.0
                        self.is_transparent = False
                if time_passed > Default.character.value["invincible_period"]:
                    self.is_collidable = True
                    if(self.is_transparent):
                        self.img = self.img_copy
                        self.is_transparent = False
        # 캐릭터 rect 위치 업데이트
        self.update_rect((self.x, self.y))
        # 화면 밖으로 나간 미사일 삭제
        for missile in list(self.missiles_fired):
            missile.update(game)
            if missile.y < -missile.sy:
                if missile in self.missiles_fired:
                    self.missiles_fired.remove(missile)


# pvp player1게임 실행 중 입력 키에 따라 캐릭터 이동, 발사 등의 액션을 수행
    def pvp_update1(self, game):
        if (game.size[0] != self.boundary[0]) or (game.size[1] != self.boundary[1]):
            self.on_resize(game)
        # 키 입력 감지
        key_pressed = pygame.key.get_pressed()
        # 캐릭터 이동(방향키)
        # 캐릭터가 창 밖으로 이동할 수 없도록 boundary 값과 비교
        if key_pressed[pygame.K_a]:
            self.x -= self.velocity
            if self.x < 0:
                self.x = 0
        if key_pressed[pygame.K_d]:
            self.x += self.velocity
            if self.x >= self.boundary[0]/2 - self.sx:
                self.x = self.boundary[0]/2 - self.sx
        if key_pressed[pygame.K_w]:
            self.y -= self.velocity
            if self.y < 0:
                self.y = 0
        if key_pressed[pygame.K_s]:
            self.y += self.velocity
            if self.y >= self.boundary[1] - self.sy:
                self.y = self.boundary[1] - self.sy
        if key_pressed[pygame.K_SPACE]:
            if time.time() - self.last_fired > self.fire_interval:
                self.shoot()
                if self.auto_target:
                    self.shoot_targeted(game)
        '''if key_pressed[pygame.K_a]:
            if self.bomb_count > 0:
                if time.time() - self.last_bomb > Default.item.value["bomb"]["interval"]:
                    self.use_bomb(game)
                    self.bomb_count-=1'''
        # 속도 증가 아이템을 얻고 일정 시간 이후 능력치를 다시 원래대로 초기화
        if self.is_boosted == True:
            if time.time() - self.boosted > Default.item.value["powerup"]["duration"]:
                self.velocity = self.org_velocity
                self.fire_interval = self.org_fire_interval
                self.is_boosted = False
        # 무적상태인 경우 깜빡임 효과 적용
        if self.is_collidable == False:
            time_passed = time.time() - self.last_crashed
            self.blink_count += Default.animation.value["blink"]["speed"]
            if game.life_player1 > 0:
                if(self.blink_count >= Default.animation.value["blink"]["frame"]):
                    if(self.is_transparent == False):
                        self.img = self.img_trans
                        self.blink_count = 0.0
                        self.is_transparent = True
                    else:
                        self.img = self.img_copy
                        self.blink_count = 0.0
                        self.is_transparent = False
                if time_passed > Default.character.value["invincible_period"]:
                    self.is_collidable = True
                    if(self.is_transparent):
                        self.img = self.img_copy
                        self.is_transparent = False
        # 캐릭터 rect 위치 업데이트
        self.update_rect((self.x, self.y))
        # 화면 밖으로 나간 미사일 삭제
        for missile in list(self.missiles_fired):
            missile.update(game)
            if missile.y < -missile.sy:
                if missile in self.missiles_fired:
                    self.missiles_fired.remove(missile)
    

# pvp player 2 게임 실행 중 입력 키에 따라 캐릭터 이동, 발사 등의 액션을 수행
    def pvp_update2(self, game):
        if (game.size[0] != self.boundary[0]) or (game.size[1] != self.boundary[1]):
            self.on_resize(game)
        # 키 입력 감지
        key_pressed = pygame.key.get_pressed()
        # 캐릭터 이동(방향키)
        # 캐릭터가 창 밖으로 이동할 수 없도록 boundary 값과 비교
        if key_pressed[pygame.K_LEFT]:
            self.x -= self.velocity
            if self.x < self.boundary[0]/2:
                self.x = self.boundary[0]/2
        if key_pressed[pygame.K_RIGHT]:
            self.x += self.velocity
            if self.x >= self.boundary[0] - self.sx:
                self.x = self.boundary[0] - self.sx
        if key_pressed[pygame.K_UP]:
            self.y -= self.velocity
            if self.y < 0:
                self.y = 0
        if key_pressed[pygame.K_DOWN]:
            self.y += self.velocity
            if self.y >= self.boundary[1] - self.sy:
                self.y = self.boundary[1] - self.sy
        if key_pressed[pygame.K_m]:
            if time.time() - self.last_fired > self.fire_interval:
                self.shoot()
                if self.auto_target:
                    self.shoot_targeted(game)
        '''if key_pressed[pygame.K_a]:
            if self.bomb_count > 0:
                if time.time() - self.last_bomb > Default.item.value["bomb"]["interval"]:
                    self.use_bomb(game)
                    self.bomb_count-=1'''
        # 속도 증가 아이템을 얻고 일정 시간 이후 능력치를 다시 원래대로 초기화
        if self.is_boosted == True:
            if time.time() - self.boosted > Default.item.value["powerup"]["duration"]:
                self.velocity = self.org_velocity
                self.fire_interval = self.org_fire_interval
                self.is_boosted = False
        # 무적상태인 경우 깜빡임 효과 적용
        if self.is_collidable == False:
            time_passed = time.time() - self.last_crashed
            self.blink_count += Default.animation.value["blink"]["speed"]
            if game.life_player2 > 0:
                if(self.blink_count >= Default.animation.value["blink"]["frame"]):
                    if(self.is_transparent == False):
                        self.img = self.img_trans
                        self.blink_count = 0.0
                        self.is_transparent = True
                    else:
                        self.img = self.img_copy
                        self.blink_count = 0.0
                        self.is_transparent = False
                if time_passed > Default.character.value["invincible_period"]:
                    self.is_collidable = True
                    if(self.is_transparent):
                        self.img = self.img_copy
                        self.is_transparent = False
        # 캐릭터 rect 위치 업데이트
        self.update_rect((self.x, self.y))
        # 화면 밖으로 나간 미사일 삭제
        for missile in list(self.missiles_fired):
            missile.update(game)
            if missile.y < -missile.sy:
                if missile in self.missiles_fired:
                    self.missiles_fired.remove(missile)
    
    # 발사체 공격 
    def shoot(self):
        self.last_fired = time.time()
        self.missile_sfx.play()
        for num in range(1, self.fire_count+1):
            missile = Missile(self.missile_img, self.missile_size, self.missile_power)
            missile.change_size()
            div_factor = self.fire_count + 1
            missile.x = round((self.x + (num * (self.sx / div_factor))) - missile.sx / 2) 
            missile.y = self.y - missile.sy
            self.missiles_fired.append(missile)

    # 유도탄 발사 공격
    def shoot_targeted(self, game):
        targets = self.check_for_targets(game)
        if len(targets) > 0:
            x = round(self.x + (self.sx / 2)) 
            y = self.y
            missile = TargetedMissile((x,y), game, self.missile_power)
            self.missiles_fired.append(missile)
        elif hasattr(game, "stage"):
            if game.stage.is_boss_stage:
                x = round(self.x + (self.sx / 2)) 
                y = self.y
                missile = TargetedMissile((x,y), game, self.missile_power)
                self.missiles_fired.append(missile)

    # 유도탄으로 조준 가능한 적의 존재여부 확인
    def check_for_targets(self, game):
        targets = []
        for enemy in game.mobList:
            if enemy.is_targeted == False:
                targets.append(enemy)
        return targets

    # 폭탄 공격
    def use_bomb(self, game):
        self.last_bomb = time.time()
        self.bomb_sfx.play()
        explosion = Explosion(game.animation.animations["bomb_effect"])
        player_location = {"x":self.x+(self.sx/2), "y":self.y+(self.sy/2)}
        explosion.set_XY((player_location["x"] - explosion.sx/2, player_location["y"]- explosion.sy/2))
        game.effect_list.append(explosion)

    # 발사된 미사일의 리스트를 반환
    def get_missiles_fired(self):
        return self.missiles_fired

    # 스피드업 아이템 획득 시 캐릭터의 이동/발사 속도 상승
    def speed_up(self):
        self.boosted = time.time()
        self.velocity = self.org_velocity + 5
        self.fire_interval = self.org_fire_interval/3.0
        self.is_boosted = True

    # json 오브젝트로 변환 시 전달할 속성 값 정의(surface 포함한 이미지 전달 시 오류 발생함으로 제외)
    def json_dump_obj(self) -> dict:
        _data = {}
        char_dict = self.__dict__
        for key, value in char_dict.items():
            _data[key] = value
        return {
            "name": self.name,
            "img_path": self.img_path,
            "velocity": self.org_velocity,
            "missile_img": self.missile_img,
            "missile_size": self.missile_size,
            "missile_sfx": self.missile_sfx_path,
            "missile_power": self.missile_power,
            "fire_interval": self.org_fire_interval,
            "price": self.price
        }
