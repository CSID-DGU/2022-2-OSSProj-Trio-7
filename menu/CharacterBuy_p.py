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
        self.font_size = self.size[0] * 38 // 720
        self.character = character
        self.margin75 = 0.75

        self.charlock_theme = pygame_menu.Theme(
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


        if(character == 'police1'):
            self.menu_image = pygame_menu.baseimage.BaseImage(image_path=Images.failbuy_police1.value,drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
        elif(character == 'police2'):
             self.menu_image = pygame_menu.baseimage.BaseImage(image_path=Images.failbuy_police2.value,drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
        self.charlock_theme.background_color = self.menu_image
        self.menu = pygame_menu.Menu('', self.size[0], self.size[1],
                            theme=self.charlock_theme)

    def show(self):     
        self.menu.add.vertical_margin(self.size[0]*self.margin75)
        self.menu.add.button('         상점으로 돌아가기         ',self.back_from_locked,
                             selection_color=Color.ORANGE.value, font_size=self.font_size)
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
            if(ratio_screen_size[0]<sizescale.mini.value): #최소 x길이 제한
                ratio_screen_size = (sizescale.mini.value, sizescale.miniset.value)
            if(ratio_screen_size[1]>sizescale.maxi.value): #최대 y길이 제한
                ratio_screen_size = (sizescale.maxi.value, sizescale.maxiset.value)
            self.screen = pygame.display.set_mode(ratio_screen_size,
                                                    pygame.RESIZABLE)
            window_size = self.screen.get_size()
            new_w, new_h = 1 * window_size[0], 1 * window_size[1]
            self.menu.resize(new_w, new_h)
            self.size = window_size
            self.menu._current._widgets_surface = make_surface(0,0)
