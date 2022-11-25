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

        self.menu = pygame_menu.Menu(
            '직업 슈팅 게임', self.size[0], self.size[1], theme=self.mytheme)  # 상단바
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
            self.menu.resize(new_w, new_h)
            self.size = window_size
            self.menu._current._widgets_surface = make_surface(0, 0)
            print(f'New menu size: {self.menu.get_size()}')

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
        # login.mytheme.widget_background_color = (0,0,0,0) #투명 배경
        self.menu.add.text_input('ID : ', maxchar=100, onchange=self.get_id)
        self.menu.add.text_input(
            'PASSWORD : ', maxchar=100, onchange=self.get_pw, password=True, password_char='*')
        self.menu.add.text_input(
            'NICKNAME : ', maxchar=100, onchange=self.get_nickname)
        b1 = self.menu.add.button('  Login  ', self.login)
        b2 = self.menu.add.button('  Back  ', self.first_page)
        b3 = self.menu.add.button('  Quit  ', pygame_menu.events.EXIT)

        #mytheme.widget_background_color = (150, 213, 252)

    def login(self):
        if self.id:
            if self.database.id_not_exists(self.id) is False:
                if self.password and self.database.match_idpw(self.id, self.password):
                    print("로그인 성공")
                    print(self.id)
                    User.user_id = self.id
                    User.user_nickname = self.nickname
                    User.coin = self.database.show_mycoin()
                    # Database().dchar_lock()
                    self.login_success()

                else:
                    print("비밀번호 틀림")
                    self.password_fail()

            else:
                print("로그인 실패")
                self.login_fail()

        else:
            print("이건뭘까")
            self.login_page()

    def password_fail(self):
        self.menu.clear()
        self.menu.add.vertical_margin(10)
        self.menu.add.label("ID or Password Incorrect", selectable=False)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('  back  ', self.login_page)

    def login_fail(self):
        self.menu.clear()
        self.menu.add.vertical_margin(10)
        self.menu.add.label("ID or Password Incorrect", selectable=False)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('  back  ', self.login_page)

    # 아이디 input값으로 변경

    def get_id(self, value):
        self.id = value

    # 비밀번호 입력값으로 변경
    def get_pw(self, value):
        self.password = value

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
        # mytheme.widget_background_color = (0,0,0,0) #투명 배경
        # 현재의 문제점 : enter를 눌러야만 저장됨.
        self.menu.add.text_input('ID : ', maxchar=15, onreturn=self.save_id)
        self.menu.add.text_input(
            'PASSWORD : ', maxchar=50, onreturn=self.save_password, password=True, password_char='*')
        self.menu.add.text_input(
            'NICKNAME : ', maxchar=15, onreturn=self.save_nickname)
        self.menu.add.button('  Sign Up  ', self.login_page)
        self.menu.add.button('  back  ', self.first_page)
        self.menu.add.button('  Quit   ', pygame_menu.events.EXIT)

    def login_success(self):
        # Main(screen).show()
        game = CharacterSelect(self.screen)
    
        while True:
            game.show(self.screen)
            pygame.display.flip()

    def signup_fail(self):
        self.menu.clear()
        self.menu.add.vertical_margin(10)
        self.menu.add.label("    ID Already Exists     ", selectable=False)
        self.menu.add.vertical_margin(10)
        self.menu.add.button('  back  ', self.show_signup)

    def tutorial_page(self):  # 2인 플레이어
        print(self.pvpcharacter_data[2].name)
        pvpgame = tutorial(self.pvpcharacter_data,
                           self.pvpcharacter_data[0], self.mode)
        pvpgame.pvp_info()

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
            screen.fill((25, 0, 50))  # 값 변경해보고 지워봤는데 큰 변화 없음. 없어도 되는 기능인듯?

            login.menu.update(events)
            login.menu.draw(screen)
            # pygame.draw.rect(screen,color,input_rect,2)

            pygame.display.flip()  # 화면이 계속 업데이트 될 수 있도록 설정


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
