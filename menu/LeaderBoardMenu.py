
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
        self.size = screen.get_size()
        self.screen = screen
        self.font_size = self.size[0] * 40//720
        self.font_option = self.size[0] * 5//720
        self.mytheme = pygame_menu.themes.THEME_DEFAULT.copy()
        self.mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
        self.mytheme.title_close_button_cursor = pygame_menu.locals.CURSOR_HAND
        self.mytheme.title_font_color = Color.WHITE.value
        self.mytheme.title_font = pygame_menu.font.FONT_BEBAS
        self.mytheme.widget_font_size = self.font_size
        self.mytheme.title_background_color = (0,100,162)
        self.mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL
        self.mytheme.widget_font = pygame_menu.font.FONT_BEBAS

        
        self.menu = pygame_menu.Menu('Rank', self.size[0], self.size[1],
                            theme=self.mytheme)


        # 페이지화를 위한 변수
        self.tens = 0

    # 메인 메뉴로 돌아가기
    def to_menu(self):
        self.menu.disable()

    def gameselectmenu(self):
        import menu.gameselectMenu
        game=menu.gameselectMenu.GameselectMenu(self.screen)

        while True:
            game.show(self.screen)
            pygame.display.flip()  

    # 리더보드 메인 메뉴
    def rank(self):
        self.menu.clear()
        self.menu.add.button('     easy mode     ', self.show_current_easy_rank,font_size = self.font_size)
        self.menu.add.button('     hard mode     ', self.show_current_hard_rank,font_size = self.font_size)
        #self.menu.add.button('     rank search     ', self.show_current_rank_search)
        self.menu.add.button('         back         ', self.to_menu,font_size = self.font_size)
        self.menu.mainloop(self.screen,bgfun = self.check_resize)

    def check_resize_main(self):
        if self.check_resize():
            self.rank()

    # 이번 달 easy 모드 랭킹 보여주기
    def show_current_easy_rank(self):
        self.get_current_rank('easy')

    # 이번 달 hard 모드 랭킹 보여주기
    def show_current_hard_rank(self):
        self.get_current_rank('hard')

    # 데이터 베이스에서 이번 달 랭킹 정보 가져오기
    # mode : 난이도 (easy, hard)
    def get_current_rank(self, mode):
            rank = Database()
            self.menu.clear()
            self.tens = 0 # 페이지 변수

            if(mode == 'easy'):
                global easy_data
                easy_data = rank.load_data('easy') # 데이터 불러옴
                self.get_current_easy_rank_page(self.tens)

            elif(mode == 'hard'):
                global hard_data
                hard_data = rank.load_data('hard')
                self.get_current_hard_rank_page(self.tens)

    # 페이지화 된 이번 달 easy 모드 랭킹 보여주기
    def get_current_easy_rank_page(self, tens):
        self.menu.clear()
        self.menu.add.label("--Easy Rank--",selectable=False,font_size = self.font_size+self.font_option)
        if(len(easy_data) == 0): # 데이터가 없는 경우
            self.menu.add.vertical_margin(Menus.margin_100.value)
            self.menu.add.label('No Ranking Information.\nRegister ranking for the update.')
            self.menu.add.vertical_margin(Menus.margin_100.value)
        else:   # 데이터가 있는 경우
            self.menu.add.vertical_margin(Menus.margin_40.value)
            table = self.menu.add.table(table_id='my_table', font_size = self.font_size-self.font_option)
            table.default_cell_padding = Menus.table_padding.value
            table.default_row_background_color = Color.GRAY.value
            table.add_row(['Rank', 'ID', 'Score', 'Date'],
                            cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD, cell_align=pygame_menu.locals.ALIGN_CENTER, cell_border_color=Color.GRAY.value)
            
            for i in range(10): # 한 페이지에 10개씩 조회 가능
                if(tens*10+i == len(easy_data)): break
                name = str(easy_data[tens*10+i]['ID'])
                score = '{0:>05s}'.format(str(easy_data[tens*10+i]['score']))
                date = str(easy_data[tens*10+i]['date'])
                table.add_row([str(i+1+tens*10), name, score, date], cell_align=pygame_menu.locals.ALIGN_CENTER, cell_border_color=Color.GRAY.value)
            prev_next_frame = self.menu.add.frame_h(300, 60) # 가로 300, 세로 60의 프레임 생성
            # 페이지 넘김을 위한 버튼 구성
            if(tens == 0):  # 1 페이지 일 때
                prev_next_frame.pack(self.menu.add.label('  '),align=ALIGN_CENTER)
                prev_next_frame.pack(self.menu.add.horizontal_margin(Menus.margin_200.value),align=ALIGN_CENTER)
                if(tens != len(easy_data)//10):  # 1 페이지가 마지막 페이지는 아닐 때 # 넘기는 버튼 > 
                    prev_next_frame.pack(self.menu.add.button('>', self.get_next_easy_rank_page),align=ALIGN_CENTER)
            elif(tens == len(easy_data)//10): # 마지막 페이지 일 때
                prev_next_frame.pack(self.menu.add.button('<', self.get_prev_easy_rank_page),align=ALIGN_CENTER)
                prev_next_frame.pack(self.menu.add.horizontal_margin(Menus.margin_200.value),align=ALIGN_CENTER)
                prev_next_frame.pack(self.menu.add.label('  '),align=ALIGN_CENTER)
            else:   # 1 페이지도, 마지막 페이지도 아닐 때
                prev_next_frame.pack(self.menu.add.button('<', self.get_prev_easy_rank_page),align=ALIGN_CENTER)
                prev_next_frame.pack(self.menu.add.horizontal_margin(Menus.margin_200.value),align=ALIGN_CENTER)
                prev_next_frame.pack(self.menu.add.button('>', self.get_next_easy_rank_page),align=ALIGN_CENTER)
        self.menu.add.button('back', self.rank,font_size = self.font_size)
        self.menu.mainloop(self.screen,bgfun = self.check_resize_easy)
    
    def check_resize_easy(self):
        if self.check_resize() :
            #self.menu.disable()
            self.get_current_easy_rank_page(self.tens)

    # 이번 달 easy 모드 랭킹에서 다음 페이지 보기
    def get_next_easy_rank_page(self):
        self.tens += 1
        self.get_current_easy_rank_page(self.tens)

    # 이번 달 easy 모드 랭킹에서 이전 페이지 보기
    def get_prev_easy_rank_page(self):
        self.tens -= 1
        self.get_current_easy_rank_page(self.tens)

    # 페이지화 된 이번 달 hard 모드 랭킹 보여주기
    def get_current_hard_rank_page(self, tens):
        self.menu.clear()
        self.menu.add.label("--Hard Rank--",selectable=False,font_size = self.font_size+self.font_option)
        if(len(hard_data) == 0): # 데이터가 없는 경우
            self.menu.add.vertical_margin(Menus.margin_100.value)
            self.menu.add.label('No Ranking Information.\nRegister ranking for the update.')
            self.menu.add.vertical_margin(Menus.margin_100.value)
        else:   # 데이터가 있는 경우
            self.menu.add.vertical_margin(Menus.margin_40.value)
            table = self.menu.add.table(table_id='my_table', font_size=self.font_size-self.font_option)
            table.default_cell_padding = Menus.table_padding.value
            table.default_row_background_color = Color.GRAY.value
            table.add_row(['Rank', 'ID', 'Score', 'Date'],
                            cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD, cell_align=pygame_menu.locals.ALIGN_CENTER, cell_border_color=Color.GRAY.value)
          
            for i in range(10): # 한 페이지에 10개씩 조회 가능
                if(tens*10+i == len(hard_data)): break
                name = str(hard_data[tens*10+i]['ID'])
                score = '{0:>05s}'.format(str(hard_data[tens*10+i]['score']))
                date = str(hard_data[tens*10+i]['date'])
                table.add_row([str(i+1+tens*10), name, score, date], cell_align=pygame_menu.locals.ALIGN_CENTER, cell_border_color=Color.GRAY.value)
            prev_next_frame = self.menu.add.frame_h(300, 60) # 가로 300, 세로 60의 프레임 생성
            # 페이지 넘김을 위한 버튼 구성
            if(tens == 0):   # 1 페이지 일 때
                prev_next_frame.pack(self.menu.add.label('  '),align=ALIGN_CENTER)
                prev_next_frame.pack(self.menu.add.horizontal_margin(Menus.margin_200.value),align=ALIGN_CENTER)
                if(tens != len(hard_data)//10): # 1 페이지가 마지막 페이지는 아닐 때
                    prev_next_frame.pack(self.menu.add.button('>', self.get_next_hard_rank_page),align=ALIGN_CENTER)
            elif(tens == len(hard_data)//10):   # 마지막 페이지 일 때
                prev_next_frame.pack(self.menu.add.button('<', self.get_prev_hard_rank_page),align=ALIGN_CENTER)
                prev_next_frame.pack(self.menu.add.horizontal_margin(Menus.margin_200.value),align=ALIGN_CENTER)
                prev_next_frame.pack(self.menu.add.label('  '),align=ALIGN_CENTER)
            else:   # 1 페이지도, 마지막 페이지도 아닐 때
                prev_next_frame.pack(self.menu.add.button('<', self.get_prev_hard_rank_page),align=ALIGN_CENTER)
                prev_next_frame.pack(self.menu.add.horizontal_margin(Menus.margin_200.value),align=ALIGN_CENTER)
                prev_next_frame.pack(self.menu.add.button('>', self.get_next_hard_rank_page),align=ALIGN_CENTER)
        self.menu.add.button('back', self.rank, font_size = self.font_size)
        self.menu.mainloop(self.screen,bgfun = self.check_resize_hard)

    def check_resize_hard(self):
        if self.check_resize():
            self.get_current_hard_rank_page(self.tens)

    # 이번 달 hard 모드 랭킹에서 다음 페이지 보기
    def get_next_hard_rank_page(self):
        self.tens += 1
        self.get_current_hard_rank_page(self.tens)

    # 이번 달 hard 모드 랭킹에서 다음 페이지 보기
    def get_prev_hard_rank_page(self):
        self.tens -= 1
        self.get_current_hard_rank_page(self.tens)

    
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
            #font_size = new_w * 30//720
            #self.mytheme.widget_font_size = font_size  
            font_size = new_w * 40 //720
            font_option = new_w * 5//720
            self.font_size = font_size
            self.font_option = font_option
            #self.scale = (new_w*0.00015,new_h*0.00015)
            return True 
