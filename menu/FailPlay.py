

import pygame
import pygame_menu
from data.CharacterDataManager import *
from data.Defs import *
from data.StageDataManager import *
from menu.MypageMenu import *

#Mypage에서 잠긴 캐릭터 SELECT할 시 보여주는 창
class FailPlay:
    def __init__(self,screen):
        self.size = screen.get_size()
        self.screen = screen
        self.failplay_theme =  pygame_menu.Theme(
            title_font = pygame_menu.font.FONT_BEBAS,
            widget_font = pygame_menu.font.FONT_FIRACODE,
            selection_color = (255,255,255), #선택됐을때 글씨색 설정
            widget_font_color = (255,255,255), #글씨색 설정
            title_background_color = (0,100,162),
            #title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL
            background_color = (0,0,0)
        )
        self.menu = pygame_menu.Menu('Cannot Play!', self.size[0], self.size[1],
                            theme=self.failplay_theme)

    def show(self):        
        self.menu.add.label("Can't play Game!")
        self.menu.add.label("Selected Character is locked!")
        self.menu.add.label("Select your character again!")
        self.failplay_theme.widget_background_color = (150, 213, 252)
        self.menu.add.button('Go to Mypage', self.go_to_mypage)
        self.menu.mainloop(self.screen,bgfun = self.check_resize)
        
    
    def go_to_mypage(self):
        self.menu.clear()
        Mypage(self.screen).show()

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

    def unlock_character(self):
        import data.database_user
        database =  data.database_user.Database()
        price= [0,10,10,20]
        curs =database.dct_db.cursor()
        self.id = User.user_id
        sql = "SELECT user_id,char2,char3,char4,user_coin FROM users2 WHERE user_id=%s" #user_id와 user_coin열만 선택
        curs.execute(sql,self.id) 
        data = curs.fetchone()  
        self.coin = data[4]
        if self.character == "Merry":
            selected_idx = 1
        if self.character == "Haengal":
            selected_idx = 2
        if self.character == "Kongchi":
            selected_idx = 3
        #print(selected_idx)
        if(data[4] >= price[selected_idx]):
            print("잠금을 해제합니다.")
            if self.character == "Merry":
                User.coin = self.coin-10
                sql = "UPDATE users2 SET char2=%s WHERE user_id = %s"
                curs.execute(sql, (5, self.id))
                sql = "UPDATE users2 SET user_coin=%s WHERE user_id = %s"
                curs.execute(sql, (self.coin-10, self.id))
                database.dct_db.commit()
                User.cat_lock[1] = False
                database.char_lock()                
                

            if self.character == "Haengal":
                User.coin = self.coin-10
                sql = "UPDATE users2 SET char3=%s WHERE user_id = %s"
                curs.execute(sql, (5, self.id))
                sql = "UPDATE users2 SET user_coin=%s WHERE user_id = %s"
                curs.execute(sql, (self.coin-10, self.id))
                database.dct_db.commit()
                User.cat_lock[2] = False
                database.char_lock()       

            if self.character == "Kongchi":
                User.coin = self.coin-20
                sql = "UPDATE users2 SET char4=%s WHERE user_id = %s"
                curs.execute(sql, (5, self.id))
                sql = "UPDATE users2 SET user_coin=%s WHERE user_id = %s"
                curs.execute(sql, (self.coin-20, self.id))
                database.dct_db.commit()
                User.cat_lock[3] = False
                database.char_lock()       
 
            
        else:
            print("코인이 부족하여 구매가 불가능합니다.")
        curs.close()
