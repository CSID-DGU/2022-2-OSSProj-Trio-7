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
from menu.CharacterStoreMenu_p import *
from menu.CharacterStoreMenu_f import *
from menu.CharacterStoreMenu_d import *
from data.database_user import *
from menu.HelpMenu import *
from menu.Mypage_p import *
from menu.Mypage_f import *
from menu.Mypage_d import *
from menu.wselectmenu import *


global soundset
soundset = 0.1

global choosed_character  # 사용자가 선택한 캐릭터


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
                              0.05, 0.06, 0.06, "Image/thema/on.png")


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
        
        self.background_music = "./Sound/bgm/bgm_gameSelect.wav"

        self.mode = [("score", InfiniteGame.ScoreMode()),
                     ("time", InfiniteGame.TimeMode())]

        self.inf_mode = 0

        self.temp1 = self.stage_level_button.image

        self.stage_data = StageDataManager.loadStageData()  # 스테이지 데이터
        self.character_data = CharacterDataManager.load()  # 캐릭터 데이터
        self.selectedChapter = [list(self.stage_data["chapter"].keys())[0]]

        self.stay = 0

        pygame.mixer.init()
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)
        
    def show(self, screen, character):
        global soundset
        self.check_resize(screen)
        choosed_character = character



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

        screen.fill((255, 255, 255))

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
                        self.stage_level_button.image = "Image/thema/level2.png"
                    elif self.stage_level == "2":
                        self.stage_level_button.image = "Image/thema/level3.png"
                    elif self.stage_level == "3":
                        self.stage_level_button.image = "Image/thema/level1.png"
                else:
                    self.stage_level_button.image = self.temp1
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONUP:  # 마우스 클릭
                self.database = Database()
                self.pcheck = Database().check_pchar_lock()
                self.fcheck = Database().check_fchar_lock()
                self.dcheck = Database().check_dchar_lock()

                if self.stageMode.isOver(pos):  # 맵 선택하면 게임이랑 연결시키기
                    wselectMenu(self.screen)
                    game = wselectMenu(self.screen)
                    winfo=""
                    while True:
                        game.show()
                        pygame.display.flip()
                        if game.isSelect==True:
                            winfo = game.weapon    
                            if choosed_character == "police":  # 경찰관 맵
                                print('show_pmychar')
                                User.pcharacter = self.database.show_pmychar()

                                self.stage_map = Stage(
                                    self.stage_data["chapter"]["gloomy street"][self.stage_level])

                                if self.pcheck:
                                    import menu.FailPlay
                                    menu.FailPlay.FailPlay(self.screen).show()
                                else:
                                    StageGame(
                                        self.character_data, self.character_data[User.pcharacter], self.stage_map, "police", winfo).main_info() 
                                pygame.display.update()

                            if choosed_character == "firefighter":    
                                print('show_fmychar')
                                User.fcharacter = self.database.show_fmychar()
                                self.stage_map = Stage(
                                    self.stage_data["chapter"]["burning house"][self.stage_level])

                                if self.fcheck:
                                    import menu.FailPlay
                                    menu.FailPlay.FailPlay(self.screen).show()
                                else:
                                    StageGame(
                                        self.character_data, self.character_data[User.fcharacter], self.stage_map, "firefighter", winfo).main_info()
                                pygame.display.update()

                            if choosed_character == "doctor": 
                                print('show_dmychar')
                                User.dcharacter = self.database.show_dmychar()
                                self.stage_map = Stage(
                                    self.stage_data["chapter"]["hospital"][self.stage_level])

                                if self.dcheck:
                                    import menu.FailPlay
                                    menu.FailPlay.FailPlay(self.screen).show()
                                else:
                                    StageGame(
                                        self.character_data, self.character_data[User.dcharacter], self.stage_map, "doctor", winfo).main_info()
                                pygame.display.update()
               

                if self.stage_level_button.isOver(pos):
                    if self.stage_level == "1":
                        self.temp1 = "Image/thema/level2.png"  # 이미지 바꾸기
                        self.stage_level = "2"  # 바뀐 레벨로 저장.

                    elif self.stage_level == "2":
                        self.temp1 = "Image/thema/level3.png"  # 이미지 바꾸기
                        self.stage_level = "3"  # 바뀐 레벨로 저장.

                    elif self.stage_level == "3":
                        self.temp1 = "Image/thema/level1.png"  # 이미지 바꾸기
                        self.stage_level = "1"  # 바뀐 레벨로 저장.
                pygame.display.update()
                
                if self.mode_map1.isOver(pos):
                    if self.inf_mode_map1 == 0:
                        self.inf_mode_map1 = 1
                        self.mode_map1.image = "Image/catthema/TIME.png"
                    else:
                        self.inf_mode_map1 = 0
                        self.mode_map1.image = "Image/catthema/SCORE.png"
                pygame.display.update()

