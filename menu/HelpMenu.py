
import pygame
import pygame_menu
from data.Defs import *
from pygame_menu.locals import ALIGN_CENTER, ALIGN_LEFT, ALIGN_RIGHT
from pygame_menu.utils import make_surface
from pygame_menu.widgets.core.widget import Widget

# 도움말 화면
class HelpMenu:
    def __init__(self,screen):
        self.size = screen.get_size()
        self.screen = screen
        self.font_size = self.size[0] * 38 //720 # 글씨크기
        self.mytheme = pygame_menu.themes.THEME_DEFAULT.copy()
        self.mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
        self.mytheme.title_close_button_cursor = pygame_menu.locals.CURSOR_HAND
        self.mytheme.title_font_color = Color.WHITE.value
        self.mytheme.background_color = Color.WHITE.value
        self.menu = pygame_menu.Menu('Help', self.size[0], self.size[1],
                            theme=self.mytheme)

    # 메인 메뉴로 돌아가기
    def to_menu(self):
        self.menu.disable()

    # 도움말 메인 메뉴
    def show(self):
        self.menu.clear()
        self.menu.add.vertical_margin(Menus.margin_20.value)
        self.menu.add.label("   - HELP -   ", selectable=False,font_size = self.font_size)
        self.menu.add.button('     infinite game     ', self.infinite_game_1, selection_color=Color.BLACK.value,font_size = self.font_size)
        self.menu.add.button('     stage game     ', self.stage_game_1, selection_color=Color.BLACK.value,font_size = self.font_size)
        self.menu.add.button('     items     ', self.items, selection_color=Color.BLACK.value,font_size = self.font_size)
        self.menu.add.button('     controls     ', self.controls, selection_color=Color.BLACK.value,font_size = self.font_size)
        self.menu.add.button('         back         ', self.to_menu, selection_color=Color.BLACK.value,font_size = self.font_size)
        self.menu.mainloop(self.screen,bgfun = self.check_resize)

    # 무한 모드 설명 페이지 1
    def infinite_game_1(self):
        self.menu.clear()
        self.menu.add.label("1",font_size = self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_infi_1.value, scale=(self.size[0]*0.001,self.size[1]*0.001))
        self.menu.add.button('     next     ', self.infinite_game_2, selection_color=Color.BLACK.value,font_size = self.font_size)
        self.menu.add.button('         back         ', self.show, selection_color=Color.BLACK.value,font_size = self.font_size)

    # 무한 모드 설명 페이지 2
    def infinite_game_2(self):
        self.menu.clear()
        self.menu.add.label("2",font_size = self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_infi_2.value, scale=(self.size[0]*0.001,self.size[1]*0.001))
        self.menu.add.button('     next     ', self.infinite_game_3, selection_color=Color.BLACK.value,font_size = self.font_size)
        self.menu.add.button('         back         ', self.infinite_game_1, selection_color=Color.BLACK.value,font_size = self.font_size)

    # 무한 모드 설명 페이지 3
    def infinite_game_3(self):
        self.menu.clear()
        self.menu.add.label("3",font_size = self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_infi_3.value, scale=(self.size[0]*0.001,self.size[1]*0.001))
        self.menu.add.button('     next     ', self.infinite_game_4, selection_color=Color.BLACK.value,font_size = self.font_size)
        self.menu.add.button('         back         ', self.infinite_game_2, selection_color=Color.BLACK.value,font_size = self.font_size)

    # 무한 모드 설명 페이지 4
    def infinite_game_4(self):
        self.menu.clear()
        self.menu.add.label("4",font_size = self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_infi_4.value, scale=(self.size[0]*0.001,self.size[1]*0.001))
        self.menu.add.button('     next     ', self.infinite_game_5, selection_color=Color.BLACK.value,font_size = self.font_size)
        self.menu.add.button('         back         ', self.infinite_game_3, selection_color=Color.BLACK.value,font_size = self.font_size)

    # 무한 모드 설명 페이지 5
    def infinite_game_5(self):
        self.menu.clear()
        self.menu.add.label("5",font_size = self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_infi_5.value, scale=(self.size[0]*0.001,self.size[1]*0.001))
        self.menu.add.button('     quit     ', self.show, selection_color=Color.BLACK.value,font_size = self.font_size)
        self.menu.add.button('         back         ', self.infinite_game_4, selection_color=Color.BLACK.value,font_size = self.font_size)

    # 스테이지 모드 설명 페이지 1
    def stage_game_1(self):
        self.menu.clear()
        self.menu.add.label("1",font_size = self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_stage_1.value, scale=(self.size[0]*0.001,self.size[1]*0.001))
        self.menu.add.button('     next     ', self.stage_game_2, selection_color=Color.BLACK.value,font_size = self.font_size)
        self.menu.add.button('         back         ', self.show, selection_color=Color.BLACK.value,font_size = self.font_size)

    # 스테이지 모드 설명 페이지 2
    def stage_game_2(self):
        self.menu.clear()
        self.menu.add.label("2",font_size = self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_stage_2.value, scale=(self.size[0]*0.001,self.size[1]*0.001))
        self.menu.add.button('     next     ', self.stage_game_3, selection_color=Color.BLACK.value,font_size = self.font_size)
        self.menu.add.button('         back         ', self.stage_game_1, selection_color=Color.BLACK.value,font_size = self.font_size)

    # 스테이지 모드 설명 페이지 3
    def stage_game_3(self):
        self.menu.clear()
        self.menu.add.label("3",font_size = self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_stage_3.value, scale=(self.size[0]*0.001,self.size[1]*0.001))
        self.menu.add.button('     next     ', self.stage_game_4, selection_color=Color.BLACK.value,font_size = self.font_size)
        self.menu.add.button('         back         ', self.stage_game_2, selection_color=Color.BLACK.value,font_size = self.font_size)

    # 스테이지 모드 설명 페이지 4
    def stage_game_4(self):
        self.menu.clear()
        self.menu.add.label("4",font_size = self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_stage_4.value, scale=(self.size[0]*0.001,self.size[1]*0.001))
        self.menu.add.button('     next     ', self.stage_game_5, selection_color=Color.BLACK.value,font_size = self.font_size)
        self.menu.add.button('         back         ', self.stage_game_3, selection_color=Color.BLACK.value,font_size = self.font_size)

    # 스테이지 모드 설명 페이지 5
    def stage_game_5(self):
        self.menu.clear()
        self.menu.add.label("5",font_size = self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.image(Images.info_stage_5.value, scale=(self.size[0]*0.001,self.size[1]*0.001))
        self.menu.add.button('     quit     ', self.show, selection_color=Color.BLACK.value,font_size = self.font_size)
        self.menu.add.button('         back         ', self.stage_game_4, selection_color=Color.BLACK.value,font_size = self.font_size)

    # 아이템 설명 페이지
    def items(self):
        self.menu.clear()
        self.menu.add.image(Images.info_items.value, scale=(self.size[0]*0.0008,self.size[1]*0.0008))
        self.menu.add.button('         back         ', self.show, selection_color=Color.BLACK.value,font_size = self.font_size)

    # 조작법 설명 페이지
    def controls(self):
        self.menu.clear()
        self.menu.add.image(Images.info_controls.value, scale=(self.size[0]*0.001,self.size[1]*0.001))
        self.menu.add.button('         back         ', self.show, selection_color=Color.BLACK.value,font_size = self.font_size)

   # 화면 크기 조정 감지 및 비율 고정
    def check_resize(self):
        if (self.size != self.screen.get_size()): #현재 사이즈와 저장된 사이즈 비교 후 다르면 변경
            changed_screen_size = self.screen.get_size() #변경된 사이즈
            ratio_screen_size = (changed_screen_size[0],changed_screen_size[0]*783/720) #y를 x에 비례적으로 계산
            if(ratio_screen_size[0]<320): #최소 x길이 제한
                ratio_screen_size = (494,537)
            if(ratio_screen_size[1]>783): #최대 y길이 제한
                ratio_screen_size = (720,783)
            self.screen = pygame.display.set_mode(ratio_screen_size,
                                                    pygame.RESIZABLE)
            window_size = self.screen.get_size()
            new_w, new_h = 1 * window_size[0], 1 * window_size[1]
            self.menu.resize(new_w, new_h)
            self.menu._current._widgets_surface = make_surface(0,0)
            self.size = window_size
            print(f'New menu size: {self.menu.get_size()}')
            font_size = new_w * 40 //720
            self.font_size = font_size
