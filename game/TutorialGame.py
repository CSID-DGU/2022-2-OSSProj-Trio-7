import pygame
import pygame_menu
import sys
import random
from pygame.locals import *
import time
from data.Animation import AnimationManager

import random
import time
from collections import OrderedDict
from typing import Sized
from data.Animation import AnimationManager
from data.CharacterDataManager import *
from data.Defs import *
from data.StageDataManager import *
from object.Item import *
#from object.Mob import Mob
from pygame_menu.utils import make_surface
from data.Defs import User

from pygame.math import Vector2  # mob.py에서 가져옴
from object.Effect import Boom
from object.Object import Object
from button import *

from object.Character import *
import time
from Main import Login


class tutorial:

    def __init__(self, character_data, character1, stage):

        # 1. 게임초기화
        pygame.init()
        self.stage_cleared = False

        # 2. 게임창 옵션 설정
        infoObject = pygame.display.Info()
        title = "PVP game"
        pygame.display.set_caption(title)  # 창의 제목 표시줄 옵션
        self.size = [infoObject.current_w, infoObject.current_h]
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.scale = (self.size[0]*0.00015, self.size[1]*0.00015)
        self.font_size = self.size[0] * 40 // 720

        # 3. 게임 내 필요한 설정
        self.clock = pygame.time.Clock()  # 이걸로 FPS설정함

        # 4. 게임에 필요한 객체들을 담을 배열 생성, 변수 초기화, pvp
        self.animation = AnimationManager()
        self.mobList = []
        self.item_list = []
        self.effect_list = []
        self.enemyBullets = []
        self.character_data = character_data

        self.goal_time = 120  # play 120초
        self.character1 = character1  # player1 character

        self.score = 0  # player1 score
        # self.gung = 0
        # self.bomb = 0
        self.life_player1 = 3  # player1 life

        self.startTime = time.time()
        self.mob_gen_rate = 0.01
        self.mob_velocity = 2
        self.mob_image = "./Image/policeCharacters/policeStage_monster.png"
        #self.background_image = stage.background_image
        self.background_image = "Image/background/police_background.png"
        self.gameover_image1 = "Image/catthema/win1_.png"
        self.gameover_image2 = "Image/catthema/win2_.png"
        self.gameover_image3 = "Image/catthema/same.png"
        self.background_music = "./Sound/bgm/bgm_police.mp3"
        self.k = 0
        self.SB = 0
        #self.infowindow_image = "Image/catthema/map1.png"

        # 5. 캐릭터 초기화
        self.character1.pvp_reinitialize1(self)

        # 방향키

        self.direction1 = {None: (0, 0), pygame.K_UP: (0, -2), pygame.K_DOWN: (0, 2),
                           pygame.K_LEFT: (-2, 0), pygame.K_RIGHT: (2, 0)}
        mytheme = pygame_menu.themes.THEME_ORANGE.copy()
        self.menu = pygame_menu.Menu('PVP.', self.size[0], self.size[1],
                                     theme=mytheme)

        # 일시정지 버튼
        self.changed_screen_size = self.screen.get_size()
        self.board_width = self.changed_screen_size[0]  # x
        self.board_height = self.changed_screen_size[1]  # y

        import button
        self.gotohome = button.button(
            self.board_width, self.board_height, 0.9, 0.05, 0.2, 0.1, "Image/thema/gotohome.png")

    def main(self, screen):
        # 메인 이벤트
        pygame.mixer.init()
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

        pygame.display.flip()  # 그려왔던데 화면에 업데이트가 됨

        # 텍스트 렌더링 여부
        box_render = False  # 메시지 박스 여부
        mission = False  # 미션 클리어 여부
        index = -1

        # 튜토리얼 초기화
        self.texts1 = [
            '튜토리얼을 시작하겠습니다. 캐릭터를 방향키를 눌러 움직여보세요.',
            '잘하셨습니다. 이제 스페이스바를 눌러 공격해 보세요.',
            '훌륭합니다. 이제 a키를 눌러 폭탄을 작동시켜 보세요.',
            '잘하셨습니다. s키를 눌러 궁극기를 사용하세요.',
            '훌륭합니다. 튜토리얼은 모두 완료하였습니다. 이제 게임을 플레이해보세요'
        ]
        self.test_sound = pygame.mixer.Sound("./Sound/message.wav")
        font = pygame.font.SysFont("malgungothic", 15)
        text_renders = [font.render(text, True, (255, 255, 255))
                        for text in self.texts1]
        text_box = pygame.Rect(
            0, self.size[1]*0.8, self.size[0], self.size[1]/3)
        # print(index)

        while self.SB == 0:
            # fps 제한을 위해 한 loop에 한번 반드시 호출해야합니다.
            self.clock.tick(30)

            # 화면 흰색으로 채우기
            self.screen.fill(Color.WHITE.value)

            # pvp 모드를 위한 배경 분리
            background1 = pygame.image.load(self.background_image)

            background1 = pygame.transform.scale(
                background1, (self.size[0], self.size[1]))  # 왼쪽
            # background2 = pygame.transform.scale(
            # background2, (self.size[0]/2, self.size[1])) # 오른쪽
            background1_width = background1.get_width()
            background1_height = background1.get_height()

            background1_copy = background1.copy()

            self.screen.blit(background1,  [0, 0])
            self.screen.blit(background1, [self.size[0], 0])

            # 화면 사이즈 변경되면 버튼사이즈 바꿔줌.
            self.gotohome.change(self.screen.get_size()[
                0], self.screen.get_size()[1])
            self.gotohome.draw(self.screen, (0, 0, 0))

            start_ticks = pygame.time.get_ticks()

            # 입력 처리
            for event in pygame.event.get():  # 동작을 했을때 행동을 받아오게됨
                if event.type == pygame.QUIT:
                    self.SB = 1  # SB 가 1이되면 while 문을 벗어나오게 됨
                '''if event.type == pygame.KEYDOWN: # 어떤 키를 눌렀을때!(키보드가 눌렸을 때)
                    if event.key == pygame.K_x:
                        self.SB=1
                    if event.key == pygame.K_z: #테스트용
                        self.score += 30'''
                if event.type == pygame.VIDEORESIZE:  # 창크기가 변경되었을 때
                    # 화면 크기가 최소 300x390은 될 수 있도록, 변경된 크기가 그것보다 작으면 300x390으로 바꿔준다
                    width, height = max(event.w, 300), max(event.h, 390)

                    # 크기를 조절해도 화면의 비율이 유지되도록, 가로와 세로 중 작은 것을 기준으로 종횡비(10:13)으로 계산
                    if (width <= height):
                        height = int(width * (13/10))
                    else:
                        width = int(height * (10/13))

                    self.size = [width, height]  # 게임의 size 속성 변경
                    self.screen = pygame.display.set_mode(
                        self.size, pygame.RESIZABLE)  # 창 크기 세팅
                    # self.check_resize(screen)
                    # self.animation.on_resize(self)
                    text_box = pygame.Rect(
                        0, self.size[1]*0.8, self.size[0], self.size[1]/3)
                    if box_render:
                        self.screen.blit(
                            text_renders[index], (40, self.size[1]*0.85))

                pos = pygame.mouse.get_pos()  # mouse
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.gotohome.isOver(pos):  # 마우스로  버튼 클릭하면
                        print("home 화면으로 돌아가기")
                        Login(self.screen)

            # 몹을 확률적으로 발생시키기 -> 몹 하나가 화면에 가만히 있도록
            if (random.random() < self.mob_gen_rate):
                newMob = Mob(self.mob_image, {
                             "x": 50, "y": 50}, self.mob_velocity, 0)
                # set mob location randomly

                newMob.set_XY((self.size[0]//2, 0))
                self.mobList.append(newMob)

            # 몹 객체 이동
            # for mob in self.mobList:
            #     mob.move(self.size, self)

            for item in self.item_list:
                item.move(self)

            for effect in self.effect_list:
                effect.move(self)

            # 튜토리얼 초기화

            keys = pygame.key.get_pressed()

            # if index == len(text_renders)-1:
            #     print("튜토리얼이 종료됩니다.")
            #     time.sleep(2)
            #     return

            if index == -1 and keys[pygame.K_RETURN]:
                box_render = True  # 텍스트 박스 렌더링
                index += 1
                print(index)
                print(box_render)

            if (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]) and index == 0:  # 방향키 미션일 경우
                self.test_sound.play()
                box_render = True
                index += 1
                print("첫 번째 미션 클리어!")

            if keys[pygame.K_SPACE] and index == 1:
                self.test_sound.play()
                index += 1
                box_render = True
                print("두 번째 미션 클리어!")
                # 폭탄 개수 +=1
                self.character1.bomb_count += 1

            if keys[pygame.K_a] and index == 2:
                self.test_sound.play()
                index += 1
                box_render = True
                print("세 번쨰 미션 클리어!")
                # 궁극기 개수 +=1
                self.character1.gung_count += 1

            if keys[pygame.K_s] and index == 3:
                self.test_sound.play()
                index += 1
                box_render = True
                print("마지막 미션 클리어!")

            if box_render == True:  # 박스 렌더링이 true일 경우 화면에 텍스트 박스를 그림
                pygame.draw.rect(self.screen, (0, 0, 0, 0), text_box, 0)
                self.screen.blit(
                    text_renders[index], (self.size[0]*0.02, self.size[1]*0.85))
                if index == len(text_renders)-1 and keys[pygame.K_RETURN]:
                    print("튜토리얼이 종료됩니다.")
                    time.sleep(2)
                    return

            if box_render == False:
                pygame.init()  # 화면을 초기화 해버림

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            # print("update")
            # pygame.display.update() # 업데이트를 시킬 위치를 지정해야 함

            # 발사체와 몹 충돌 감지(player1)
            for missile in list(self.character1.get_missiles_fired()):
                for mob in list(self.mobList):
                    if self.check_crash(missile, mob):
                        self.score += 10
                        if missile in self.character1.missiles_fired:
                            self.character1.missiles_fired.remove(missile)
                        mob.destroy(self)

            # 궁극기와 몹 충돌 감지
            for gung in list(self.character1.get_gung_fired()):
                for mob in list(self.mobList):
                    if self.check_crash(gung, mob):
                        self.score += 10
                        mob.destroy(self)

            # 화면 그리기
            for effect in self.effect_list:
                effect.show(self.screen)

            # 캐릭터 그리기
            self.character1.show(self.screen)
            # self.character2.show(self.screen)

            # 몹 그리기
            for mob in self.mobList:
                mob.show(self.screen)

            for item in list(self.item_list):
                item.show(self.screen)

            for i in self.character1.get_missiles_fired():
                i.show(self.screen)
                if hasattr(i, "crosshair"):
                    if i.locked_on == True:
                        i.crosshair.show(self.screen)

            # 궁극기 사용시 그리기
            for gung in self.character1.get_gung_fired():
                gung.show(self.screen)

            # 점수와 목숨, 타이머 표시
            font = pygame.font.Font(Default.font.value, self.size[0]//40)
            play_time = time.gmtime(time.time() - self.startTime)
            timer = self.goal_time - play_time.tm_sec
            time_score_life_text1 = font.render("궁극기 : {} 생명: {} 폭탄: {}".format(
                self.character1.gung_count, self.life_player1, self.character1.bomb_count), True, Color.YELLOW.value)  # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔

            # 이미지화 한 텍스트라 이미지를 보여준다고 생각하면 됨
            self.screen.blit(time_score_life_text1, (10, 15))

            # 목숨이 0 이하면 게임 종료 화면 => 튜토리얼이 끝나면 종료 화면
            if (self.life_player1 < 1):
                pygame.mixer.music.stop()
                pygame.mixer.Sound(Default.item.value["sound"]).stop()
                pygame.mixer.Sound(
                    Default.effect.value["boom"]["sound"]).stop()
                self.win1 = pygame.image.load(self.gameover_image2)
                self.win1 = pygame.transform.scale(
                    self.win1, (self.size[0], self.size[1]))
                self.screen.fill(Color.BLACK.value)
                self.screen.blit(self.win1,  [0, 0])
            # print("update")
            # pygame.display.update()

            self.character1.pvp_update1(self)

            pygame.display.flip()

        pygame.mixer.music.stop()
        print("update")
        # pygame.display.update()

# 충돌 감지 함수
    def check_crash(self, o1, o2):
        o1_mask = pygame.mask.from_surface(o1.img)
        o2_mask = pygame.mask.from_surface(o2.img)

        offset = (int(o2.x - o1.x), int(o2.y - o1.y))
        collision = o1_mask.overlap(o2_mask, offset)

        if collision:
            return True
        else:
            return False

    def tutorial_info(self):
        self.check_resize(self.screen)
        self.infotutorial_img = "./Image/tutorial_help.png"  # 이미지 수정필요
        self.menu.add.image(self.infotutorial_img, scale=Scales.default.value)
        infowindow = pygame.image.load(self.infotutorial_img)
        infowindow = pygame.transform.scale(infowindow, self.size)
        self.screen.blit(infowindow, [0, 0])
        pygame.display.flip()
        time.sleep(3)  # 3초뒤에 게임 시작.
        self.main(self.screen)

    # 화면 크기 조정 감지 및 비율 고정
    def check_resize(self, screen):
        if (self.size != screen.get_size()):  # 현재 사이즈와 저장된 사이즈 비교 후 다르면 변경
            changed_screen_size = self.screen.get_size()  # 변경된 사이즈
            ratio_screen_size = (
                changed_screen_size[0], changed_screen_size[0]*783/720)  # y를 x에 비례적으로 계산
            if (ratio_screen_size[0] < 320):  # 최소 x길이 제한
                ratio_screen_size = (494, 537)
            if (ratio_screen_size[1] > 783):  # 최대 y길이 제한
                ratio_screen_size = (720, 783)
            screen = pygame.display.set_mode(ratio_screen_size,
                                             pygame.RESIZABLE)


class Mob(Object):
    def __init__(self, img_path, size, velocity, missile):
        super().__init__(img_path, size, velocity)
        self.x_inv = random.choice([True, False])  # 추가
        self.y_inv = False  # 추가
        self.missile = missile
        self.is_targeted = False
        self.direction = Vector2(1, 1)
        self.rad = 1
        self.kill_sfx = pygame.mixer.Sound(
            Default.effect.value["boom"]["sound"])
        self.kill_sfx.set_volume(Default.sound.value["sfx"]["volume"])

    def move(self, boundary, game):
        # update when screen resized
        if (game.size[0] != self.boundary[0]) or (game.size[1] != self.boundary[1]):
            self.on_resize(game)
        self.x += self.direction.y
        self.y += self.direction.x
        self.rad += 0.04*self.velocity  # 속도에 적절한 값을 곱하여, 각도 변경
        # self.direction.from_polar((self.velocity*3,math.cos(self.rad)*70)) #속도에 비례한 길이를 갖고, 방향 sin함수를 따르는 벡터를 다음 방향으로 지정
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
        elif self.x >= self.boundary[0]/2 - self.sx and self.x <= self.boundary[0]/2:
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
        mob_location = {"x": self.x+(self.sx/2), "y": self.y+(self.sy/2)}
        boom.set_XY((mob_location["x"] - boom.sx/2,
                    mob_location["y"] - boom.sy/2))
        game.effect_list.append(boom)
        if self in game.mobList:
            game.mobList.remove(self)
