from button import *
import pygame
import pygame_menu
from menu.gameselectMenu import GameselectMenu


class CharacterSelect:
    def __init__(self, screen):
        self.size = screen.get_size()
        self.screen = screen
        self.changed_screen_size = self.screen.get_size()
        self.board_width = self.changed_screen_size[0]  # x
        self.board_height = self.changed_screen_size[1]  # y

        self.charactor1 = button(self.board_width, self.board_height,
                                 0.2, 0.4, 0.25, 0.35, "Image/policeCharacters/policeOfficer.png")
        self.charactor2 = button(self.board_width, self.board_height,
                                 0.5, 0.4, 0.25, 0.35, "Image/fireCharacters/firefighter.png")
        self.charactor3 = button(self.board_width, self.board_height,
                                 0.8, 0.4, 0.25, 0.35, "Image/doctorCharacters/doctor.png")

        self.buttonlist = [self.charactor1, self.charactor2, self.charactor3]

        self.mytheme = pygame_menu.Theme(
            widget_font=Default.font.value,
            # 버튼 가독성 올리기 위해서 버튼 배경색 설정 : 노란색
            widget_background_color=(255, 171, 0),
            title_font=Default.font.value,
            selection_color=(0, 0, 0),  # 선택됐을때 글씨색 설정 (white)
            widget_font_color=(255, 255, 255),  # 기본 글씨색 설정 (black)
            title_background_color=(255, 171, 0),
            title_font_color=(255, 255, 255),
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY,
            widget_font_size=self.size[0] * 45 // 720
        )

        main_image = pygame_menu.baseimage.BaseImage(
            image_path=Images.characterSelect.value, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)  # 메뉴 이미지, Images는 Defs.py에 선언되어 있는 클래스명

        self.mytheme.background_color = main_image

        self.menu = pygame_menu.Menu(
            '', self.size[0], self.size[1], theme=self.mytheme)  # 상단바
        self.first_page()
        self.menu.mainloop(self.screen, bgfun=self.check_resize)

    def show(self, screen):
        self.check_resize(screen)
        screen.fill((255, 255, 255))  # 배경 나중에 바꾸기.

    def check_resize(self, screen):
        if (self.size != screen.get_size()):  # 현재 사이즈와 저장된 사이즈 비교 후 다르면 변경
            changed_screen_size = self.screen.get_size()  # 변경된 사이즈
            ratio_screen_size = (
                changed_screen_size[0], changed_screen_size[0]*783/720)  # y를 x에 비례적으로 계산
            if (ratio_screen_size[0] < 320):  # 최소 x길이 제한
                ratio_screen_size = (494, 537)
            if (ratio_screen_size[1] > 783):  # 최대 y길이 제한
                ratio_screen_size = (720, 783)
            screen = pygame.display.set_mode(
                ratio_screen_size, pygame.RESIZABLE)

    def show_policMap(self):
        print("경찰관선택")
        game = GameselectMenu(self.screen)

        while True:
            game.show(self.screen, "police")
            pygame.display.flip()

    def show_firefighterMap(self):
        print("소방관선택")
        game = GameselectMenu(self.screen)

        while True:
            game.show(self.screen, "firefighter")
            pygame.display.flip()

    def show_doctorMap(self):
        print("의사선택")
        game = GameselectMenu(self.screen)

        while True:
            game.show(self.screen, "doctor")
            pygame.display.flip()

    def first_page(self):
        self.menu.clear()
        b1 = self.menu.add.button(' 경찰관  ', self.show_policMap)
        self.menu.add.vertical_margin(10)
        b2 = self.menu.add.button(' 소방관 ', self.show_firefighterMap)
        self.menu.add.vertical_margin(10)
        b3 = self.menu.add.button('   의사   ', self.show_doctorMap)
