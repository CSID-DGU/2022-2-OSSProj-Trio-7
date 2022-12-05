
import pygame
import pygame_menu
from data.Defs import *
from pygame_menu.locals import ALIGN_CENTER, ALIGN_LEFT, ALIGN_RIGHT
from pygame_menu.utils import make_surface
from pygame_menu.widgets.core.widget import Widget

# 도움말 화면


class HelpMenu:
    def __init__(self, screen, choosed_character):
        self.size = screen.get_size()
        self.screen = screen
        
        self.orange_color = (253, 111, 34)
        self.font_size = self.size[0] * 38 // 720  # 글씨크기

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

        main_image = pygame_menu.baseimage.BaseImage(
            image_path=Images.help.value, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)  # 메뉴 이미지, Images는 Defs.py에 선언되어 있는 클래스명

        self.mytheme.background_color = main_image

        self.menu = pygame_menu.Menu(
            '', self.size[0], self.size[1], theme=self.mytheme)  # 상단바
        self.choosed_character = choosed_character # 현재 유저 정보 저장
        self.show()
        self.menu.mainloop(self.screen, bgfun=self.check_resize)

    def gameselectmenu(self):
        import menu.gameselectMenu
        game = menu.gameselectMenu.GameselectMenu(self.screen)

        while True:
            game.show(self.screen, self.choosed_character)
            pygame.display.flip()


    # 도움말 메인 메뉴
    def show(self):
        self.menu.clear()
        self.menu.add.button('     스테이지 모드     ', self.infinite_game_1,
                             selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('     무한 모드     ', self.stage_game_1,
                             selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('   아이템 설명서   ', self.items,
                             selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('   조작법 설명서   ', self.controls,
                             selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('         이전         ',self.gameselectmenu,
                             selection_color=self.orange_color, font_size=self.font_size)
        self.menu.mainloop(self.screen, bgfun=self.check_resize)

    # 무한 모드 설명 페이지 1
    def infinite_game_1(self):
        self.menu.clear()
        self.menu.add.label("1", font_size=self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_infi_1.value, scale=(
            self.size[0]*0.001, self.size[1]*0.001))
        self.menu.add.button('     다음     ', self.infinite_game_2,
                             selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.button('         이전         ', self.show,
                             selection_color=self.orange_color, font_size=self.font_size)

    # 무한 모드 설명 페이지 2
    def infinite_game_2(self):
        self.menu.clear()
        self.menu.add.label("2", font_size=self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_infi_2.value, scale=(
            self.size[0]*0.001, self.size[1]*0.001))
        self.menu.add.button('     다음     ', self.infinite_game_3,
                             selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.button('         이전         ', self.infinite_game_1,
                             selection_color=self.orange_color, font_size=self.font_size)

    # 무한 모드 설명 페이지 3
    def infinite_game_3(self):
        self.menu.clear()
        self.menu.add.label("3", font_size=self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_infi_3.value, scale=(
            self.size[0]*0.001, self.size[1]*0.001))
        self.menu.add.button('     다음     ', self.infinite_game_4,
                             selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.button('         이전         ', self.infinite_game_2,
                             selection_color=self.orange_color, font_size=self.font_size)

    # 무한 모드 설명 페이지 4
    def infinite_game_4(self):
        self.menu.clear()
        self.menu.add.label("4", font_size=self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_infi_4.value, scale=(
            self.size[0]*0.001, self.size[1]*0.001))
        self.menu.add.button('     다음     ', self.infinite_game_5,
                             selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.button('         이전         ', self.infinite_game_3,
                             selection_color=self.orange_color, font_size=self.font_size)

    # 무한 모드 설명 페이지 5
    def infinite_game_5(self):
        self.menu.clear()
        self.menu.add.label("5", font_size=self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_infi_5.value, scale=(
            self.size[0]*0.001, self.size[1]*0.001))
        self.menu.add.button('     다음     ', self.show,
                             selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.button('         이전         ', self.infinite_game_4,
                             selection_color=self.orange_color, font_size=self.font_size)

    # 스테이지 모드 설명 페이지 1
    def stage_game_1(self):
        self.menu.clear()
        self.menu.add.label("1", font_size=self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_stage_1.value, scale=(
            self.size[0]*0.001, self.size[1]*0.001))
        self.menu.add.button('     다음     ', self.stage_game_2,
                             selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.button('         이전         ', self.show,
                             selection_color=self.orange_color, font_size=self.font_size)

    # 스테이지 모드 설명 페이지 2
    def stage_game_2(self):
        self.menu.clear()
        self.menu.add.label("2", font_size=self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_stage_2.value, scale=(
            self.size[0]*0.001, self.size[1]*0.001))
        self.menu.add.button('     다음     ', self.stage_game_3,
                             selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.button('         이전         ', self.stage_game_1,
                             selection_color=self.orange_color, font_size=self.font_size)

    # 스테이지 모드 설명 페이지 3
    def stage_game_3(self):
        self.menu.clear()
        self.menu.add.label("3", font_size=self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_stage_3.value, scale=(
            self.size[0]*0.001, self.size[1]*0.001))
        self.menu.add.button('     다음     ', self.stage_game_4,
                             selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.button('         이전         ', self.stage_game_2,
                             selection_color=self.orange_color, font_size=self.font_size)

    # 스테이지 모드 설명 페이지 4
    def stage_game_4(self):
        self.menu.clear()
        self.menu.add.label("4", font_size=self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_stage_4.value, scale=(
            self.size[0]*0.001, self.size[1]*0.001))
        self.menu.add.button('     다음     ', self.stage_game_5,
                             selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.button('         이전         ', self.stage_game_3,
                             selection_color=self.orange_color, font_size=self.font_size)

    # 스테이지 모드 설명 페이지 5
    def stage_game_5(self):
        self.menu.clear()
        self.menu.add.label("5", font_size=self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_stage_5.value, scale=(
            self.size[0]*0.001, self.size[1]*0.001))
        self.menu.add.button('     다음     ', self.show,
                             selection_color=self.orange_color, font_size=self.font_size)
        self.menu.add.button('         이전         ', self.stage_game_4,
                             selection_color=self.orange_color, font_size=self.font_size)

    # 아이템 설명 페이지
    def items(self):
        self.menu.clear()
        self.menu.add.vertical_margin(30)
        self.menu.add.image(Images.info_items.value, scale=(
            self.size[0]*0.001, self.size[1]*0.001))
        self.menu.add.button('         이전         ', self.show,
                             selection_color=self.orange_color, font_size=self.font_size)

    # 조작법 설명 페이지
    def controls(self):
        self.menu.clear()
        self.menu.add.vertical_margin(30)
        self.menu.add.image(Images.info_controls.value, scale=(
            self.size[0]*0.001, self.size[1]*0.001))
        self.menu.add.button('         이전         ', self.show,
                             selection_color=self.orange_color, font_size=self.font_size)

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
            self.menu._current._widgets_surface = make_surface(0, 0)
            self.size = window_size
            print(f'New menu size: {self.menu.get_size()}')
            font_size = new_w * 40 // 720
            self.font_size = font_size
