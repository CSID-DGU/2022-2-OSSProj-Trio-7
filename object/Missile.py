import pygame
from data.Defs import *
from pygame.math import Vector2
from pymysql import NULL

from object.Object import Object


class Missile(Object):
    # 캐릭터 발사체 객체

    # Attributes:
    # power : 공격력 (int)
    def __init__(self, img_path, size, power):
        self.boundary = pygame.display.get_surface().get_size()
        super().__init__(img_path, size, Default.character.value["missile"]["speed"])
        self.power = power

    # 미사일 이동 
    def update(self, game):
        if (game.size[0] != self.boundary[0]) or (game.size[1] != self.boundary[1]):
            self.on_resize(game)
        self.y -= self.velocity

class TargetedMissile(Missile):
    # 적의 위치로 추적하는 유도탄 객체

    # Attributes
    # game : 현재 실행 중인 게임 모드
    # vel : 적이 있는 방향 * 속도 (vector2)
    # position : 현재 미사일 위치 (vector2)
    # target : 추적하고 있는 객체 
    # locked_on : 추적 여부 (bool)
    # crosshair : 적 조준 시 표시되는 오브젝트 (crosshar)
    # direction : 적의 방향 (vector2)
    # velocity : 미사일의 이동 속도 (int)
    # img : 미사일 이미지 (surface)
    def __init__(self, position, game, power):
        super().__init__(Images.weapon_target_missile.value, {"x":15, "y":25}, power)
        self.game = game
        self.vel = Vector2(0,0)
        self.position = Vector2(position[0]-self.sx/2, position[1]-self.sy)
        self.target = self.find_target(game)
        self.locked_on = True
        self.crosshair = Crosshair(self.target)
        if self.target in game.mobList:
            direction = Vector2(self.target.get_pos()) - self.position
            radius, angle = direction.as_polar()
            self.img = pygame.transform.rotozoom(self.img, -angle - 90.0, 1)
            self.vel = direction.normalize() * self.velocity
        if hasattr(game, "stage"):
            if game.stage.is_boss_stage:
                direction = Vector2(self.target.get_pos()) - self.position
                radius, angle = direction.as_polar()
                self.img = pygame.transform.rotozoom(self.img, -angle - 90.0, 1)
                self.vel = direction.normalize() * self.velocity

    # 화면에 있는 적들 중에서 가장 근접한 타깃 탐색
    # 보스가 있으면 일반 몹 대신 보스만 조준
    def find_target(self, game):
        if hasattr(game, "stage"): 
            if game.stage.is_boss_stage:
                self.target_type = "BOSS"
                return game.boss
            elif len(game.mobList) > 0:
                targets = game.character.check_for_targets(game)
                if len(targets) > 0:
                    target = targets[0]
                    min = Utils.get_distance({"x":target.x,"y":target.y},{"x":game.character.x,"y":game.character.y}) 
                    for enemy in targets:
                        if min > Utils.get_distance({"x":enemy.x,"y":enemy.y},{"x":game.character.x,"y":game.character.y}):
                            min = Utils.get_distance({"x":enemy.x,"y":enemy.y},{"x":game.character.x,"y":game.character.y})
                            target = enemy
                    self.target_type = "MOB"
                    target.is_targeted = True
                    return target    
                else:
                    self.target_type = "NULL"
        else:
            if len(game.mobList) > 0:
                targets = game.character.check_for_targets(game)
                if len(targets) > 0:
                    target = targets[0]
                    min = Utils.get_distance({"x":target.x,"y":target.y},{"x":game.character.x,"y":game.character.y}) 
                    for enemy in targets:
                        if min > Utils.get_distance({"x":enemy.x,"y":enemy.y},{"x":game.character.x,"y":game.character.y}):
                            min = Utils.get_distance({"x":enemy.x,"y":enemy.y},{"x":game.character.x,"y":game.character.y})
                            target = enemy
                    self.target_type = "MOB"
                    target.is_targeted = True
                    return target
                else:
                    self.target_type = "NULL"
            
    # 화면에 있는 적들 중에서 가장 근접한 타깃 탐색
    # 보스가 있으면 일반 몹 대신 보스만 조준
    def find_target_pvp(self, game):
        #pvp
        self.target_pvp = self.find_target_pvp(game)
        if len(game.mobList) > 0:
            targets1 = game.character1.check_for_targets(game)
            if len(targets1) > 0:
                target = targets1[0]
                min = Utils.get_distance({"x":target.x,"y":target.y},{"x":game.character1.x,"y":game.character1.y}) 
                for enemy in targets1:
                    if min > Utils.get_distance({"x":enemy.x,"y":enemy.y},{"x":game.character1.x,"y":game.character1.y}):
                        min = Utils.get_distance({"x":enemy.x,"y":enemy.y},{"x":game.character1.x,"y":game.character1.y})
                        target = enemy
                self.target_type = "MOB"
                target.is_targeted = True
                return target
            else:
                self.target_type = "NULL"

        if len(game.mobList) > 0:
            targets2 = game.character2.check_for_targets(game)
            if len(targets2) > 0:
                target = targets2[0]
                min = Utils.get_distance({"x":target.x,"y":target.y},{"x":game.character2.x,"y":game.character2.y}) 
                for enemy in targets2:
                    if min > Utils.get_distance({"x":enemy.x,"y":enemy.y},{"x":game.character2.x,"y":game.character2.y}):
                        min = Utils.get_distance({"x":enemy.x,"y":enemy.y},{"x":game.character2.x,"y":game.character2.y})
                        target = enemy
                self.target_type = "MOB"
                target.is_targeted = True
                return target
            else:
                self.target_type = "NULL"

    # 적을 향해 미사일 이동
    def update(self, game):
        if (game.size[0] != self.boundary[0]) or (game.size[1] != self.boundary[1]):
            self.on_resize(game)
        if self.target_type == "BOSS":
            self.crosshair.move(game)
            direction = Vector2(self.target.get_pos()) - self.position
            self.put_img(self.img_path)
            radius, angle = direction.as_polar()
            self.vel = direction.normalize() * self.velocity
            self.img = pygame.transform.rotozoom(self.img, -angle - 90.0, 1)
        elif self.target in game.mobList:
            self.crosshair.move(game)
            direction = Vector2(self.target.get_pos()) - self.position
            self.put_img(self.img_path)
            radius, angle = direction.as_polar()
            self.vel = direction.normalize() * self.velocity
            self.img = pygame.transform.rotozoom(self.img, -angle - 90.0, 1)
        else:
            self.locked_on = False
        self.position += self.vel 
        self.velocity += Default.character.value["missile"]["speed_inc"]
        self.x = self.position[0] 
        self.y = self.position[1]

class Crosshair(Object):
    # 유도탄 발사 시 생성되는 객체
    # 적 파괴 시 같이 화면에서 사라짐

    # target : 추적 중인 객체
    def __init__(self, target):
        super().__init__(Default.effect.value["crosshair"]["image"], Default.effect.value["crosshair"]["size"], Default.effect.value["crosshair"]["velocity"])
        self.target = target
    
    # 추적 중인 객체의 위치로 이동
    def move(self, game):
        if (game.size[0] != self.boundary[0]) or (game.size[1] != self.boundary[1]):
            self.on_resize(game)
        if self.target in game.mobList: 
            self.set_XY((self.target.get_pos()[0]-self.sx/2, self.target.get_pos()[1]-self.sy/2))
        elif hasattr(game, "stage"):
            if game.stage.is_boss_stage:
                self.set_XY((self.target.get_pos()[0]-self.sx/2, self.target.get_pos()[1]-self.sy/2))
