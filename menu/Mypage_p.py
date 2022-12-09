

from select import select
import pygame
import pygame_menu
from data.CharacterDataManager import *
from data.Defs import *
from data.Stage import Stage
from data.StageDataManager import *
from data.database_user import Database
from game.InfiniteGame import *
from pygame_menu.locals import ALIGN_RIGHT
from pygame_menu.utils import make_surface
from data.StoreDataManager import *

# 캐릭터 선택 메뉴
class Mypage_p:
    image_widget: 'pygame_menu.widgets.Image'
    item_description_widget: 'pygame_menu.widgets.Label'

    def __init__(self,screen):
        title = "마이 페이지"
        pygame.display.set_caption(title)  # 창의 제목 표시줄 옵션
        # 화면 받고 화면 크기 값 받기
        self.screen = screen
        self.size = screen.get_size()
        self.font_size = self.size[0] * 25 //720
        #menu_image = pygame_menu.baseimage.BaseImage(image_path='./Image/Login.png',drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
        self.mytheme = pygame_menu.themes.THEME_ORANGE.copy()
        #mytheme.widget_font = pygame_menu.font.FONT_8BIT
        #mytheme.widget_background_color = (150, 213, 252) #버튼 가독성 올리기 위해서 버튼 배경색 설정 : 하늘색
        self.mytheme.title_font = pygame_menu.font.FONT_BEBAS
        self.mytheme.selection_color = (0,0,0) #선택됐을때 글씨색 설정
        self.mytheme.widget_font_color = (0,0,0) #글씨색 설정
        self.mytheme.title_background_color = (253, 111, 34) #주황색 
        self.mytheme.title_font_color = (0,10,63) # 남색
        self.mytheme.widget_font = pygame_menu.font.FONT_BEBAS
        #self.mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL
        self.mytheme.background_color = (255,255,255)
        self.mytheme.widget_font_size = self.font_size
        self.menu = pygame_menu.Menu('My Page', self.size[0], self.size[1],
                            theme=self.mytheme)


        #캐릭터 데이터를 json에서 불러온다
        self.character_data = CharacterDataManager.load()

        self.show(character='police')
        self.menu.mainloop(self.screen,bgfun = self.check_resize)
        
           

    def to_menu(self):
        import menu.gameselectMenu
        game=menu.gameselectMenu.GameselectMenu(self.screen)

        while True:
            game.show(self.screen, 'police')
            pygame.display.flip()

    #메뉴 구성하고 보이기
    def show(self, character):
        choosed_chracter = character 
        self.db = Database()
        self.nickname = self.db.get_nickname() 
        # Database().char_lock()  
        self.menu.add.label("My ID : %s "%User.user_id)
        self.menu.add.label("My NICKNAME : %s "%self.db.get_nickname())
        Database().my_score_rank()
        Database().my_time_rank()
        User.coin = Database().show_mycoin()
        self.menu.add.label("Best Score : %s"%User.score_score)
        self.menu.add.label("Best Time : %s"%User.time_score)
        self.menu.add.label("My coin : %d "%User.coin)
        #캐릭터 선택 메뉴 구성
        if choosed_chracter == "police":
            Database().pchar_lock()
            pcharacters = [] #보유하고 있는 캐릭터 이름만 저장하는 리스트

            curs = Database().dct_db.cursor()
            self.id = User.user_id
            sql = "SELECT user_id,pchar1,pchar2,pchar3 FROM tusers2 WHERE user_id=%s" #user_id와 user_character열만 선택
            curs.execute(sql,self.id) 
            data = curs.fetchone()  
            curs.close()

            self.pcharacter_data = StoreDataManager.load("police")
            front_image_path = [Images.police.value,Images.police1.value, Images.police2.value]
            self.pcharacter_imgs = [] #보유하고 있는 이미지만 들어 있는 파일
            self.pcharacter_imgs2 = [] #전체 이미지 들어 있는 파일
            for i in range(1,4):
                pchar = data[i]
                
                if(pchar > -1): 
                    default_image = pygame_menu.BaseImage(
                    image_path=front_image_path[i-1]
                    ).scale(0.5, 0.5)
                    #print("이미지경로",front_image_path[i-1])
                    pcharacters.append((self.pcharacter_data[i-1].name, i-1)) #보유하고 있는 캐릭터 이름만 저장
                    self.pcharacter_imgs.append(default_image.copy()) #보유하고 있는 캐릭터만 배열에 이미지 저장

            for i in range(3): 
                    default_image = pygame_menu.BaseImage(
                    image_path=front_image_path[i]
                    ).scale(0.3, 0.3)
        
                    self.pcharacter_imgs2.append(default_image.copy())
            #print(self.price)    
            #print("이미지리스트",self.character_imgs)
            self.pcharacter_selector = self.menu.add.selector(
                title='Character :\t',
                items=pcharacters,
                onchange=self.on_selector_change #이미지 수정 코드
            )
            self.image_widget = self.menu.add.image(
                image_path=self.pcharacter_imgs[0],
                padding=(25, 0, 0, 0)  # top, right, bottom, left
            )
            self.status = ""
            if User.pcharacter == 0:
                self.status = "Selected"
            else:
                self.status = "Unlocked"

            self.item_description_widget = self.menu.add.label(title = self.status)
            self.mytheme.widget_background_color = (253, 111, 34) # 버튼 색깔
            self.menu.add.button("SELECT",self.select_pcharacter)
            self.menu.add.vertical_margin(5)
            self.menu.add.button("    BACK    ",self.to_menu)
            self.update_from_selection(int(self.pcharacter_selector.get_value()[0][1]))
            self.mytheme.widget_background_color = (0,10,63)

    def select_pcharacter(self):
        selected_idx = self.pcharacter_selector.get_value()[0][1]
        if User.police_lock[selected_idx] == False:
            User.pcharacter = selected_idx
            database = Database()
            database.set_pchar()
            self.menu.clear()
            self.show('police')
        else:
            print("character locked")
            import menu.CharacterLock
            menu.CharacterLock.Characterlock(self.screen,self.pcharacter_data[selected_idx].name).show()

   
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

    # 캐릭터 변경 시 실행
    def on_selector_change(self, selected, value: int) -> None:
        self.update_from_selection(value)

    # 캐릭터 선택 시 캐릭터 이미지 및 능력치 위젯 업데이트
    def update_from_selection(self, selected_value, **kwargs) -> None:
        self.status2 = ""
        if User.pcharacter == selected_value:
            self.status2 = "Selected"
        elif User.police_lock[selected_value] == False:
            self.status2 = "Unlocked"
        else:
            self.status2 = "Locked"

        self.current = selected_value
        self.image_widget.set_image(self.pcharacter_imgs2[selected_value])
        self.item_description_widget.set_title(title = self.status2)
