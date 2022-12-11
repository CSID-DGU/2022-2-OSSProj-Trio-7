import pygame
import pygame_menu
from data.Defs import *
from pygame_menu.locals import ALIGN_CENTER, ALIGN_LEFT, ALIGN_RIGHT
from pygame_menu.utils import make_surface
from pygame_menu.widgets.core.widget import Widget

class JobInfo:
    def __init__(self, screen):
        infoObject = pygame.display.Info()
        title = "직업 소개"
        pygame.display.set_caption(title)  # 창의 제목 표시줄 옵션
        
        self.size = screen.get_size()
        self.screen = screen
        self.changed_screen_size = self.screen.get_size()
        self.board_width = self.changed_screen_size[0]  # x
        self.board_height = self.changed_screen_size[1]  # y

        JobInfo_image = pygame_menu.baseimage.BaseImage(
            image_path=Images.JobInfo.value, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)  # 메뉴 이미지, Images는 Defs.py에 선언되어 있는 클래스명
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

        self.mytheme.background_color = JobInfo_image

        self.menu = pygame_menu.Menu(
            '', self.size[0], self.size[1], theme=self.mytheme)  # 상단바
        self.first_page()
        self.menu.mainloop(self.screen, bgfun=self.check_resize)

    def show(self, screen):
        self.check_resize(screen)
        screen.fill((255, 255, 255))  # 배경 나중에 바꾸기.
        
    def returnPage(self):
        from menu.CharacterSelectMenu import CharacterSelect
        game = CharacterSelect(self.screen)

        while True:
            game.show(self.screen)
            pygame.display.flip()

    def first_page(self):
        self.menu.clear()
        self.menu.add.vertical_margin(300)

        b1 = self.menu.add.button('   직업을 선택하러 가볼까요?   ', self.returnPage)

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
            self.menu._current._widgets_surface = make_surface(0, 0)
            self.size = window_size
            print(f'New menu size: {self.menu.get_size()}')
            font_size = new_w * 40 // 720
            self.font_size = font_size