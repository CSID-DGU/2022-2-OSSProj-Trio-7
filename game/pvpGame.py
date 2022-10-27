import pygame
import pygame_menu
import sys
import random
from pygame.locals import *
import time
from boss.Boss import Boss
from boss.Bullet import Bullet
from data.Animation import AnimationManager

import random
import time
from collections import OrderedDict
from typing import Sized

import pygame
import pygame_menu
from boss.Boss import Boss
from boss.Bullet import Bullet
from data.Animation import AnimationManager
from data.CharacterDataManager import *
from data.Defs import *
from data.StageDataManager import *
from object.Item import *
#from object.Mob import Mob
from pygame_menu.utils import make_surface
from data.Defs import User
from data.database_user import *

from pygame.math import Vector2 #mob.py에서 가져옴
from object.Effect import Boom
from object.Object import Object
from button import *

import time

class pvp :
    
    def __init__(self,character_data,character1,character2,stage):

        # 1. 게임초기화 
        pygame.init()
        self.stage_cleared = False

        # 2. 게임창 옵션 설정
        infoObject = pygame.display.Info()
        title = "PVP game"
        pygame.display.set_caption(title) # 창의 제목 표시줄 옵션
        self.size = [infoObject.current_w,infoObject.current_h]
        self.screen = pygame.display.set_mode(self.size,pygame.RESIZABLE)
        self.scale = (self.size[0]*0.00015,self.size[1]*0.00015)
        self.font_size = self.size[0] * 40 //720

        # 3. 게임 내 필요한 설정
        self.clock = pygame.time.Clock() # 이걸로 FPS설정함

        # 4. 게임에 필요한 객체들을 담을 배열 생성, 변수 초기화, pvp
        self.animation = AnimationManager()
        self.mobList = []
        self.item_list = []
        self.effect_list = []
        self.enemyBullets =[]
        self.character_data = character_data

        self.goal_time = 120 # play 120초
        self.character1 = character1 # player1 character
        self.character2 = character2 # player2 character
        self.score_player1 = 0 # player1 score
        self.score_player2 = 0 # player2 score
        self.life_player1 = 3 # player1 life
        self.life_player2 = 3 # player2 life

        self.startTime = time.time()
        self.mob_gen_rate = 0.01
        self.mob_velocity = 2
        self.mob_image = "./Image/catthema/attack/cat_att.png"
        #self.background_image = stage.background_image
        self.background_image = "Image/catthema/map1.png"
        self.gameover_image1 = "Image/catthema/win1_.png"
        self.gameover_image2 = "Image/catthema/win2_.png"
        self.gameover_image3 = "Image/catthema/same.png"
        self.background_music = "./Sound/bgm/bensound-evolution.wav"
        self.k = 0
        self.SB = 0
        #self.infowindow_image = "Image/catthema/map1.png"

        # 5. 캐릭터 초기화
        self.character1.pvp_reinitialize1(self)
        self.character2.pvp_reinitialize2(self)

        # 방향키 
        self.direction1 = {None: (0, 0), pygame.K_w: (0, -2), pygame.K_s: (0, 2),
                    pygame.K_a: (-2, 0), pygame.K_d: (2, 0)} #player1

        self.direction2 = {None: (0, 0), pygame.K_UP: (0, -2), pygame.K_DOWN: (0, 2),
                    pygame.K_LEFT: (-2, 0), pygame.K_RIGHT: (2, 0)} #playter2
        mytheme = pygame_menu.themes.THEME_ORANGE.copy()
        self.menu = pygame_menu.Menu('PVP.', self.size[0], self.size[1],
                            theme=mytheme)

    def main(self, screen):
        # 메인 이벤트
        pygame.mixer.init()
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        
        while self.SB==0:
            #fps 제한을 위해 한 loop에 한번 반드시 호출해야합니다.
            self.clock.tick(30)

            #화면 흰색으로 채우기
            self.screen.fill(Color.WHITE.value)
            
            # pvp 모드를 위한 배경 분리
            background1 = pygame.image.load(self.background_image)
            background2 = pygame.image.load(self.background_image)
            background1 = pygame.transform.scale(background1, (self.size[0]/2,self.size[1])) #왼쪽
            background2 = pygame.transform.scale(background2, (self.size[0]/2,self.size[1])) #오른쪽
            background1_width = background1.get_width()
            background1_height = background1.get_height()
            background2_width = background2.get_width()
            background2_height = background2.get_height()
            background1_copy = background1.copy()
            background2_copy = background2.copy()

            self.screen.blit(background1,  [0,0]) 
            self.screen.blit(background1, [self.size[0]/2, 0])

            start_ticks = pygame.time.get_ticks()

            # 입력 처리
            for event in pygame.event.get(): #동작을 했을때 행동을 받아오게됨
                if event.type ==pygame.QUIT:
                    self.SB=1 # SB 가 1이되면 while 문을 벗어나오게 됨
                '''if event.type == pygame.KEYDOWN: # 어떤 키를 눌렀을때!(키보드가 눌렸을 때)
                    if event.key == pygame.K_x:
                        self.SB=1
                    if event.key == pygame.K_z: #테스트용
                        self.score += 30'''
                if event.type == pygame.VIDEORESIZE: #창크기가 변경되었을 때
                    #화면 크기가 최소 300x390은 될 수 있도록, 변경된 크기가 그것보다 작으면 300x390으로 바꿔준다
                    width, height = max(event.w,300), max(event.h,390)

                    #크기를 조절해도 화면의 비율이 유지되도록, 가로와 세로 중 작은 것을 기준으로 종횡비(10:13)으로 계산
                    if(width<=height):
                        height = int(width * (13/10))
                    else:
                        width = int(height * (10/13))
                    
                    self.size =[width,height] #게임의 size 속성 변경
                    self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE) #창 크기 세팅
                    self.check_resize(screen)
                    self.animation.on_resize(self)

            #몹을 확률적으로 발생시키기
            if(random.random()<self.mob_gen_rate):
                newMob = Mob(self.mob_image,{"x":50, "y":50},self.mob_velocity,0)
                newMob.set_XY((random.randrange(0,self.size[0]),0)) #set mob location randomly
                self.mobList.append(newMob)
            
            if random.random() < Default.item.value["powerup"]["spawn_rate"]:
                new_item = PowerUp(self.animation.animations["powerup"])
                new_item.set_XY((random.randrange(0,self.size[0]-new_item.sx),0))
                self.item_list.append(new_item)


            if random.random() < Default.item.value["health"]["spawn_rate"]:
                new_item = Health(self.animation.animations["health"])
                new_item.set_XY((random.randrange(0,self.size[0]-new_item.sx),0))
                self.item_list.append(new_item)

            if random.random()< Default.item.value["speedup"]["spawn_rate"]:
                new_item = SpeedUp(self.animation.animations["speedup"])
                new_item.set_XY((random.randrange(0,self.size[0]-new_item.sx),0))
                self.item_list.append(new_item)
            
            #몹 객체 이동
            for mob in self.mobList:
                mob.move(self.size,self)

            for item in self.item_list:
                item.move(self)

            for effect in self.effect_list:
                effect.move(self)

            #적 투사체 이동
            for bullet in self.enemyBullets:
                bullet.move(self.size,self)
                bullet.show(self.screen)

            for item in list(self.item_list):
                if item.rect_collide(self.character1.rect):
                    item.use1(self, self.character1)
                if item.rect_collide(self.character2.rect):
                    item.use2(self, self.character2)

            #발사체와 몹 충돌 감지(player1)
            for missile in list(self.character1.get_missiles_fired()):
                for mob in list(self.mobList):
                    if self.check_crash(missile,mob):
                        self.score_player1 += 10
                        if missile in self.character1.missiles_fired:
                            self.character1.missiles_fired.remove(missile)
                        mob.destroy(self)

            #발사체와 몹 충돌 감지(player2)
            for missile in list(self.character2.get_missiles_fired()):
                for mob in list(self.mobList):
                    if self.check_crash(missile,mob):
                        self.score_player2 += 10
                        if missile in self.character2.missiles_fired:
                            self.character2.missiles_fired.remove(missile)
                        mob.destroy(self)

            #몹과 플레이어 충돌 감지
            for mob in list(self.mobList):
                if(self.check_crash(mob,self.character1)):
                    if self.character1.is_collidable == True:
                        self.character1.last_crashed = time.time()
                        self.character1.is_collidable = False
                        print("crash!")
                        self.life_player1 -= 1
                        mob.destroy(self)

            for mob in list(self.mobList):
                if(self.check_crash(mob,self.character2)):
                    if self.character2.is_collidable == True:
                        self.character2.last_crashed = time.time()
                        self.character2.is_collidable = False
                        print("crash!")
                        self.life_player2 -= 1
                        mob.destroy(self)

            #화면 그리기
            for effect in self.effect_list:
                effect.show(self.screen)

            #캐릭터 그리기
            self.character1.show(self.screen)
            self.character2.show(self.screen)

            #몹 그리기
            for mob in self.mobList:
                mob.show(self.screen)

            for item in list(self.item_list):
                item.show(self.screen)

            for i in self.character1.get_missiles_fired():
                i.show(self.screen)
                if hasattr(i, "crosshair"):
                    if i.locked_on == True:
                        i.crosshair.show(self.screen)
            
            for i in self.character2.get_missiles_fired():
                i.show(self.screen)
                if hasattr(i, "crosshair"):
                    if i.locked_on == True:
                        i.crosshair.show(self.screen)

            #점수와 목숨, 타이머 표시
            font = pygame.font.Font(Default.font.value, self.size[0]//40)
            play_time = time.gmtime(time.time() - self.startTime)
            timer = self.goal_time - play_time.tm_sec
            time_score_life_text1 = font.render("Time : {:} Score : {} Life: {} ".format(timer,self.score_player1,self.life_player1), True, Color.YELLOW.value) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔
            time_score_life_text2 = font.render("Time : {:} Score : {} Life: {} ".format(timer,self.score_player2,self.life_player2), True, Color.YELLOW.value) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔
            self.screen.blit(time_score_life_text1,(10,15)) # 이미지화 한 텍스트라 이미지를 보여준다고 생각하면 됨
            self.screen.blit(time_score_life_text2,(10+self.size[0]/2,15)) # 이미지화 한 텍스트라 이미지를 보여준다고 생각하면 됨
                        

            # 만약 시간이 0 이하이면 게임 종료
            if timer <= 0:
                pygame.mixer.music.stop()
                pygame.mixer.Sound(Default.item.value["sound"]).stop()
                pygame.mixer.Sound(Default.effect.value["boom"]["sound"]).stop()
                font2 = pygame.font.Font(Default.font.value, self.size[0]//20)
                if self.score_player1 > self.score_player2:
                    pygame.mixer.music.stop()
                    self.win1 = pygame.image.load(self.gameover_image1)
                    self.win1 = pygame.transform.scale(self.win1, (self.size[0],self.size[1]))
                    self.screen.fill(Color.BLACK.value)
                    self.screen.blit(self.win1,  [0,0])
                    score_player1 = font2.render("Player1 Score : {} ".format(self.score_player1), True, Color.WHITE.value) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔
                    score_player2 = font2.render("Player2 Score : {} ".format(self.score_player2), True, Color.WHITE.value)
                    self.screen.blit(score_player1,(self.size[0]/3-15,self.size[1]/2+80))
                    self.screen.blit(score_player2,(self.size[0]/3-15,self.size[1]/2+120))
                    
                if self.score_player2 > self.score_player1:
                    pygame.mixer.music.stop()
                    self.win2 = pygame.image.load(self.gameover_image2)
                    self.win2 = pygame.transform.scale(self.win2, (self.size[0],self.size[1]))
                    self.screen.fill(Color.BLACK.value)
                    self.screen.blit(self.win2,  [0,0])
                    score_player1 = font2.render("Player1 Score : {} ".format(self.score_player1), True, Color.WHITE.value) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔
                    score_player2 = font2.render("Player2 Score : {} ".format(self.score_player2), True, Color.WHITE.value)
                    self.screen.blit(score_player1,(self.size[0]/3-15,self.size[1]/2+80))
                    self.screen.blit(score_player2,(self.size[0]/3-15,self.size[1]/2+120))

                if self.score_player1 == self.score_player2:
                    pygame.mixer.music.stop()
                    self.same = pygame.image.load(self.gameover_image3)
                    self.same = pygame.transform.scale(self.same, (self.size[0],self.size[1]))
                    self.screen.fill(Color.BLACK.value)
                    self.screen.blit(self.same,  [0,0])
                    score_player1 = font2.render("Player1 Score : {} ".format(self.score_player1), True, Color.WHITE.value) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔
                    score_player2 = font2.render("Player2 Score : {} ".format(self.score_player2), True, Color.WHITE.value)
                    self.screen.blit(score_player1,(self.size[0]/3-15,self.size[1]/2+80))
                    self.screen.blit(score_player2,(self.size[0]/3-15,self.size[1]/2+120))
                

            #목숨이 0 이하면 게임 종료 화면
            if(self.life_player1<1):
                pygame.mixer.music.stop()
                pygame.mixer.Sound(Default.item.value["sound"]).stop()
                pygame.mixer.Sound(Default.effect.value["boom"]["sound"]).stop()
                self.win1 = pygame.image.load(self.gameover_image2)
                self.win1 = pygame.transform.scale(self.win1, (self.size[0],self.size[1]))
                self.screen.fill(Color.BLACK.value)
                self.screen.blit(self.win1,  [0,0])
                

            #목숨이 0 이하면 게임 종료 화면
            if(self.life_player2<1):
                pygame.mixer.music.stop()
                pygame.mixer.Sound(Default.item.value["sound"]).stop()
                pygame.mixer.Sound(Default.effect.value["boom"]["sound"]).stop()
                self.win2 = pygame.image.load(self.gameover_image1)
                self.win2 = pygame.transform.scale(self.win2, (self.size[0],self.size[1]))
                self.screen.fill(Color.BLACK.value)
                self.screen.blit(self.win2,  [0,0])
                

            pygame.display.update()

            self.character1.pvp_update1(self)
            self.character2.pvp_update2(self)

            pygame.display.flip()

        pygame.mixer.music.stop()  

            #pygame.display.update()

#충돌 감지 함수
    def check_crash(self,o1,o2):
        o1_mask = pygame.mask.from_surface(o1.img)
        o2_mask = pygame.mask.from_surface(o2.img)

        offset = (int(o2.x - o1.x), int(o2.y - o1.y))
        collision = o1_mask.overlap(o2_mask, offset)
        
        if collision:
            return True
        else:
            return False

    def pvp_info(self):
        self.check_resize(self.screen)
        self.infopvp_img = "./Image/catthema/pvp_help.png"
        self.menu.add.image(self.infopvp_img, scale=Scales.default.value)
        infowindow = pygame.image.load(self.infopvp_img)
        infowindow = pygame.transform.scale(infowindow, self.size)
        self.screen.blit(infowindow, [0,0])
        pygame.display.flip()
        time.sleep(3) # 3초뒤에 게임 시작.
        self.main(self.screen)

    # 화면 크기 조정 감지 및 비율 고정
    def check_resize(self,screen):
        if (self.size != screen.get_size()): #현재 사이즈와 저장된 사이즈 비교 후 다르면 변경
            changed_screen_size = self.screen.get_size() #변경된 사이즈
            ratio_screen_size = (changed_screen_size[0],changed_screen_size[0]*783/720) #y를 x에 비례적으로 계산
            if(ratio_screen_size[0]<320): #최소 x길이 제한
                ratio_screen_size = (494,537)
            if(ratio_screen_size[1]>783): #최대 y길이 제한
                ratio_screen_size = (720,783)
            screen = pygame.display.set_mode(ratio_screen_size,
                                                    pygame.RESIZABLE)


class Mob(Object):
    def __init__(self, img_path, size, velocity, missile):
        super().__init__(img_path, size, velocity)
        self.x_inv = random.choice([True, False]) #추가
        self.y_inv = False #추가
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
        #self.direction.from_polar((self.velocity*3,math.cos(self.rad)*70)) #속도에 비례한 길이를 갖고, 방향 sin함수를 따르는 벡터를 다음 방향으로 지정
        if self.x_inv == False:
            self.x += self.velocity*3
        else:
            self.x -= self.velocity*3
        if self.y_inv == False:
            self.y += self.velocity*3
        else:
            self.y -= self.velocity*3
        if self.x <= 0:
            self.x_inv = False
        elif self.y <= 0:
            self.y_inv = False
        elif self.x >= self.boundary[0]/2 - self.sx and self.x<= self.boundary[0]/2:
            self.x_inv = True
        elif self.x > self.boundary[0]/2 and self.x <= self.boundary[0]/2 + self.sx/2:
            self.x_inv = False
        elif self.x >= self.boundary[0]-self.sx:
            self.x_inv = True
        elif self.y >= self.boundary[1] - self.sy:
            game.mobList.remove(self)
        # rect 위치 업데이트
        self.update_rect((self.x, self.y))
        

    def destroy(self, game):
        self.kill_sfx.play()
        boom = Boom(game.animation.animations["destroy_effect"])
        mob_location = {"x":self.x+(self.sx/2), "y":self.y+(self.sy/2)}
        boom.set_XY((mob_location["x"] - boom.sx/2, mob_location["y"]- boom.sy/2))
        game.effect_list.append(boom)
        if self in game.mobList:
            game.mobList.remove(self)

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
        if (game.size[0] != self.boundary[0]/2) or (game.size[1] != self.boundary[1]):
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
        elif self.x >= self.boundary[0]/2 - self.sx and self.x<= self.boundary[0]/2:
            self.x_inv = True
        elif self.x > self.boundary[0]/2 and self.x <= self.boundary[0]/2 + self.sx/2:
            self.x_inv = False
        elif self.x >= self.boundary[0]-self.sx:
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




class Health(Item):
    # 목숨 아이템: 획득 시 목숨 증가
    def __init__(self, animation):
        super().__init__(animation.frames, animation.frames_trans, "health")

    # 캐릭터와 충돌 시  바로 실행(player1)
    def use1(self, game, character1):
        self.character1 = character1 # player1 character
        if self.character1.is_collidable == True:
            self.sfx.play()
            game.life_player1 += 1
            self.character1.is_collidable = False
            game.item_list.remove(self)

    # 캐릭터와 충돌 시  바로 실행(player2)
    def use2(self, game, character2):
        self.character2 = character2 # player2 character
        if self.character2.is_collidable == True:
            self.sfx.play()
            game.life_player2 += 1
            self.character2.is_collidable = False
            game.item_list.remove(self)

class PowerUp(Item):
    # 파워업 아이템: 획득 시 캐릭터 발사체 개수 증가
    def __init__(self, animation):
        super().__init__(animation.frames, animation.frames_trans, "powerup")

    # 캐릭터와 충돌 시  바로 실행(player1)
    def use1(self, game, character1):
        self.character1 = character1 # player1 character
        if self.character1.is_collidable == True:
            self.sfx.play()
            fire_count = game.character1.fire_count + 1
            n_min = Default.character.value["missile"]["min"]
            n_max = Default.character.value["missile"]["max"]
            if fire_count > n_max:
                game.character1.auto_target = True
            game.character1.fire_count  = Utils.clamp(fire_count, n_min, n_max)
            self.character1.is_collidable = False
            game.item_list.remove(self)

    # 캐릭터와 충돌 시  바로 실행(player2)
    def use2(self, game, character2):
        self.character2 = character2 # player2 character
        if self.character2.is_collidable == True:
            self.sfx.play()
            fire_count = game.character2.fire_count + 1
            n_min = Default.character.value["missile"]["min"]
            n_max = Default.character.value["missile"]["max"]
            if fire_count > n_max:
                game.character2.auto_target = True
            game.character2.fire_count  = Utils.clamp(fire_count, n_min, n_max)
            self.character2.is_collidable = False
            game.item_list.remove(self)


class SpeedUp(Item):
    # 스피드업 아이템: 획득 시 캐릭터 이동/발사 속도 증가
    def __init__(self, animation):
        super().__init__(animation.frames, animation.frames_trans, "speedup")
        
    # 캐릭터와 충돌 시  바로 실행
    def use1(self, game, character1):
        self.character1 = character1 # player1 character
        if self.character1.is_collidable == True:
            self.sfx.play()
            self.used = time.time()
            self.org_velocity = game.character1.velocity
            self.org_fire_interval = game.character1.fire_interval
            game.character1.speed_up()
            self.character1.is_collidable = False
            game.item_list.remove(self)

    # 캐릭터와 충돌 시  바로 실행
    def use2(self, game, character2):
        self.character2 = character2 # player2 character
        if self.character2.is_collidable == True:
            self.sfx.play()
            self.used = time.time()
            self.org_velocity = game.character2.velocity
            self.org_fire_interval = game.character2.fire_interval
            game.character2.speed_up()
            self.character2.is_collidable = False
            game.item_list.remove(self)


