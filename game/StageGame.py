# Character : 이동속도, 투사체 속도, 크기, 이미지, 투사체 사운드
# stage : 목표점수, 배경이미지, 배경 사운드

# 게임 : 목숨, 시간
# 로직 : 세이브파일 변경 후 저장 필요

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
from object.Mob import Mob
from pygame_menu.utils import make_surface
from data.Defs import User
from data.database_user import *
from data.Stage import Stage
import time
from data.StoryManager import *


class StageGame:
    # 캐릭터데이터, 캐릭터, 스테이지 정보, 맵 정보, 구매한 무기
    def __init__(self, character_data, character, stage, map_info, weapon):
        # 1. 게임초기화
        pygame.init()
        self.stage_cleared = False

        # 2. 게임창 옵션 설정
        infoObject = pygame.display.Info()
        title = "스테이지 모드"
        pygame.display.set_caption(title)  # 창의 제목 표시줄 옵션
        self.size = [infoObject.current_w, infoObject.current_h]
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.font_size = self.size[0] * 40 // 720
        self.scale = (self.size[0]*0.0020, self.size[1]*0.0020)
        mytheme = pygame_menu.themes.THEME_ORANGE.copy()
        self.menu = pygame_menu.Menu('Select Stage...', self.size[0], self.size[1],
                                     theme=mytheme)

        # 3. 게임 내 필요한 설정
        self.clock = pygame.time.Clock()  # 이걸로 FPS설정함

        # 4. 게임에 필요한 객체들을 담을 배열 생성, 변수 초기화
        self.animation = AnimationManager()
        self.mobList = []
        self.item_list = []
        self.effect_list = []
        self.character_data = character_data
        self.character = character
        self.stage = stage
        self.goal_score = stage.goal_score
        self.score = 0
        self.life = 3
        self.startTime = time.time()
        self.mob_gen_rate = 0.01
        self.mob_image = stage.mob_image
        self.background_image = stage.background_image
        self.background_music = stage.background_music
        self.k = 0
        self.SB = 0
        self.coin = 0
        self.infowindow_image = "Image/stageMode_background.png".format(
            self.stage.chapter)
        self.soundvol = 0.1
        self.stage_data = StageDataManager.loadStageData()  # 스테이지 데이터
        self.temp = 0

        self.storyInfo = map_info  # 스토리라인 조건문에 사용될 변수 받아옴

        # 일시정지 버튼
        self.changed_screen_size = self.screen.get_size()
        self.board_width = self.changed_screen_size[0]  # x
        self.board_height = self.changed_screen_size[1]  # y
        import button
        self.setting = button.button(self.board_height, self.board_height, 0.85, 0.05, 0.1, 0.085, "Image/thema/on.png")
        self.stop = button.button(
            self.board_width, self.board_height, 0.95, 0.05, 0.1, 0.1, "Image/thema/stop.png")

        # 4-1. 보스 스테이지를 위한 변수 초기화
        self.is_boss_stage = stage.is_boss_stage
        if self.is_boss_stage:
            self.boss = Boss(self.size, stage.boss_image,
                             stage.boss_bullet_image)
        self.enemyBullets = []

        # 5. 캐릭터 초기화
        self.character.reinitialize(self)

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

    def main_info(self):
        self.check_resize()
        self.menu.add.image(self.infowindow_image, scale=Scales.default.value)
        infowindow = pygame.image.load(self.infowindow_image)
        infowindow = pygame.transform.scale(infowindow, self.size)

        self.screen.blit(infowindow, [0, 0])
        font = pygame.font.Font(Default.font.value, self.size[0]//25)
        info_stage_test = font.render(" [{} 단계 ]".format(
            self.stage.stage), True, Color.BLACK.value)
        info_score_text = font.render("목표점수 {}를 도달하면 보스가 등장합니다!".format(
            self.goal_score), True, Color.BLACK.value)
        info_boss_text = font.render("목표점수를 달성해 보스를 잡아보세요!".format(
            self.goal_score), True, Color.BLACK.value)
        info_start_text = font.render("로딩이 끝난 후 SPACE키를 눌러 시작하세요".format(
            self.goal_score), True, Color.BLACK.value)
        self.screen.blit(
            info_stage_test, (self.size[0]*0.45, self.size[1]*0.35))
        self.screen.blit(
            info_score_text, (self.size[0]*0.15, self.size[1]*0.45))
        self.screen.blit(
            info_boss_text, (self.size[0]*0.2, self.size[1]*0.55))
        self.screen.blit(
            info_start_text, (self.size[0]*0.15, self.size[1]*0.65))
        pygame.display.flip()
        time.sleep(3)  # 3초뒤에 스토리라인 전개.

        self.size = StoryManager(self.storyInfo).get_currentSize()

        self.main()

    def main(self):

        from menu.GameSelectMenu import soundset
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
                pos = pygame.mouse.get_pos()  # mouse
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.stop.isOver(pos):  # 마우스로 일시정지 버튼 클릭하면
                        self.StopGame()

                    if self.setting.isOver(pos):
                        if soundset == 0.1:
                            self.setting.image = "Image/thema/off.png"
                            soundset = 0
                            Default.sound.value['sfx']['volume'] = 0
                            pygame.mixer.music.set_volume(0)
                        else:
                            self.setting.image = "Image/thema/on.png"
                            from menu.GameSelectMenu import soundset
                            soundset = 0.1
                            Default.sound.value['sfx']['volume'] = 0.1
                            pygame.mixer.music.set_volume(0.1)

                if event.type == pygame.VIDEORESIZE:  # 화면이 리사이즈 되면
                    # 화면 크기가 최소 300x390은 될 수 있도록, 변경된 크기가 그것보다 작으면 300x390으로 바꿔준다
                    width, height = max(event.w, 300), max(event.h, 390)

                    # 크기를 조절해도 화면의 비율이 유지되도록, 가로와 세로 중 작은 것을 기준으로 종횡비(10:13)으로 계산
                    if (width <= height):
                        height = int(width * (13/10))
                    else:
                        width = int(height * (10/13))

                    w_ratio = width/self.size[0]
                    h_ratio = height/self.size[1]

                    self.size = [width, height]  # 게임의 size 속성 변경
                    self.screen = pygame.display.set_mode(
                        self.size, pygame.RESIZABLE)  # 창 크기 세팅
                    self.check_resize()

                    if (self.is_boss_stage):  # 보스 스테이지라면 보스 리사이징
                        self.boss.on_resize(self)
                    self.animation.on_resize(self)

            # 몹을 확률적으로 발생시키기

            if (random.random() < self.mob_gen_rate):
                newMob = Mob(self.mob_image, {"x": 50, "y": 50}, 2, 0)
                newMob.set_XY((random.randrange(0, self.size[0]), 0))
                self.mobList.append(newMob)


            if random.random() < Default.item.value["bomb"]["spawn_rate"]:
                if (Default.item.value["bomb"]["spawn_rate"] < 0.3):
                    Default.item.value["bomb"]["spawn_rate"] += 0.0001
                new_item = Bomb(self.animation.animations["bomb"])
                new_item.set_XY(
                    (random.randrange(0, self.size[0]-new_item.sx), 0))
                self.item_list.append(new_item)

            # 기본값 0.002
            if random.random() < Default.item.value["health"]["spawn_rate"]:
                if (Default.item.value["health"]["spawn_rate"] < 0.3):
                    Default.item.value["health"]["spawn_rate"] += 0.0001
                new_item = Health(self.animation.animations["health"])
                new_item.set_XY(
                    (random.randrange(0, self.size[0]-new_item.sx), 0))
                self.item_list.append(new_item)

            # 100coin 기본값 0.002
            if random.random() < Default.item.value["100won"]["spawn_rate"]:
                if (Default.item.value["100won"]["spawn_rate"] < 0.3):
                    Default.item.value["100won"]["spawn_rate"] += 0.0001
                new_item = Coin(
                    self.animation.animations["Coin100WonAnim"], "100won")
                new_item.set_XY(
                    (random.randrange(0, self.size[0]-new_item.sx), 0))
                self.item_list.append(new_item)


            # 500coin 기본값 0.001
            if random.random() < Default.item.value["500won"]["spawn_rate"]:
                if (Default.item.value["500won"]["spawn_rate"] < 0.3):
                    Default.item.value["500won"]["spawn_rate"] += 0.0001
                new_item = Coin(
                    self.animation.animations["Coin500WonAnim"], "500won")
                new_item.set_XY(
                    (random.randrange(0, self.size[0]-new_item.sx), 0))
                self.item_list.append(new_item)

            # 1000coin 기본값 0.0005
            if random.random() < Default.item.value["1000won"]["spawn_rate"]:
                if (Default.item.value["1000won"]["spawn_rate"] < 0.3):
                    Default.item.value["1000won"]["spawn_rate"] += 0.0001
                new_item = Coin(
                    self.animation.animations["Coin1000WonAnim"], "1000won")
                new_item.set_XY(
                    (random.randrange(0, self.size[0]-new_item.sx), 0))
                self.item_list.append(new_item)



            # # 무기 구매 적용 
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

            # 보스 이동
            # 보스 업데이트
            if (self.score >= self.goal_score or self.stage_cleared):
                if (self.is_boss_stage):
                    self.boss.draw(self.screen)
                    self.boss.update(self.enemyBullets,
                                     self.character, self.size)
                    self.boss.check(self.character, self)

                    # 보스와 플레이어 충돌 감지
                    if (self.check_crash(self.boss, self.character)):
                        if self.character.is_collidable == True:
                            self.character.last_crashed = time.time()
                            self.character.is_collidable = False
                            self.life -= 1

                    # 보스의 총알과 플레이어 충돌 감지
                    for bullet in self.enemyBullets:
                        if (bullet.check_crash(self.character)):
                            if self.character.is_collidable == True:
                                self.character.last_crashed = time.time()
                                self.character.is_collidable = False
                                self.life -= 1
                                self.enemyBullets.remove(bullet)

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
                        if missile in self.character.missiles_fired:
                            self.character.missiles_fired.remove(missile)
                        mob.destroy(self)

            # 몹과 플레이어 충돌 감지
            for mob in list(self.mobList):
                if (self.check_crash(mob, self.character)):
                    if self.character.is_collidable == True:
                        self.character.last_crashed = time.time()
                        self.character.is_collidable = False
                        self.life -= 1
                        mob.destroy(self)

            # 화면 그리기
            # 효과 그리기(폭탄 아이템)
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
            # 플레이어 발사체 그리기
            for i in self.character.get_missiles_fired():
                i.show(self.screen)
                if hasattr(i, "crosshair"):
                    if i.locked_on == True:
                        i.crosshair.show(self.screen)

            # 점수와 목숨 표시
            font = pygame.font.Font(Default.font.value, self.size[0]//40)
            score_life_text = font.render("점수 : {} 생명: {} 폭탄: {} 돈 : {}".format(
                self.score, self.life, self.character.bomb_count, self.coin), True, Color.YELLOW.value)  # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔
            # 이미지화 한 텍스트라 이미지를 보여준다고 생각하면 됨
            self.screen.blit(score_life_text, (10, 5))


            # 화면갱신
            pygame.display.flip()  

            # 보스를 처치하면 스테이지 클리어 화면
            if (self.stage_cleared):
                StageDataManager.unlockNextStage(self.stage)
                self.showStageClearScreen()
                return

            # 목숨이 0 이하면 게임 오버 화면
            if (self.life < 1):
                self.showGameOverScreen()
                return

        # While 빠져나오면 게임오버 스크린 실행
        self.showGameOverScreen()

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

    def toMenu(self, menu):
        menu.disable()
        pygame.mixer.music.play(-1)

    # 재시도 버튼 클릭 시
    def retry(self):
        StageGame(self, self.character, self.stage, self.storyInfo, self.wselect).main() # storyInfo는 맵 정보
        self.menu.disable()

    # 홈버튼 클릭 시
    def Home(self, menu):
        pygame.mixer.music.stop()
        menu.disable()

    # Continue 클릭 시

    def Continue(self, menu):
        menu.disable()
        pygame.mixer.music.unpause()

    def gameselectmenu(self):
        import menu.GameSelectMenu
        game = menu.GameSelectMenu.GameSelectMenu(self.screen)

        while True:
            game.show(self.screen, self.storyInfo)
            pygame.display.flip()

    # next stage 버튼 클릭 시
    def nextstage(self):

        chapterlist = [['police', "gloomy street"], [
            'firefighter', "burning house"], ['doctor', "hospital"]]
        if self.stage.chapter == "map1":
            self.temp = 0    
        elif self.stage.chapter == "map2":
            self.temp = 1
        else:
            self.temp = 2

        if (self.stage.stage == 1): # 스테이지 단계
            self.stage_map = Stage(
                self.stage_data["chapter"][chapterlist[self.temp][1]]["2"]) # 맵이름을 가져오기 stage_data[챕터][맵이름][단계]
            StageGame(self.character_data,
                      self.character, self.stage_map, self.storyInfo, self.wselect).main_info()
            self.menu.disable()
        if (self.stage.stage == 2):
            self.stage_map = Stage(
                self.stage_data["chapter"][chapterlist[self.temp][1]]["3"])
            StageGame(self.character_data,
                      self.character, self.stage_map, self.storyInfo, self.wselect).main_info()
            self.menu.disable()

    # 클리어 화면
    def showStageClearScreen(self):
        pygame.mixer.music.stop()
        stageclaer_image = pygame_menu.baseimage.BaseImage(
        image_path=Images.stage_clear.value, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)  # 메뉴 이미지, Images는 Defs.py에 선언되어 있는 클래스명
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
        self.mytheme.background_color = stageclaer_image
        self.menu = pygame_menu.Menu('', self.size[0], self.size[1],
                                     theme=self.mytheme)
        #self.menu.add.button('to Menu', self.toMenu,self.menu)
        if (self.stage.stage != 3):
            self.menu.add.button(
                '다음 스테이지', self.nextstage, font_size=self.font_size)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('홈으로', self.gameselectmenu,
                             font_size=self.font_size)
        User.coin = User.coin + self.coin
        self.database = Database()
        self.database.set_coin()
        self.menu.mainloop(self.screen,bgfun = self.check_resize) 

    # 실패 화면
    def showGameOverScreen(self):
        pygame.mixer.music.stop()
        gameover_image = pygame_menu.baseimage.BaseImage(
        image_path=Images.gameover.value, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)  # 메뉴 이미지, Images는 Defs.py에 선언되어 있는 클래스명
        self.mytheme = pygame_menu.Theme(
            widget_font=Default.font.value,
            widget_background_color=(0, 10, 63),  # 버튼 배경색 설정
            title_font=Default.font.value,
            selection_color=(253, 111, 34),  # 선택됐을때 글씨색 설정
            widget_font_color=(255, 255, 255),  # 기본 글자색
            title_background_color=(255, 171, 0, 0),
            title_font_color=(255, 255, 255, 0),
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY,
            widget_font_size=self.size[0] * 45 // 720
        )
        self.mytheme.background_color = gameover_image
        self.menu = pygame_menu.Menu('', self.size[0], self.size[1],
                                     theme=self.mytheme)
        self.menu.add.label("점수 : {}".format(
            self.score), font_size=self.font_size)
        self.menu.add.vertical_margin(30)
        self.menu.add.button('  다시 시작  ', self.retry, font_size=self.font_size)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('모드 선택화면으로', self.Home, self.menu,
                             font_size=self.font_size)
        User.coin = User.coin + self.coin
        self.database = Database()
        self.database.set_coin()
        self.menu.mainloop(self.screen,bgfun = self.check_resize) 
    

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
        b3 = self.menu.add.button("모드 선택화면으로", self.gameselectmenu, selection_color=self.orange_color,
                             font_size=self.font_size,)


    # 화면 크기 조정 감지 및 비율 고정
    def check_resize(self):
        if (self.size != self.screen.get_size()):  # 현재 사이즈와 저장된 사이즈 비교 후 다르면 변경
            changed_screen_size = self.screen.get_size()  # 변경된 사이즈
            ratio_screen_size = (
                changed_screen_size[0], changed_screen_size[0]*783/720)  # y를 x에 비례적으로 계산
            if (ratio_screen_size[0] < 320):  # 최소 x길이 제한
                ratio_screen_size = (494, 537)
            if (ratio_screen_size[1] > 783):  # 최대 y길이 제한
                ratio_screen_size = (720, 783)
            self.screen = pygame.display.set_mode(ratio_screen_size,
                                                  pygame.RESIZABLE)
            window_size = self.screen.get_size()
            new_w, new_h = 1 * window_size[0], 1 * window_size[1]
            self.menu.resize(new_w, new_h)
            self.size = window_size
            self.menu._current._widgets_surface = make_surface(0, 0)
            font_size = new_w * 40 // 720
            self.font_size = font_size
            self.scale = (new_w*0.0020, new_h*0.0020)
            return True
