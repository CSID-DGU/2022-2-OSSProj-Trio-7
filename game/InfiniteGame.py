# Character : 이동속도, 투사체 속도, 크기, 이미지, 투사체 사운드
# stage : 목표점수, 배경이미지, 배경 사운드

# 게임 : 목숨, 시간
# 로직 : 세이브파일 변경 후 저장 필요

import random
import time
from collections import OrderedDict
from typing import Sized
from menu.LeaderBoardMenu import *
import pygame
import pygame_menu
from boss.Boss import Boss
from boss.Bullet import Bullet
from data.Animation import AnimationManager
from data.Defs import *
from data.StageDataManager import *
from object.Effect import *
from object.Item import *
from object.Mob import Mob
from pygame_menu.locals import ALIGN_CENTER
from pygame_menu.utils import make_surface
from data.database_user import *
from data.Defs import User

class InfiniteGame:

    def __init__(self, character, choosed_chracter, mode, mapimg, target1img, target2img, target3img, target4img, weapon):
        # 1. 게임초기화
        pygame.init()

        # 2. 게임창 옵션 설정
        infoObject = pygame.display.Info()
        title = "무한 모드"
        pygame.display.set_caption(title)  # 창의 제목 표시줄 옵션
        self.size = [infoObject.current_w, infoObject.current_h]
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.font_size = self.size[0] * 40 // 720
        self.scale = (self.size[0]*0.00015, self.size[1]*0.00015)

        # 3. 게임 내 필요한 설정
        self.clock = pygame.time.Clock()  # 이걸로 FPS설정함

        self.mode = mode  # Game mode = score/time
        self.choosed_chracter = choosed_chracter

        self.menu = pygame_menu.Menu('게임이 끝났습니다!', self.size[0], self.size[1],
                                     theme=pygame_menu.themes.THEME_DEFAULT)

        # 4. 게임에 필요한 객체들을 담을 배열 생성, 변수 초기화
        self.animation = AnimationManager()
        self.mobList = []
        self.item_list = []
        self.effect_list = []
        self.missileList = []
        self.character = character
        self.score = 0
        self.life = 3
        self.start_time = time.time()
        self.mob_gen_rate = 0.01
        self.target1_image = target1img
        self.target2_image = target2img
        self.target3_image = target3img
        self.target4_image = target4img
        self.background_image = mapimg
        from menu.ModeSelectMenu import soundset
        if(choosed_chracter == "police"):
            self.background_music = "./Sound/bgm/bgm_police.mp3"
        if(choosed_chracter == "firefighter"):
            self.background_music = "./Sound/bgm/bgm_firefighter.mp3"
        if(choosed_chracter == "doctor"):
            self.background_music = "./Sound/bgm/bgm_doctor.mp3"
        self.SB = 0
        self.dy = 2
        self.mob_velocity = 2
        self.coin = 0
        self.enemyBullets = []
        self.crashed_mob_count = 0  # 폭파시킨 몹 갯수

        # 5. 캐릭터 초기화
        self.character.reinitialize(self)

        # user
        self.database = Database()
        self.user = User.user_id

        # 일시정지 버튼
        self.changed_screen_size = self.screen.get_size()
        self.board_width = self.changed_screen_size[0]  # x
        self.board_height = self.changed_screen_size[1]  # y
        import button
        self.setting = button.button(self.board_height, self.board_height, 0.85, 0.05, 0.1, 0.085, "Image/thema/on.png")

        self.stop = button.button(self.board_width, self.board_height, 0.95, 0.05, 0.1, 0.1, "Image/thema/stop.png")
        self.sound = "on"

        self.plusgenerate = 0.0001 # FPS 단위마다 생성 범위 증가
        self.maxgenerate = 0.3 #최대 발생 확률

        # 무기 선택 옵션
        self.stagew=False
        self.infinitew=False
        self.defaultw=False
        self.wselect = weapon
        if weapon == "stage":
            self.stagew = True
        elif weapon == "infinite":
            self.infinitew = True
        else:
            self.defaultw = True


    def main(self):
        from menu.ModeSelectMenu import soundset
        # 메인 이벤트
        pygame.mixer.init()
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)

        # 현재 소리 on/off 상태
        if  Default.sound.value['sfx']['volume'] == 0.1:
            self.setting.image = "Image/thema/on.png"
            pygame.mixer.music.set_volume(0.1)
        else :
            pass

        if  Default.sound.value['sfx']['volume'] == 0:
            self.setting.image = "Image/thema/off.png"
            pygame.mixer.music.set_volume(0)
        else :
            pass
        
        background1_y = 0  # 배경 움직임을 위한 변수
        while self.SB == 0:
            # fps 제한을 위해 한 loop에 한번 반드시 호출해야합니다.
            self.clock.tick(30)

            # 화면 흰색으로 채우기
            self.screen.fill(Color.WHITE.value)
            # 배경 크기 변경 처리 및 그리기
            # 창크기가 바뀜에 따라 배경화면 크기 변경 필요

            background1 = pygame.image.load(self.background_image)
            background1 = pygame.transform.scale(background1, self.size)
            background_width = background1.get_width()
            background_height = background1.get_height()
            background2 = background1.copy()
            self.screen.blit(background1, (0, background1_y))
            self.screen.blit(background2, (0, 0), pygame.Rect(
                0, background_height - background1_y, background_width, background1_y))
            # 화면 사이즈 변경되면 버튼사이즈 바꿔줌.
            self.stop.change(self.screen.get_size()[
                             0], self.screen.get_size()[1])
            self.stop.draw(self.screen, (0, 0, 0))
            self.setting.change(self.screen.get_size()[
                             0], self.screen.get_size()[1])
            self.setting.draw(self.screen, (0, 0, 0))

            # 입력 처리
            for event in pygame.event.get():  # 동작을 했을때 행동을 받아오게됨
                if event.type == pygame.QUIT:
                    self.SB = 1  # SB 가 1이되면 while 문을 벗어나오게 됨
                if event.type == pygame.KEYDOWN:  # 어떤 키를 눌렀을때!(키보드가 눌렸을 때)
                    if event.key == pygame.K_x:
                        self.SB = 1
                    if event.key == pygame.K_z:  # 테스트용
                        self.score += 30
                        
                pos = pygame.mouse.get_pos()  # mouse

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.stop.isOver(pos):  # 마우스로 일시정지 버튼 클릭하면
                        self.StopGame()

                    if self.setting.isOver(pos):
                        if soundset == 0.1:
                            self.setting.image = "Image/thema/off.png"
                            soundset = 0
                            print(soundset)
                            Default.sound.value['sfx']['volume'] = 0
                            pygame.mixer.music.set_volume(0)
                        else:
                            self.setting.image = "Image/thema/on.png"
                            from menu.ModeSelectMenu import soundset
                            soundset = 0.1
                            print(soundset)
                            Default.sound.value['sfx']['volume'] = 0.1
                            pygame.mixer.music.set_volume(0.1)

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
                    self.check_resize()
                    self.animation.on_resize(self)

            # 몹/ 아이템을 확률적으로 발생시키기

            # 기본값 0.015
            if (random.random() < self.mob_gen_rate):
                if (self.mob_gen_rate < self.maxgenerate):
                    self.mob_gen_rate += self.plusgenerate
                # 게임 시작 후 일정 시간 지나면 새로운 attack target 등장
                if (time.time() - self.start_time > 270):
                    newMob = Mob(
                        self.target4_image, {"x": 50, "y": 50}, self.mob_velocity, 0)
                elif (time.time() - self.start_time > 180):
                    newMob = Mob(
                        self.target3_image, {"x": 50, "y": 50}, self.mob_velocity, 0)
                elif (time.time() - self.start_time > 90):
                    newMob = Mob(
                        self.target2_image, {"x": 50, "y": 50}, self.mob_velocity, 0)
                else:
                    newMob = Mob(
                        self.target1_image, {"x": 50, "y": 50}, self.mob_velocity, 0)
                # set mob location randomly
                newMob.set_XY((random.randrange(0, self.size[0]), 0))
                self.mobList.append(newMob)

            # 기본값 0.002
            if random.random() < Default.item.value["bomb"]["spawn_rate"]:
                if (Default.item.value["bomb"]["spawn_rate"] < self.maxgenerate):
                    Default.item.value["bomb"]["spawn_rate"] += self.plusgenerate
                new_item = Bomb(self.animation.animations["bomb"])
                new_item.set_XY(
                    (random.randrange(0, self.size[0]-new_item.sx), 0))
                self.item_list.append(new_item)

            # 기본값 0.002
            if random.random() < Default.item.value["health"]["spawn_rate"]:
                if (Default.item.value["health"]["spawn_rate"] < self.maxgenerate):
                    Default.item.value["health"]["spawn_rate"] += self.plusgenerate 
                new_item = Health(self.animation.animations["health"])
                new_item.set_XY(
                    (random.randrange(0, self.size[0]-new_item.sx), 0))
                self.item_list.append(new_item)

            # 100coin 기본값 0.003
            if random.random() < Default.item.value["100won"]["spawn_rate"]:
                if (Default.item.value["100won"]["spawn_rate"] < self.maxgenerate):
                    Default.item.value["100won"]["spawn_rate"] += self.plusgenerate 
                new_item = Coin(
                    self.animation.animations["Coin100WonAnim"], "100won")
                new_item.set_XY(
                    (random.randrange(0, self.size[0]-new_item.sx), 0))
                self.item_list.append(new_item)

            # 500coin 기본값 0.002
            if random.random() < Default.item.value["500won"]["spawn_rate"]:
                if (Default.item.value["500won"]["spawn_rate"] < self.maxgenerate):
                    Default.item.value["500won"]["spawn_rate"] += self.plusgenerate 
                new_item = Coin(
                    self.animation.animations["Coin500WonAnim"], "500won")
                new_item.set_XY(
                    (random.randrange(0, self.size[0]-new_item.sx), 0))
                self.item_list.append(new_item)

            # 1000coin 기본값 0.001
            if random.random() < Default.item.value["1000won"]["spawn_rate"]:
                if (Default.item.value["1000won"]["spawn_rate"] < self.maxgenerate):
                    Default.item.value["1000won"]["spawn_rate"] += self.plusgenerate 

                new_item = Coin(
                    self.animation.animations["Coin1000WonAnim"], "1000won")
                new_item.set_XY(
                    (random.randrange(0, self.size[0]-new_item.sx), 0))
                self.item_list.append(new_item)


            # 무기 구입 정보 적용하기
            if self.stagew==True:
                PowerUp(self)

            if self.infinitew==True:
                SpeedUp(self)

            # 플레이어 객체 이동
            self.character.update(self)

            # 몹 객체 이동
            for mob in self.mobList:
                mob.move(self.size, self)

            for item in self.item_list:
                item.move(self)

            for effect in self.effect_list:
                effect.move(self)

            # 적 투사체 이동
            for bullet in self.enemyBullets:
                bullet.move(self.size, self)
                bullet.show(self.screen)

            for item in list(self.item_list):
                if item.rect_collide(self.character.rect):
                    item.use(self)

            # 발사체와 몹 충돌 감지
            for missile in list(self.character.get_missiles_fired()):
                for mob in list(self.mobList):
                    if self.check_crash(missile, mob):
                        self.score += 10
                        self.crashed_mob_count += 1
                        if (self.crashed_mob_count >= 10):  # 몹 10마리 잡으면 궁극기 추가
                            self.character.gung_count += 1
                            self.crashed_mob_count = 0
                        if missile in self.character.missiles_fired:
                            self.character.missiles_fired.remove(missile)
                        mob.destroy(self)

            # 궁극기와 몹 충돌 감지
            for gung in list(self.character.get_gung_fired()):
                for mob in list(self.mobList):
                    if self.check_crash(gung, mob):
                        self.score += 10
                        self.crashed_mob_count += 1
                        mob.destroy(self)

            # 몹과 플레이어 충돌 감지
            for mob in list(self.mobList):
                if (self.check_crash(mob, self.character)):
                    if self.character.is_collidable == True:
                        self.character.last_crashed = time.time()
                        self.character.is_collidable = False
                        print("crash!")
                        self.life -= 1
                        mob.destroy(self)

            # 화면 그리기
            for effect in self.effect_list:
                effect.show(self.screen)
            # 플레이어 그리기
            self.character.show(self.screen)

            # 몹 그리기
            for mob in self.mobList:
                mob.show(self.screen)

            # 아이템 그리기
            for item in list(self.item_list):
                item.show(self.screen)

            # 발사된 미사일 그리기
            for i in self.character.get_missiles_fired():
                i.show(self.screen)
                if hasattr(i, "crosshair"):
                    if i.locked_on == True:
                        i.crosshair.show(self.screen)

            # 궁극기 사용시 그리기
            for gung in self.character.get_gung_fired():
                gung.show(self.screen)

            # 점수와 목숨 표시
            font = pygame.font.Font(Default.font.value, self.size[0]//40)
            score_life_text = font.render("점수 : {} 생명: {} 폭탄: {} 돈 : {} 궁극기 : {} ".format(
                self.score, self.life, self.character.bomb_count, self.coin, self.character.gung_count), True, Color.YELLOW.value) 
            self.screen.blit(score_life_text, (10, 5)) # x: 왼족에서 10 떨어짐 y : 위에서 5 떨어짐

            # 현재 흘러간 시간
            play_time = float(time.time() - self.start_time)
            time_text = font.render("시간 : {:.2f}".format(
                play_time), True, Color.YELLOW.value)
            self.screen.blit(time_text, (self.size[0]//2, 5)) # x: 화면정 중앙 y : 위에서 5 떨어짐

            # 화면갱신
            pygame.display.flip()  # 그려왔던데 화면에 업데이트가 됨

            # 목숨이 0 이하면 랭킹 등록 화면
            if (self.life < 1):
                self.register_ranking()
                self.show_ranking_register_screen()
                return

        # While 빠져나오면 랭킹등록 스크린 실행
        self.register_ranking()
        self.show_ranking_register_screen()

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

    # 홈버튼 클릭 시
    def Home(self, menu):
        menu.disable()
        pygame.mixer.music.stop()

    def show_ranking_register_screen(self):
        play_time = time.time() - self.start_time
        pygame.mixer.music.stop()
        gameover_image = pygame_menu.baseimage.BaseImage(
            image_path=Images.gameover.value, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)  # 메뉴 이미지, Images는 Defs.py에 선언되어 있는 클래스명
        self.mytheme = pygame_menu.Theme(
            widget_font=Default.font.value,
            widget_background_color=Color.NAVY.value,  # 버튼 배경색 설정
            title_font=Default.font.value,
            selection_color=Color.ORANGE.value,  # 선택됐을때 글씨색 설정
            widget_font_color=Color.WHITE.value,  # 기본 글자색
            title_background_color=Color.TRANSPARENT.value, # 투명
            title_font_color=Color.TRANSPARENT.value, # 투명
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY,
            widget_font_size=self.size[0] * 45 // 720
        )
        self.mytheme.background_color = gameover_image

        self.menu = pygame_menu.Menu('', self.size[0], self.size[1],
                                     theme=self.mytheme)
        self.menu.add.label("점수 : {}".format(
            self.score), font_size=self.font_size)
        self.menu.add.vertical_margin(10)
        self.menu.add.label("시간 : {:.2f}".format(
            play_time), font_size=self.font_size)
        self.menu.add.vertical_margin(30)
        self.menu.add.button(
            '   랭킹   ', self.show_register_result, font_size=self.font_size)
        self.menu.add.vertical_margin(10)
        self.menu.add.button( '다시 시작 ', self.retry, font_size=self.font_size)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('모드 선택화면으로', self.ModeSelectMenu,
                             font_size=self.font_size)
        print(User.coin)
        print(self.coin)
        User.coin = User.coin + self.coin
        print(User.coin)
        self.database = Database()
        self.database.set_coin()
        self.menu.mainloop(self.screen)
        pygame.display.flip()

    def register_ranking(self):  # 랭크 기록
        current_score = self.score  # 현재 게임 기록
        play_time = time.time() - self.start_time
        current_time = play_time
        print(self.user)
        print(current_score)
        if (isinstance(self.mode, InfiniteGame.ScoreMode)):  # score mode
            # 기록 없는 경우
            if self.database.rank_not_score_exists(self.user, "score") is True:
                self.database.update_score2("score", current_score)  # 기록추가
                print("enter")
            else:
                if (self.database.high_score("score") <= current_score):  # 데이터 베이스에 저장되어 있는 점수 비교 후 등록
                    self.database.update_score(
                        'score', current_score)  # 새로운 점수가 더 높으면 기록
        elif (isinstance(self.mode, InfiniteGame.TimeMode)):
            # 기록 없는 경우
            if self.database.rank_not_time_exists(self.user, "time") is True:
                self.database.update_time2("time", current_time)
            else:
                if (self.database.high_time("time") <= current_time):  # 데이터 베이스에 저장되어 있는 점수 비교 후 등록
                    self.database.update_time('time', current_time)

    # 랭킹 등록 결과 화면

    def show_register_result(self):
        LeaderBoardMenu(self.screen).rank()

    def ModeSelectMenu(self):
        import menu.ModeSelectMenu
        game = menu.ModeSelectMenu.ModeSelectMenu(self.screen)

        while True:
            game.show(self.screen, self.choosed_chracter)
            pygame.display.flip()

    # Continue 클릭 시
    def Continue(self, menu):
        menu.disable()
        pygame.mixer.music.unpause()

    # 일시정지 화면
    def StopGame(self):
        pygame.mixer.music.pause()
        self.orange_color = (253, 111, 34)
        self.font_size = self.size[0] * 38 // 720  # 글씨크기

        self.mytheme = pygame_menu.Theme(
            widget_font=Default.font.value,
            widget_background_color=Color.INDIGO.value,  # 버튼 배경색 설정
            title_font=Default.font.value,
            selection_color=Color.ORANGE.value,  # 선택됐을때 글씨색 설정
            widget_font_color=Color.WHITE.value,  # 기본 글자색
            title_background_color=Color.TRANSPARENT.value,
            title_font_color=Color.TRANSPARENT.value,
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY,
            widget_font_size=self.size[0] * 45 // 720
        )

        main_image = pygame_menu.baseimage.BaseImage(
            image_path=Images.stop.value, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)  # 메뉴 이미지, Images는 Defs.py에 선언되어 있는 클래스명

        self.mytheme.background_color = main_image

        self.menu = pygame_menu.Menu(
            '', self.size[0], self.size[1], theme=self.mytheme)  # 상단바

        self.stop_page()
        self.menu.mainloop(self.screen, bgfun=self.check_resize)

    def stop_page(self):
        self.menu.clear()
        b1 = self.menu.add.button('   계속하기   ', self.Continue, 
                             self.menu, selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.vertical_margin(10)
        b2 = self.menu.add.button("   다시시작   ", self.retry,selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.vertical_margin(10)
        b3 = self.menu.add.button("모드 선택화면으로", self.ModeSelectMenu, selection_color=self.orange_color,
                             font_size=self.font_size,)

    def check_resize_end(self):
        if self.check_resize():
            self.menu.disable()
            self.show_ranking_register_screen()

    # 화면 크기 조정 감지 및 비율 고정
    def check_resize(self):
        if (self.size != self.screen.get_size()):  # 현재 사이즈와 저장된 사이즈 비교 후 다르면 변경
            changed_screen_size = self.screen.get_size()  # 변경된 사이즈
            ratio_screen_size = (
                changed_screen_size[0], changed_screen_size[0]*783/720)  # y를 x에 비례적으로 계산
            if (ratio_screen_size[0] < 300):  # 최소 x길이 제한
                ratio_screen_size = (300, 390)
            if (ratio_screen_size[1] > 700):  # 최대 y길이 제한
                ratio_screen_size = (700, 910)
            self.screen = pygame.display.set_mode(ratio_screen_size,
                                                  pygame.RESIZABLE)
            window_size = self.screen.get_size()
            new_w, new_h = 1 * window_size[0], 1 * window_size[1]
            self.menu.resize(new_w, new_h)
            self.size = window_size
            self.menu._current._widgets_surface = make_surface(0, 0)
            print(f'New menu size: {self.menu.get_size()}')
            print(self.screen)
            font_size = new_w * 40 // 720
            self.font_size = font_size
            self.scale = (new_w*0.00015, new_h*0.00015)
            return True

    # 재시도 버튼 클릭 시 실행
    def retry(self):
        InfiniteGame(self.character, self.choosed_chracter, self.mode,
                     self.background_image,self.target1_image,self.target2_image,self.target3_image,self.target4_image, self.wselect).main()
        self.menu.disable()

    # 난이도를 나누는 모드 클래스 (상속하여 사용)
    class Mode:
        def update_difficulty():
            pass

    class ScoreMode(Mode):  # 스코어 모드
        @staticmethod
        def update_difficulty(game):
            play_time = float(time.time() - game.start_time)  # 게임 진행 시간
            if (game.mob_gen_rate < 0.215):  # 최대값 제한
                # 10초마다 mob_gen_rate 0.1 증가(기본 0.015)
                game.mob_gen_rate = play_time//10/10 + 0.015
            if (game.dy < 20):  # 최대값 제한
                game.dy = play_time//5*2 + 2  # 5초마다 dy(배경 이동 속도) 2 증가 (기본 2)
            if (game.mob_velocity < 3):  # 최대값 제한
                # 10초마다 mob_velocity(몹 이동 속도) 1 증가 (기본 2)
                game.mob_velocity = play_time//10*1 + 2

    class TimeMode(Mode):  # time 모드
        @staticmethod
        def update_difficulty(game):
            play_time = float(time.time() - game.start_time)  # 게임 진행 시간
            if (game.mob_gen_rate < 0.215):  # 최대값 제한
                # 10초마다 mob_gen_rate 0.1 증가(기본 0.015)
                game.mob_gen_rate = play_time//10/10 + 0.015
            if (game.dy < 20):  # 최대값 제한
                game.dy = play_time//5*2 + 2  # 5초마다 dy(배경 이동 속도) 2 증가 (기본 2)
            if (game.mob_velocity < 3):  # 최대값 제한
                # 10초마다 mob_velocity(몹 이동 속도) 2 증가 (기본 2)
                game.mob_velocity = play_time//10*1 + 2
