import pygame
import pygame_menu
from data.CharacterDataManager import *
from data.Defs import *
from data.StageDataManager import *
from menu.CharacterStoreMenu_p import *
from menu.CharacterStoreMenu_f import *
from menu.CharacterStoreMenu_d import *

#Mypage에서 잠긴 캐릭터 SELECT할 시 보여주는 창
class CharacterBuy_p:
    def __init__(self,screen,character):
        self.size = screen.get_size()
        self.screen = screen
        self.orange_color = (253, 111, 34)
        self.font_size = self.size[0] * 38 // 720
        self.character = character

        self.charlock_theme = pygame_menu.Theme(
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

        '''
        self.charlock_theme =  pygame_menu.Theme(
            widget_font = pygame_menu.font.FONT_BEBAS,
            widget_background_color = (150, 213, 252), #버튼 가독성 올리기 위해서 버튼 배경색 설정 : 하늘색
            title_font = pygame_menu.font.FONT_BEBAS,
            selection_color = (0,0,0), #선택됐을때 글씨색 설정
            widget_font_color = (255,255,255), #글씨색 설정
            title_background_color = (0,100,162),
            title_font_color = (255,255,255),
            title_bar_style = pygame_menu.pygame_menu.widgets.MENUBAR_STYLE_NONE,
            widget_font_size = self.size[0] * 30 //720)

        '''

        if(character == 'police1'):
            self.menu_image = pygame_menu.baseimage.BaseImage(image_path=Images.failbuy_police1.value,drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
        elif(character == 'police2'):
             self.menu_image = pygame_menu.baseimage.BaseImage(image_path=Images.failbuy_police2.value,drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
        self.charlock_theme.background_color = self.menu_image
        self.menu = pygame_menu.Menu('', self.size[0], self.size[1],
                            theme=self.charlock_theme)

    def show(self):     
        print(self.size[0])
        self.menu.add.vertical_margin(self.size[0]*0.75)
        self.menu.add.button('         상점으로 돌아가기         ',self.back_from_locked,
                             selection_color=self.orange_color, font_size=self.font_size)
        # self.menu.add.button('back', self.back_from_locked)
        self.menu.mainloop(self.screen,bgfun = self.check_resize)
        CharacterStoreMenu_p.buy_character()
        
    
    def back_from_locked(self):
        self.menu.clear()
        CharacterStoreMenu_p(self.screen,self.character).show()

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
            self.size = window_size
            self.menu._current._widgets_surface = make_surface(0,0)
            print(f'New menu size: {self.menu.get_size()}')
