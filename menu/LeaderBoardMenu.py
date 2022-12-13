
import pygame
import pygame_menu
from data.Defs import *
from pygame_menu.locals import ALIGN_CENTER, ALIGN_LEFT, ALIGN_RIGHT
from pygame_menu.utils import make_surface
from pygame_menu.widgets.core.widget import Widget
from data.database_user import *

# 리더보드 관련 메뉴
class LeaderBoardMenu:
    def __init__(self,screen):
        title = "랭킹"
        pygame.display.set_caption(title)  # 창의 제목 표시줄 옵션
        self.size = screen.get_size()
        self.screen = screen
        self.font_size = self.size[0] * 38 // 720  # 글씨크기
        self.font_option = self.size[0] * 5//720
        
        self.mytheme = pygame_menu.Theme(
            widget_font=Default.font.value,
            widget_background_color=Color.INDIGO.value,  # 버튼 배경색 설정
            title_font=Default.font.value,
            selection_color= Color.ORANGE.value,  # 선택됐을때 글씨색 설정
            widget_font_color= Color.WHITE.value,  # 기본 글자색
            title_background_color=Color.TRANSPARENT.value,
            title_font_color=Color.TRANSPARENT.value,
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY,
            widget_font_size=self.size[0] * 45 // 720
        )
        main_image = pygame_menu.baseimage.BaseImage(
            image_path=Images.ranking.value, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)  # 메뉴 이미지, Images는 Defs.py에 선언되어 있는 클래스명

        self.mytheme.background_color = main_image

        self.menu = pygame_menu.Menu(
            '', self.size[0], self.size[1], theme=self.mytheme)  # 상단바


        # 페이지화를 위한 변수
        self.tens = 0

    # 메인 메뉴로 돌아가기
    def to_menu(self):
        self.menu.disable()

    def ModeSelectMenu(self):
        import menu.ModeSelectMenu
        game=menu.ModeSelectMenu.ModeSelectMenu(self.screen)

        while True:
            game.show(self.screen)
            pygame.display.flip()  

    # 리더보드 메인 메뉴
    def rank(self):
        self.menu.clear()
        self.menu.add.button('     점수 랭킹     ', self.show_current_score_rank,
                             selection_color=Color.ORANGE.value, font_size=self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.button('     시간 랭킹     ', self.show_current_time_rank,
                             selection_color=Color.ORANGE.value, font_size=self.font_size)
        self.menu.add.vertical_margin(Menus.margin_10.value)
        self.menu.add.button('        이전       ', self.to_menu,
                             selection_color=Color.ORANGE.value, font_size=self.font_size)
        self.menu.mainloop(self.screen,bgfun = self.check_resize)

    def check_resize_main(self):
        if self.check_resize():
            self.rank()

    # score 모드 랭킹 보여주기
    def show_current_score_rank(self):
        self.get_current_rank('score')

    # time 모드 랭킹 보여주기
    def show_current_time_rank(self):
        self.get_current_rank('time')

    # 데이터 베이스에서 랭킹 정보 가져오기
    # mode : (score, time)
    def get_current_rank(self, mode):
            rank = Database()
            self.menu.clear()
            self.tens = 0 # 페이지 변수
            self.ten = 10

            if(mode == 'score'):
                global score_data
                score_data = rank.load_data('score') # 데이터 불러옴
                self.get_current_score_rank_page(self.tens)

            elif(mode == 'time'):
                global time_data
                time_data = rank.load_data('time')
                self.get_current_time_rank_page(self.tens)

    # 페이지화 된 score 모드 랭킹 보여주기
    def get_current_score_rank_page(self, tens):
        self.menu.clear()
        if(len(score_data) == 0): # 데이터가 없는 경우
            self.menu.add.vertical_margin(Menus.margin_100.value)
            self.menu.add.label('No Ranking Information.\nRegister ranking for the update.')
            self.menu.add.vertical_margin(Menus.margin_100.value)
        else:   # 데이터가 있는 경우
            self.menu.add.vertical_margin(Menus.margin_40.value)
            table = self.menu.add.table(table_id='my_table', font_size = self.font_size-self.font_option)
            table.default_cell_padding = Menus.table_padding.value
            table.default_row_background_color = Color.INDIGO.value
            table.add_row(['Rank', 'Nickname', 'Score', 'Date'],
                            cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD, cell_align=pygame_menu.locals.ALIGN_CENTER, cell_border_color=Color.ORANGE.value)
            
            for i in range(10): # 한 페이지에 10개씩 조회 가능
                if(tens*self.ten+i == len(score_data)): break
                name = str(score_data[tens*self.ten+i]['nickname'])
                score = '{0:>05s}'.format(str(score_data[tens*self.ten+i]['score']))
                date = str(score_data[tens*self.ten+i]['date'])
                table.add_row([str(i+1+tens*self.ten), name, score, date], cell_align=pygame_menu.locals.ALIGN_CENTER, cell_border_color=Color.ORANGE.value)

            
            # 페이지 넘김을 위한 버튼 구성
            if(tens == 0):  # 1 페이지 일 때
                if(tens != len(score_data)//self.ten):  # 1 페이지가 마지막 페이지는 아닐 때 # 넘기는 버튼 > 
                    self.menu.add.button('>', self.get_next_score_rank_page,align=ALIGN_RIGHT)
            elif(tens == len(score_data)//self.ten): # 마지막 페이지 일 때
                    self.menu.add.button('<', self.get_prev_score_rank_page,align=ALIGN_LEFT)
                    self.menu.add.label('  ',align=ALIGN_CENTER)
            else:   # 1 페이지도, 마지막 페이지도 아닐 때
                    self.menu.add.button('<', self.get_prev_score_rank_page,align=ALIGN_LEFT)
                    self.menu.add.button('>', self.get_next_score_rank_page,align=ALIGN_RIGHT)
            self.menu.add.vertical_margin(Menus.margin_100.value)
            self.menu.add.button('back', self.rank,font_size = self.font_size)
            self.menu.mainloop(self.screen,bgfun = self.check_resize_score)
   
    def get_current_time_rank_page(self, tens):
        self.menu.clear()
        if(len(time_data) == 0): # 데이터가 없는 경우
            self.menu.add.vertical_margin(Menus.margin_100.value)
            self.menu.add.label('No Ranking Information.\nRegister ranking for the update.')
            self.menu.add.vertical_margin(Menus.margin_100.value)
        else:   # 데이터가 있는 경우
            self.menu.add.vertical_margin(Menus.margin_40.value)
            table = self.menu.add.table(table_id='my_table', font_size = self.font_size-self.font_option)
            table.default_cell_padding = Menus.table_padding.value
            table.default_row_background_color = Color.INDIGO.value
            table.add_row(['Rank', 'Nickname', 'Time', 'Date'],
                            cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD, cell_align=pygame_menu.locals.ALIGN_CENTER, cell_border_color=Color.ORANGE.value)
            
            for i in range(10): # 한 페이지에 10개씩 조회 가능
                if(tens*self.ten+i == len(time_data)): break
                name = str(time_data[tens*self.ten+i]['nickname'])
                time = '{0:>05s}'.format(str(time_data[tens*10+i]['time']))
                date = str(time_data[tens*self.ten+i]['date'])
                table.add_row([str(i+1+tens*self.ten), name, time, date], cell_align=pygame_menu.locals.ALIGN_CENTER, cell_border_color=Color.ORANGE.value)

            # 페이지 넘김을 위한 버튼 구성
            if(tens == 0):  # 1 페이지 일 때
                if(tens != len(time_data)//self.ten):  # 1 페이지가 마지막 페이지는 아닐 때 # 넘기는 버튼 > 
                    self.menu.add.button('>', self.get_next_time_rank_page,align=ALIGN_RIGHT)
            elif(tens == len(time_data)//self.ten): # 마지막 페이지 일 때
                    self.menu.add.button('<', self.get_prev_time_rank_page,align=ALIGN_LEFT)
                    self.menu.add.label('  ',align=ALIGN_CENTER)
            else:   # 1 페이지도, 마지막 페이지도 아닐 때
                    self.menu.add.button('<', self.get_prev_time_rank_page,align=ALIGN_LEFT)
                    self.menu.add.button('>', self.get_next_time_rank_page,align=ALIGN_RIGHT)
            self.menu.add.vertical_margin(Menus.margin_100.value)
            self.menu.add.button('back', self.rank,font_size = self.font_size)
            self.menu.mainloop(self.screen,bgfun = self.check_resize_score)

    def check_resize_score(self):
        if self.check_resize() :
            self.get_current_score_rank_page(self.tens)
    
    def check_resize_time(self):
        if self.check_resize() :
            self.get_current_time_rank_page(self.tens)

    # score 모드 랭킹에서 다음 페이지 보기
    def get_next_score_rank_page(self):
        self.tens += 1
        self.get_current_score_rank_page(self.tens)

    def get_next_time_rank_page(self):
        self.tens += 1
        self.get_current_time_rank_page(self.tens)

    # score 모드 랭킹에서 이전 페이지 보기
    def get_prev_score_rank_page(self):
        self.tens -= 1
        self.get_current_score_rank_page(self.tens)

    def get_prev_time_rank_page(self):
        self.tens -= 1
        self.get_current_time_rank_page(self.tens)


    def check_resize_time(self):
        if self.check_resize():
            self.get_current_time_rank_page(self.tens)

    # time 모드 랭킹에서 다음 페이지 보기
    def get_next_time_rank_page(self):
        self.tens += 1
        self.get_current_time_rank_page(self.tens)

    # time 모드 랭킹에서 다음 페이지 보기
    def get_prev_time_rank_page(self):
        self.tens -= 1
        self.get_current_time_rank_page(self.tens)

    
    # 화면 크기 조정 감지 및 비율 고정
    def check_resize(self):
        if (self.size != self.screen.get_size()): #현재 사이즈와 저장된 사이즈 비교 후 다르면 변경
            changed_screen_size = self.screen.get_size() #변경된 사이즈
            ratio_screen_size = (changed_screen_size[0],changed_screen_size[0]*sizescale.maxiset.value/sizescale.maxi.value) #y를 x에 비례적으로 계산
            if(ratio_screen_size[0]<sizescale.mini.value): #최소 x길이 제한
                ratio_screen_size = (sizescale.mini.value, sizescale.miniset.value)
            if(ratio_screen_size[1]>sizescale.maxi.value): #최대 y길이 제한
                ratio_screen_size = (sizescale.maxi.value, sizescale.maxiset.value)
            self.screen = pygame.display.set_mode(ratio_screen_size,
                                                    pygame.RESIZABLE)
            window_size = self.screen.get_size()
            new_w, new_h = 1 * window_size[0], 1 * window_size[1]
            self.menu.resize(new_w, new_h)
            self.menu._current._widgets_surface = make_surface(0,0)
            self.size = window_size
            print(f'New menu size: {self.menu.get_size()}')
            font_size = new_w * 40 //720
            font_option = new_w * 5//720
            self.font_size = font_size
            self.font_option = font_option
            return True 
