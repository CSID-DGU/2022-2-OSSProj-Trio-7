
from email.policy import default
from pickle import TRUE
from button import *
import pygame
# import pygame_menu
from data.CharacterDataManager import *
# from data.Stage import Stage
from data.StageDataManager import *
from game.StageGameplay import StageGame
from game.InfiniteGame import InfiniteGame
from pygame_menu.utils import make_surface
from pygame.locals import *
from data.Defs import *
from menu.WeaponSelect import *
# from menu.LeaderBoardMenu import *
from menu.MypageMenu import *
from menu.CharacterStoreMenu import *

from menu.HelpMenu import *

global soundset
soundset = 0.1

global choosed_chracter  # 사용자가 선택한 캐릭터


class GameselectMenu:
    def __init__(self, screen):

        self.size = screen.get_size()
        self.screen = screen
        self.changed_screen_size = self.screen.get_size()
        self.board_width = self.changed_screen_size[0]  # x
        self.board_height = self.changed_screen_size[1]  # y

        self.rankpage = button(self.board_height, self.board_height,
                               0.75, 0.05, 0.15, 0.063, "Image/thema/RANK.png")
        self.mypage = button(self.board_height, self.board_height,
                             0.15, 0.05, 0.15, 0.06, "Image/thema/MYPAGE.png")
        self.store = button(self.board_height, self.board_height,
                            0.3, 0.05, 0.15, 0.06, "Image/thema/STORE.png")
        self.logout = button(self.board_height, self.board_height,
                             0.9, 0.05, 0.15, 0.06, "Image/thema/logout.png")
        self.help = button(self.board_height, self.board_height,
                           0.61, 0.05, 0.15, 0.06, "Image/thema/help.png")

        self.returnpage = button(self.board_height, self.board_height,  # 직업 선택페이지로 되돌아가기
                                 0.45, 0.05, 0.17, 0.065, "Image/thema/return.png")

        self.setting = button(self.board_height, self.board_height, 0.05,
                              0.05, 0.06, 0.06, "Image/thema/on.png")  # sound on/off

        self.barcol = button(self.board_height, self.board_height,
                             0.5, 0.0, 1, 0.2, "Image/thema/bar.png")

        self.logo = button(self.board_height, self.board_height,
                           0.5, 0.92, 0.4, 0.07, "Image/thema/logo.png")

        self.stageMode = button(self.board_width, self.board_height,
                                0.3, 0.4, 0.35, 0.45, "Image/stageMode.png")

        self.infiniteMode = button(self.board_width, self.board_height,
                                   0.7, 0.4, 0.35, 0.45, "Image/infiniteMode.png")

        self.stage_level_button = button(self.board_width, self.board_height,
                                         0.3, 0.75, 0.35, 0.05, "Image/thema/level1.png")

        self.mode_map1 = button(self.board_width, self.board_height,
                                0.7, 0.75, 0.35, 0.05, "Image/catthema/SCORE.png")

        self.inf_mode_map1 = 0

        self.buttonlist = [self.barcol, self.stageMode, self.infiniteMode, self.returnpage, self.stage_level_button, self.mode_map1,
                           self.rankpage, self.mypage, self.store, self.setting, self.logout, self.help, self.logo]

        self.attchar = ["./Image/policeCharacters/policeStage_monster.png",
                        "./Image/fireCharacters/FireStage_monster.png", "./Image/doctorCharacters/doctorStage_monster.png"]

        self.police_attackTarget = ["./Image/policeCharacters/policeStage_monster.png",
                                    "./Image/policeCharacters/policeStage_boss1.png", "./Image/policeCharacters/policeStage_boss2.png", "./Image/policeCharacters/policeStage_boss3.png"]
        self.firefighter_attackTarget = ["./Image/fireCharacters/FireStage_monster.png",
                                         "./Image/fireCharacters/FireStage_boss1.png", "./Image/fireCharacters/FireStage_boss2.png", "./Image/fireCharacters/FireStage_boss3.png"]
        self.doctor_attackTarget = ["./Image/doctorCharacters/doctorStage_monster.png",
                                    "./Image/doctorCharacters/doctorStage_boss1.png", "./Image/doctorCharacters/doctorStage_boss2.png", "./Image/doctorCharacters/doctorStage_boss3.png"]

        self.police_background = ["./Image/background/police_background.png"]
        self.firefighter_background = [
            "./Image/background/firefighter_background.png"]
        self.doctor_background = ["./Image/background/doctor_background.png"]

        self.stage_level = "1"

        self.sound = "on"

        self.mode = [("score", InfiniteGame.ScoreMode()),
                     ("time", InfiniteGame.TimeMode())]

        self.inf_mode = 0

        self.temp1 = self.stage_level_button.image
        #self.temp2 = self.infinite_level_button.image

        self.stage_data = StageDataManager.loadStageData()  # 스테이지 데이터
        self.character_data = CharacterDataManager.load()  # 캐릭터 데이터
        self.selectedChapter = [list(self.stage_data["chapter"].keys())[0]]

        self.stay = 0

    def show(self, screen, character):
        global soundset
        self.check_resize(screen)
        choosed_chracter = character

        # if self.modestate == "stage":  # stage mode

        screen.fill((255, 255, 255))  # 배경 나중에 바꾸기.

        for self.button in enumerate(self.buttonlist):  # 버튼 그리기
            # 화면 사이즈 변경되면 버튼사이즈 바꿔줌.
            self.button[1].change(
                screen.get_size()[0], screen.get_size()[1])
            self.button[1].draw(screen, (0, 0, 0))

        for event in pygame.event.get():

            pos = pygame.mouse.get_pos()  # mouse

            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.MOUSEMOTION:  # 마우스모션
                if self.stage_level_button.isOver(pos):
                    if self.stage_level == "1":
                        self.stage_level_button.image = "Image/menu/level2.png"
                    elif self.stage_level == "2":
                        self.stage_level_button.image = "Image/menu/level3.png"
                    elif self.stage_level == "3":
                        self.stage_level_button.image = "Image/menu/level1.png"
                else:
                    self.stage_level_button.image = self.temp1
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONUP:  # 마우스 클릭
                self.check = Database().check_char_lock()
                if self.stageMode.isOver(pos):  # 맵 선택하면 게임이랑 연결시키기
                    if choosed_chracter == "police":  # 경찰관 맵
                        # 무기 선택 상점을 추가============================================================================================
                        page = WeaponSelect(self.screen)
                        while True:
                            game.show(self.screen)
                            pygame.display.flip()

                        self.stage_map = Stage(
                            self.stage_data["chapter"]["gloomy street"][self.stage_level])

                        if self.check:
                            import menu.FailPlay
                            menu.FailPlay.FailPlay(self.screen).show()
                        else:
                            StageGame(
                                self.character_data, self.character_data[User.character], self.stage_map, "police").main_info()
                        pygame.display.update()

                    elif choosed_chracter == "firefighter":  # 소방관 맵
                        self.stage_map = Stage(
                            self.stage_data["chapter"]["burning house"][self.stage_level])

                        if self.check:
                            import menu.FailPlay
                            menu.FailPlay.FailPlay(self.screen).show()
                        else:
                            StageGame(
                                self.character_data, self.character_data[User.character], self.stage_map, "firefighter").main_info()
                        pygame.display.update()
                    else:  # 의사 맵
                        self.stage_map = Stage(
                            self.stage_data["chapter"]["hospital"][self.stage_level])

                        if self.check:
                            import menu.FailPlay
                            menu.FailPlay.FailPlay(self.screen).show()
                        else:
                            StageGame(
                                self.character_data, self.character_data[User.character], self.stage_map, "doctor").main_info()
                        pygame.display.update()

                if self.stage_level_button.isOver(pos):
                    if self.stage_level == "1":
                        self.temp1 = "Image/menu/level2.png"  # 이미지 바꾸기
                        self.stage_level = "2"  # 바뀐 레벨로 저장.

                    elif self.stage_level == "2":
                        self.temp1 = "Image/menu/level3.png"  # 이미지 바꾸기
                        self.stage_level = "3"  # 바뀐 레벨로 저장.

                    elif self.stage_level == "3":
                        self.temp1 = "Image/menu/level1.png"  # 이미지 바꾸기
                        self.stage_level = "1"  # 바뀐 레벨로 저장.
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONUP:  # 마우스 클릭
                if self.mode_map1.isOver(pos):
                    if self.inf_mode_map1 == 0:
                        self.inf_mode_map1 = 1
                        self.mode_map1.image = "Image/catthema/TIME.png"
                    else:
                        self.inf_mode_map1 = 0
                        self.mode_map1.image = "Image/catthema/SCORE.png"
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONUP:  # 마우스 클릭
                if self.infiniteMode.isOver(pos):  # 맵 선택하면 게임이랑 연결시키기
                    self.stage_map = self.mode[self.inf_mode_map1][1]
                    if self.check:
                        import menu.FailPlay
                        menu.FailPlay.FailPlay(self.screen).show()
                    else:
                        if choosed_chracter == "police":  # 경찰관 맵
                            InfiniteGame(self.character_data[User.character], "police", self.stage_map,
                                         "Image/background/police_background.png", self.police_attackTarget[0], self.police_attackTarget[1], self.police_attackTarget[2], self.police_attackTarget[3]).main()
                        elif choosed_chracter == "firefighter":  # 소방관 맵
                            InfiniteGame(self.character_data[User.character], "firefighter", self.stage_map,
                                         "Image/background/firefighter_background.png", self.firefighter_attackTarget[0], self.firefighter_attackTarget[1], self.firefighter_attackTarget[2], self.firefighter_attackTarget[3]).main()
                        else:  # 의사 맵
                            InfiniteGame(self.character_data[User.character], "doctor", self.stage_map,
                                         "Image/background/doctor_background.png", self.doctor_attackTarget[0], self.doctor_attackTarget[1], self.doctor_attackTarget[2], self.doctor_attackTarget[3]).main()
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONUP:  # 마우스 클릭
                if self.mypage.isOver(pos):
                    Mypage(self.screen).show()

                if self.rankpage.isOver(pos):
                    LeaderBoardMenu(self.screen).rank()

