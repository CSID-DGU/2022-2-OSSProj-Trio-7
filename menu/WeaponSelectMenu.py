from email.policy import default
from pickle import TRUE
from button import *
import pygame
# import pygame_menu
from data.CharacterDataManager import *
# from data.Stage import Stage
from data.StageDataManager import *
from game.StageGame import StageGame
from game.InfiniteGame import InfiniteGame
from pygame_menu.utils import make_surface
from pygame.locals import *
from data.Defs import *
# from menu.LeaderBoardMenu import *
from menu.CharacterStoreMenu_p import *
from menu.CharacterStoreMenu_f import *
from menu.CharacterStoreMenu_d import *
from data.database_user import *
from menu.HelpMenu import *
from menu.Mypage_p import *
from menu.Mypage_f import *
from menu.Mypage_d import *

class wselectMenu:
    def __init__(self, screen):
        title = "무기 선택"
        pygame.display.set_caption(title)  # 창의 제목 표시줄 옵션
        self.size = screen.get_size()
        self.screen = screen
        self.changed_screen_size = self.screen.get_size()
        self.board_width = self.changed_screen_size[0]  # x
        self.board_height = self.changed_screen_size[1]  # y

        self.isSelect = False
        self.weapon = ""

        self.stageW = button(self.board_width, self.board_height,
                                0.17, 0.4, 0.32, 0.45, "Image/weaponSelect/wstage.png")

        self.infiniteW = button(self.board_width, self.board_height,
                                   0.825, 0.4, 0.32, 0.45, "Image/weaponSelect/winfinite.png")

        self.defaultW = button(self.board_width, self.board_height,
                                         0.5, 0.4, 0.32, 0.45, "Image/weaponSelect/wdefault.png")

        self.backgroundw = button(self.board_width, self.board_height,
                                         0.5, 0.5, 1.0, 1.0, "Image/weaponSelect/wbackground.png")


        self.buttonlist = [self.backgroundw, self.infiniteW, self.stageW, self.defaultW]

        self.stage_data = StageDataManager.loadStageData()  # 스테이지 데이터
        self.character_data = CharacterDataManager.load()  # 캐릭터 데이터
        self.selectedChapter = [list(self.stage_data["chapter"].keys())[0]]

        self.stay = 0
        self.check_resize(screen)
       
    def show(self):
        
        self.screen.fill((255, 255, 255))  # 배경 나중에 바꾸기.
        # bg = pygame.image.load("Image/weaponSelect/wbackground.png")
        # bg = pygame.transform.scale(bg, self.size)
        # self.screen.blit(bg, (0, 0))

        for self.button in enumerate(self.buttonlist):  # 버튼 그리기
            # 화면 사이즈 변경되면 버튼사이즈 바꿔줌.
            self.button[1].change(
                self.screen.get_size()[0], self.screen.get_size()[1])
            self.button[1].draw(self.screen, (0, 0, 0))

        for event in pygame.event.get():

             pos = pygame.mouse.get_pos()  # mouse

             if event.type == pygame.QUIT:
                 pygame.quit()
                 break

             if event.type == pygame.MOUSEBUTTONUP:  # 마우스 클릭
                if self.stageW.isOver(pos):
                    if (User.coin>=2000):
                        print("데미지 강화 아이템을 구매하셨습니다.")
                        self.isSelect = True
                        self.weapon = "stage" # 구매한 무기 정보를 설정
                        database = Database()
                        database.buy_weapon()
                        return
                    else:
                        print("돈이 부족합니다.")
                
                if self.infiniteW.isOver(pos):
                    if(User.coin>=2000):
                        print("속도 강화 아이템을 구매하셨습니다.")
                        self.isSelect = True
                        self.weapon = "infinite"
                        database = Database()
                        database.buy_weapon()
                        return
                    else:
                        print("돈이 부족합니다.")
                if self.defaultW.isOver(pos):
                    print("기본 무기로 플레이합니다.")
                    self.isSelect = True
                    self.weapon = "default"
                    return

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
            return 0