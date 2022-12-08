from collections import OrderedDict
from datetime import datetime
from os import system
from turtle import color
#from menu.DifficultySelectMenu import *
import pygame
import pygame_menu
from data.database_user import *
from data.Defs import *
from data.Defs import User
from menu.CharacterSelectMenu import CharacterSelect
from menu.gameselectMenu import *
from game.TutorialGame import *


class Display:
    w_init = 1/3
    h_init = 8/12
    angle = 0
    help_scale = (0.4, 0.4)


class Utillization:
    x = 0
    y = 1


class Login:
    def __init__(self, screen):
        self.database = Database()
        # 1. 게임초기화

        pygame.init()

        # 2. 게임창 옵션 설정
        infoObject = pygame.display.Info()

        self.size = [infoObject.current_w, infoObject.current_h]
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)

        main_image = pygame_menu.baseimage.BaseImage(
            image_path=Images.main.value, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)  # 메뉴 이미지, Images는 Defs.py에 선언되어 있는 클래스명
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

        self.mytheme.background_color = main_image

        # pvp 관련
        self.pvpcharacter_data = PvpCharacterDataManager.load()  # pvp 캐릭터 데이터
        self.mode = ("score", InfiniteGame.ScoreMode())
        self.changed_screen_size = self.screen.get_size()
        self.board_width = self.changed_screen_size[0]  # x
        self.board_height = self.changed_screen_size[1]  # y

        # main bgm
        self.background_music = "./Sound/bgm/bgm_main.mp3"
        pygame.mixer.init()
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

        # 상단바
        self.menu = pygame_menu.Menu(
            '', self.size[0], self.size[1], theme=self.mytheme)
        self.first_page()
        self.menu.mainloop(self.screen, bgfun=self.check_resize)

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
            font_size = new_w * 30 // 720
            self.mytheme.widget_font_size = font_size
            print(f'font_size: {font_size}')
            self.menu.resize(new_w, new_h)
            self.size = window_size
            self.menu._current._widgets_surface = make_surface(0, 0)
            print(f'New menu size: {self.menu.get_size()}')
            pygame.display.flip()
            return True
        return False

    def first_page(self):  # 첫화면
        self.menu.clear()
        b1 = self.menu.add.button('  회원가입  ', self.show_signup)
        self.menu.add.vertical_margin(10)
        b2 = self.menu.add.button('   로그인   ', self.login_page)
        self.menu.add.vertical_margin(10)
        b3 = self.menu.add.button(' 튜토리얼 ', self.tutorial_page)
        self.menu.add.vertical_margin(10)
        b4 = self.menu.add.button('     종료     ', pygame_menu.events.EXIT)

    def login_page(self):  # 로그인 페이지
        self.menu.clear()
        self.menu.add.text_input('아이디 : ', maxchar=100, onchange=self.get_id)
        self.menu.add.vertical_margin(10)
        self.menu.add.text_input(
            '비밀번호 : ', maxchar=100, onchange=self.get_pw, password=True, password_char='*')
        self.menu.add.vertical_margin(10)
        b1 = self.menu.add.button('  로그인  ', self.login)
        self.menu.add.vertical_margin(10)
        b2 = self.menu.add.button('  이전 화면  ', self.first_page)
        self.menu.add.vertical_margin(10)
        b3 = self.menu.add.button('  게임 종료  ', pygame_menu.events.EXIT)

    def login(self):
        if self.id:
            if self.database.id_not_exists(self.id) is False:
                if self.password and self.database.match_idpw(self.id, self.password):
                    print("로그인 성공")
                    print(self.id)
                    User.user_id = self.id
                    User.coin = self.database.show_mycoin()
                    self.login_success()

                else:
                    print("비밀번호 틀림")
                    self.password_fail()

            else:
                print("로그인 실패")
                self.login_fail()

        else:
            self.login_page()

    def password_fail(self):
        self.menu.clear()
        self.menu.add.vertical_margin(10)
        self.menu.add.label("비밀번호 불일치", selectable=False)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('  이전 화면  ', self.login_page)

    def login_fail(self):
        self.menu.clear()
        self.menu.add.vertical_margin(10)
        self.menu.add.label("아이디 없음", selectable=False)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('  이전 화면  ', self.login_page)

    # 아이디 입력값으로 변경
    def get_id(self, value):
        self.id = value

    # 비밀번호 입력값으로 변경
    def get_pw(self, value):
        self.password = value

    # 닉네임 입력값으로 변경
    def get_nickname(self, value):
        self.nickname = value

    def save_id(self, value):  # 아이디 데이터베이스에 저장
        self.id = value
        print("출력:", value)
        if self.database.id_not_exists(self.id):  # id가 데이터베이수애 존재하지않으면
            self.database.add_id(self.id)  # 데이터베이스에 저장(회원가입)
        else:
            self.signup_fail()

    def save_password(self, value):  # 비밀번호 데이터베이스에 저장
        self.password = value
        self.database.add_pw(self.password, self.id)

    def save_nickname(self, value):
        self.nickname = value
        self.database.add_ninkname(self.nickname, self.id)

    def show_signup(self):
        self.menu.clear()
        self.menu.add.text_input('아이디 : ', maxchar=15, onreturn=self.save_id)
        self.menu.add.vertical_margin(10)
        self.menu.add.text_input(
            '비밀번호 : ', maxchar=50, onreturn=self.save_password, password=True, password_char='*')
        self.menu.add.vertical_margin(10)
        self.menu.add.text_input(
            '닉네임 : ', maxchar=15, onreturn=self.save_nickname)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('  회원가입  ', self.login_page)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('  이전 화면  ', self.first_page)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('  게임 종료   ', pygame_menu.events.EXIT)

    def login_success(self):
        game = CharacterSelect(self.screen)
    
        while True:
            game.show(self.screen)
            pygame.display.flip()

    def signup_fail(self):
        self.menu.clear()
        self.menu.add.vertical_margin(10)
        self.menu.add.label("  이미 존재하는 아이디   ", selectable=False)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('  이전 화면  ', self.show_signup)

    def tutorial_page(self):
        tutorialgame = tutorial(self.pvpcharacter_data, self.pvpcharacter_data[0], self.mode)
        tutorialgame.tutorial_info()

    def main(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.VIDEORESIZE:
                    pass

            # 화면에 메뉴 그리기
            screen.fill(Color.WHITE.value)
            login.menu.update(events)
            login.menu.draw(screen)
            pygame.display.flip()  # 화면 계속 업데이트


if __name__ == '__main__':
    pygame.init()
    infoObject = pygame.display.Info()
    size = [int(infoObject.current_w*Display.w_init),
            int(infoObject.current_h*Display.h_init)]  # 사이즈 설정(w,h)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)  # 창크기 조정 가능
    ww, wh = pygame.display.get_surface().get_size()
    Default.game.value["size"]["x"] = size[0]  # Default는 Defs.py에 선언되어 있는 클래스명
    Default.game.value["size"]["y"] = size[1]
    login = Login(screen)
