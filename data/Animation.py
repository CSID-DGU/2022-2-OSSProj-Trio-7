import pygame

from data.Defs import *


class AnimationManager():
    # 게임 시작 시 애니메이션 클래스를 미리 생성하는 객체
    
    # Attributes :
    # self.animations : 각종 애니메이션 클래스들의 집합 (dict)
    def __init__(self):
        self.animations = {
            "bomb_effect": BombEffectAnim(),
            "destroy_effect": DestroyEffectAnim(),
            "bomb": BombAnim(),
            "powerup": PowerupAnim(),
            "speedup": SpeedupAnim(),
            "coin": CoinAnim(),
            "health": HealthAnim()
        }

    # 화면 크기 조정 시 모든 애니메이션 프레임을 업데이트
    def on_resize(self, game):
        for key, value in self.animations.items():
            value.on_resize(game)

class Animation():
    # 애니메이션 프레임 이미지를 미리 불러와 저장하는 객체
    # 각 애니메이션은 해당 클래스를 상속 받음
    
    # Attributes :
    # self.boundary : 현재 창 크기 (tuple)
    # self.org_boundary : 기본 창 크기(현재 창크기와 비교하여 이미지 확대/축소 비율 계산) (tuple)
    # self.frame_paths : 각 애니메이션 프레임 이미지의 파일 경로 (list)
    # self.size : 애니메이션 이미지의 크기 (dict)
    # self.frames : 애니메이션 프레임 이미지를 갖고 있는 리스트 (list)
    # self.frames_trans : 동일 이미지에 투명도를 입힌 리스트 (list)
    def __init__(self, frame_paths, size):
        self.boundary = pygame.display.get_surface().get_size()
        self.org_boundary = [Default.game.value["size"]["x"],Default.game.value["size"]["y"]]
        self.frame_paths = frame_paths
        self.size = size
        self.load_frames()

    # 모든 파일 경로로부터 이미지 불러오기
    def load_frames(self):
        self.frames = []
        self.frames_trans = []
        x_scale = self.boundary[0]/self.org_boundary[0]
        y_scale = self.boundary[1]/self.org_boundary[1]
        x = int(self.size["x"]*x_scale)
        y = int(self.size["y"]*y_scale)
        for idx in range(len(self.frame_paths)):
            img = pygame.image.load(self.frame_paths[idx]).convert_alpha()
            img = pygame.transform.scale(img,(x,y))
            img_copy = img.copy()
            img_copy.fill(Color.TRANSPARENT.value, None, pygame.BLEND_RGBA_MULT)
            self.frames.append(img)
            self.frames_trans.append(img_copy)

    # 이미지 크기 조정 후 다시 불러오기
    # 이미지 크기가 조정될 때마다 이미지 품질이 저하됨으로 다시 pygame에서 불러옴
    def on_resize(self, game):
        self.boundary = game.size
        self.load_frames()

class BombEffectAnim(Animation):
    # 폭탄 폭발 효과 애니메이션 객체 
    def __init__(self):
        super().__init__(Default.effect.value["bomb"]["frames"], Default.effect.value["bomb"]["size"])

class DestroyEffectAnim(Animation):
    # 적 파괴 효과 애니메이션 객체 
    def __init__(self):
        super().__init__(Default.effect.value["boom"]["frames"], Default.effect.value["boom"]["size"])

class BombAnim(Animation):
    # 폭탄 아이템 애니메이션 객체 
    def __init__(self):
        super().__init__(Default.item.value["bomb"]["frames"], Default.item.value["size3"])

class PowerupAnim(Animation):
    # 파워업 아이템 애니메이션 객체 
    def __init__(self):
        super().__init__(Default.item.value["powerup"]["frames"], Default.item.value["size2"])

class SpeedupAnim(Animation):
    # 스피드업 아이템 애니메이션 객체 
    def __init__(self):
        super().__init__(Default.item.value["speedup"]["frames"], Default.item.value["size"])

class HealthAnim(Animation):
    # 목숨 아이템 애니메이션 객체 
    def __init__(self):
        super().__init__(Default.item.value["health"]["frames"], Default.item.value["size"])

class CoinAnim(Animation):
    # 코인 아이템 애니메이션 객체 
    def __init__(self):
        super().__init__(Default.item.value["coin"]["frames"], Default.item.value["size"])