# ====================================================인피니티 모드==================================
            if event.type == pygame.MOUSEBUTTONUP:  # 마우스 클릭
                if self.infiniteMode.isOver(pos):  # 맵 선택하면 게임이랑 연결시키기  
                    if choosed_character == "police":  # 경찰관 맵
                        wselectMenu(self.screen)
                        game = wselectMenu(self.screen)

                        winfo = ""
                        while True:
                            game.show()
                            pygame.display.flip()

                            if game.isSelect == True:
                                winfo = game.weapon # 무기 구매 정보
                        
                                self.stage_map=self.mode[self.inf_mode_map1][1]
                                User.pcharacter = self.database.show_pmychar()
                                # wselectMenu(self.screen)
                                # game = wselectMenu(self.screen)
                                if self.pcheck:
                                    import menu.FailPlay
                                    menu.FailPlay.FailPlay(self.screen).show()
                                else: 
                                    InfiniteGame(self.character_data[User.pcharacter], "police", self.stage_map,
                                                "Image/background/police_background.png", self.police_attackTarget[0], self.police_attackTarget[1], self.police_attackTarget[2], self.police_attackTarget[3], winfo).main()
                                pygame.display.update()

            
                if self.infiniteMode.isOver(pos):  # 맵 선택하면 게임이랑 연결시키기
                    if choosed_character == "firefighter":  # 소방관 맵
                        wselectMenu(self.screen)
                        game = wselectMenu(self.screen)
                        
                        winfo = ""
                        while True:
                            game.show()
                            pygame.display.flip()
                            if game.isSelect == True:
                                winfo = game.weapon # 무기 구매 정보

                                self.stage_map=self.mode[self.inf_mode_map1][1]
                                User.fcharacter = self.database.show_fmychar()
                                if self.fcheck:
                                    import menu.FailPlay
                                    menu.FailPlay.FailPlay(self.screen).show()
                                else: 
                                    InfiniteGame(self.character_data[User.fcharacter], "firefighter", self.stage_map,
                                                "Image/background/firefighter_background.png", self.firefighter_attackTarget[0], self.firefighter_attackTarget[1], self.firefighter_attackTarget[2], self.firefighter_attackTarget[3], winfo).main()
                                pygame.display.update()

                if self.infiniteMode.isOver(pos):  # 맵 선택하면 게임이랑 연결시키기
                    if choosed_character == "doctor":  # 소방관 맵
                        wselectMenu(self.screen)
                        game = wselectMenu(self.screen)
                        
                        winfo = ""
                        while True:
                            game.show()
                            pygame.display.flip()
                            if game.isSelect == True:
                                winfo = game.weapon # 무기 구매 정보
                                self.stage_map=self.mode[self.inf_mode_map1][1]
                                User.dcharacter = self.database.show_dmychar() # 캐릭터 분류하는 필수 함수
                                if self.dcheck:
                                    import menu.FailPlay
                                    menu.FailPlay.FailPlay(self.screen).show()
                                else:
                                    InfiniteGame(self.character_data[User.dcharacter], "doctor", self.stage_map,
                                                "Image/background/doctor_background.png", self.doctor_attackTarget[0], self.doctor_attackTarget[1], self.doctor_attackTarget[2], self.doctor_attackTarget[3], winfo).main()
                                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONUP:  # 마우스 클릭

                if self.mypage.isOver(pos):
                    if choosed_character == "police":
                        Mypage_p(self.screen).show()
                    elif choosed_character == "firefighter":
                        Mypage_f(self.screen).show()
                    elif choosed_character == "doctor":
                        Mypage_d(self.screen).show()

                if self.rankpage.isOver(pos):
                    LeaderBoardMenu(self.screen).rank()

                if self.store.isOver(pos):
                    if choosed_character=="police":
                        CharacterStoreMenu_p(self.screen, choosed_character).show()
                    if choosed_character=="firefighter":
                        CharacterStoreMenu_f(self.screen, choosed_character).show()
                    if choosed_character=="doctor":
                        CharacterStoreMenu_d(self.screen, choosed_character).show()

                if self.help.isOver(pos):
                    HelpMenu(self.screen, choosed_character).show()

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
                        pygame.mixer.music.set_volume(0)
                        self.character_data = CharacterDataManager.load()  # volume 적용
                    else:
                        self.setting.image = "Image/thema/on.png"
                        self.sound = "on"
                        soundset = 0.1
                        print(soundset)
                        Default.sound.value['sfx']['volume'] = 0.1
                        pygame.mixer.music.set_volume(0.1)
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
            screen = pygame.display.set_mode(ratio_screen_size, pygame.RESIZABLE)