<<<<<<< HEAD
            if self.store.isOver(pos):
                CharacterStoreMenu(self.screen, choosed_chracter).show()
=======
                if self.store.isOver(pos):
                    CharacterStoreMenu(self.screen).show()
>>>>>>> 88618ad8f1c6bdaca8e82e75f6b43911734b0199

                if self.help.isOver(pos):
                    HelpMenu(self.screen).show()

                if self.logout.isOver(pos):
                    import Main
                    Main.Login(self.screen).show()

                if self.returnpage.isOver(pos):  # 직업 선택 화면으로 되돌아가는 페이지
                    from menu.CharacterSelectMenu import CharacterSelect
                    game = CharacterSelect(self.screen)

                    while True:
                        game.show(self.screen)
                        pygame.display.flip()

                if self.setting.isOver(pos):
                    if self.sound == "on":
                        self.setting.image = "Image/thema/off.png"
                        self.sound = "off"
                        soundset = 0
                        print(soundset)
                        Default.sound.value['sfx']['volume'] = 0
                        self.character_data = CharacterDataManager.load()  # volume 적용
                    else:
                        self.setting.image = "Image/thema/on.png"
                        self.sound = "on"
                        soundset = 0.1
                        print(soundset)
                        Default.sound.value['sfx']['volume'] = 0.1
                        self.character_data = CharacterDataManager.load()  # volume 적용

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
