import pygame

from data.Defs import *


class Object:
    # 이미지를 가진 모든 객체는 해당 클래스를 상속 받음(Boss 객체 제외)

    # Attributes:
    # boundary : 현재 창 크기 (tuple)
    # org_boundary : 창 크기 기본값 (tuple)
    # x : x축 위치 (int)
    # y : y축 위치 (int)
    # img_path : 오브젝트 이미지의 경로 (string)
    # size : 이미지의 원본 크기 (dict)
    # sx : 현재 이미지의 넓이 (int)
    # sy : 현재 이미지의 높이 (int)
    # rect : 이미지의 크기에 따라 생성되는 삭각형(픽셀 단위 충돌 대신 사각형으로 충돌 감지) (rect)
    # velocity : 오브젝트의 이동속도 (int)
    # frames : 애니메이션 객체로부터 받은 이미지 리스트 (list)
    # frames_trans : 애니메이션 객체로부터 받은 투명도가 입혀진 이미지 리스트 (list)
    # frame_count : 애니메이션 프레임 개수 (int)
    # is_collidable : 현재 오브젝트의 충돌 가능여부 (bool)
    # is_transparent : 깜빡임 애니메이션 중 이미지 투명 여부 (bool)
    # anim_id : 화면 조정 시 애니메이션 업데이트를 위한 아이디 값 (string)
    # current_frame : 현재 표시되는 애니메이션 프레임 인덱스 (int)
    def __init__(self, img_path, size, velocity, frames=[], frames_trans=[], anim_id=""):
        self.boundary = pygame.display.get_surface().get_size()
        self.org_boundary = [Default.game.value["size"]["x"],Default.game.value["size"]["y"]]
        self.x =0
        self.y=0
        self.img_path = img_path
        self.size = size
        self.sx = size["x"]
        self.sy = size["y"]
        self.rect = pygame.Rect(0, 0, self.sx, self.sy)
        self.velocity = velocity
        self.frames = frames
        self.frames_trans = frames_trans
        self.frame_count = len(frames)
        self.is_collidable = True
        self.is_transparent = False
        if self.frame_count > 0:
            self.anim_id = anim_id
            self.current_frame = 0 
            self.put_imgs()
        else:
            self.put_img(img_path)
            self.change_size()

    # 화면 크기 변경 시 애니메이션 관리자 객체로부터 프레임을 다시 받아옴 
    def reload_frames(self, game):
        for key, value in game.animation.animations.items():
            if self.anim_id == key:
                self.frames = value.frames
                self.frames_trans = value.frames_trans
                self.put_imgs()

    # 이미지 불러오기
    # png 파일은 추가 변환 작업 필요
    def put_img(self,address):
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()
        else: 
            self.img = pygame.image.load(address)
        self.change_size()

    # 애니메이션 불러오기
    def put_imgs(self):
        if self.is_transparent:
            self.img = self.frames_trans[self.current_frame]
        else:
            self.img = self.frames[self.current_frame]
        self.sx, self.sy = self.img.get_size()
        self.rect.size = (self.sx, self.sy)

    # 오브젝트의 위치 설정
    def set_XY(self,loc):
        self.x = loc[0]
        self.y = loc[1]
        self.update_rect(loc)

    # 오브젝트의 위치에 따라 rect 업데이트
    def update_rect(self, loc):
        self.rect.topleft = loc

    # 피사체의 그림 조정
    def change_size(self):
        x_scale = self.boundary[0]/self.org_boundary[0]
        y_scale = self.boundary[1]/self.org_boundary[1]
        x = int(self.size["x"]*x_scale)
        y = int(self.size["y"]*y_scale)
        self.img = pygame.transform.scale(self.img,(x,y)) # 그림의 크기를 조정한다.
        self.img_copy = self.img.copy()
        self.img_trans = self.img.copy()
        self.img_trans.fill(Color.TRANSPARENT.value, None, pygame.BLEND_RGBA_MULT)
        self.sx, self.sy = self.img.get_size()
        self.rect.size = (self.sx, self.sy)
        if self.is_transparent:
            self.img = self.img_trans
        else:
            self.img = self.img_copy

    # 화면에 오브젝트 표시
    def show(self, screen):
        screen.blit(self.img,(self.x,self.y))

    # 이미지의 불투명한 픽셀 단위로 충돌 감지
    # 이미지에 투명도가 있는 부분은 충돌 감지되지 않음(깜빡임 애니메이션 등)
    def check_crash(self, o2):
        o1_mask = pygame.mask.from_surface(self.img)
        o2_mask = pygame.mask.from_surface(o2.img)

        offset = (int(o2.x - self.x), int(o2.y - self.y))
        collision = o1_mask.overlap(o2_mask, offset)
        
        if collision:
            return True
        else:
            return False

    # rect 속성으로 충돌 감지
    # 픽셀 단위로 감지하는 것 보다 비용 낮음
    # 대량의 오브젝트가 한번에 충돌할 경우 사용(폭탄 사용)
    def rect_collide(self, rect):
        return self.rect.colliderect(rect)

    # 창 크기 변경 시 오브젝트 업데이트
    def on_resize(self, game):
        old_boundary = self.boundary
        self.boundary = game.size
        if self.frame_count > 0:
            self.reload_frames(game)
        else: 
            self.put_img(self.img_path)
        self.reposition(old_boundary)

    # 화면 크기 변경 비율에 따라 오브젝트의 위치 업데이트
    def reposition(self, old_boundary):
        x_scale = self.x/old_boundary[0]
        y_scale = self.y/old_boundary[1]
        x = int(self.boundary[0] * x_scale)
        y = int(self.boundary[1] * y_scale)
        self.set_XY((x, y))
    
    # 오브젝트의 현재 위치 반환
    def get_pos(self):
        return (self.x + (self.sx/2), self.y + (self.sy/2))
