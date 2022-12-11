from os import name
from tokenize import String
from turtle import title
import pygame
import pygame_menu
from data.CharacterDataManager import *
from data.StoreDataManager import *
from data.Defs import *
from data.Stage import Stage
from data.StageDataManager import *
from data.database_user import Database
from game.InfiniteGame import *
from pygame_menu.utils import make_surface
from object.Character import *

# 캐릭터 선택 메뉴
class CharacterStoreMenu_d:
    image_widget: 'pygame_menu.widgets.Image'
    item_description_widget: 'pygame_menu.widgets.Label'

    def __init__(self, screen, character_info):
        title = "캐릭터 선택"
        pygame.display.set_caption(title)  # 창의 제목 표시줄 옵션
        self.size = screen.get_size()
        self.character = character_info
        self.screen = screen
        
        self.orange_color = (253, 111, 34)
        self.font_size = self.size[0] * 30 // 720  # 글씨크기
        
        # 화면 받고 화면 크기 값 받기
        self.mytheme = pygame_menu.Theme(
            widget_font=Default.font.value,
            widget_background_color=(255, 255, 255),  # 버튼 배경색 설정
            title_font=Default.font.value,
            selection_color=(253, 111, 34),  # 선택됐을때 글씨색 설정
            widget_font_color=(0, 0, 0),  # 기본 글자색
            title_background_color=(255, 255, 255, 0), 
            title_font_color=(0, 0, 0, 0),
            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY,
            widget_font_size=self.size[0] * 45 // 720
        )

        main_image = pygame_menu.baseimage.BaseImage(
            image_path=Images.store.value, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)  # 메뉴 이미지, Images는 Defs.py에 선언되어 있는 클래스명

        self.mytheme.background_color = main_image

        self.menu = pygame_menu.Menu(
            '', self.size[0], self.size[1], theme=self.mytheme)  # 상단바


        self.show()
        self.menu.mainloop(self.screen,bgfun = self.check_resize)

    def to_menu(self):
            import menu.ModeSelectMenu
            game=menu.ModeSelectMenu.ModeSelectMenu(self.screen)

            while True:
                game.show(self.screen, self.character)
                pygame.display.flip()

    #메뉴 구성하고 보이기
    def show(self):  

        front_image_path = [Images.doctor.value, Images.doctor1.value, Images.doctor2.value]
        self.character_data = StoreDataManager.load("doctor")

        curs = Database().dct_db.cursor()
        self.id = User.user_id
        sql = "SELECT user_id, dchar1, dchar2, dchar3 FROM tusers2 WHERE user_id=%s"
        curs.execute(sql,self.id) 
        data = curs.fetchone()  
        curs.close()

        User.coin = Database().show_mycoin()
        self.menu.add.label("보유한 돈 : %d "%User.coin).scale(0.75, 0.75)
        #캐릭터 선택 메뉴 구성
        characters = []


        self.character_imgs = []
        self.character_imgs2 = []
        self.price = []

        for idx in range(1,4): # 데이터 베이스 정보를 가져올 인덱스 설정
            char = data[idx] # 해당 인덱스에 저장된 값 (-1 또는 보유시 5로 설정)

            if(char == -1): # 보유하지 않다면 (기본캐릭터는 상점에 나오지 않음)
                default_image = pygame_menu.BaseImage(
                    image_path=front_image_path[idx-1] # 1~3까지 설정된  front_image_path 이미지 띄움
                ).scale(0.3, 0.3)
                characters.append((self.character_data[idx-1].name, idx-1))
                self.character_imgs.append(default_image.copy())
                
        if len(characters)==0:
                    self.mytheme.widget_font_color=(0, 0, 0)
                    self.mytheme.widget_background_color = (255, 255, 255) # 버튼 색깔
                    self.menu.add.vertical_margin(10)
                    self.menu.add.label("구매할 수 있는 품목 없음.").scale(1.5, 1.5)
                    self.menu.add.vertical_margin(100)
                    self.mytheme.widget_font_color=(255, 255, 255)
                    self.mytheme.widget_background_color = (0, 10, 63) # 버튼 색깔
                    self.menu.add.button('   이전   ', self.to_menu,
                             selection_color=self.orange_color, font_size=self.font_size)

        else: # 구매할 아이템이 있을 경우
            for i in range(3): 
                    default_image = pygame_menu.BaseImage(
                    image_path=front_image_path[i]
                    ).scale(0.5, 0.5)
        
                    self.character_imgs2.append(default_image.copy())

            for i in range(0,3):
                self.price.append(User.price[i+1])
                
            self.character_selector = self.menu.add.selector(
                title='캐릭터 :',
                items=characters,
                onchange=self.on_selector_change
            )
            self.image_widget = self.menu.add.image(
                image_path=self.character_imgs[0],
                padding=(25, 0, 0, 0)  # top, right, bottom, left
            )
            

            self.item_description_widget = self.menu.add.label("")

            self.frame_v = self.menu.add.frame_v(400, 70, margin=(10, 0))
            
            self.mytheme.widget_font_color=(255, 255, 255)
            self.mytheme.widget_background_color = (0, 10, 63) # 버튼 색깔
            self.menu.add.button('   캐릭터 구매   ', self.buy_character,
                             selection_color=self.orange_color, font_size=self.font_size)

            self.menu.add.vertical_margin(10)
            self.menu.add.button('   이전   ', self.to_menu,
                             selection_color=self.orange_color, font_size=self.font_size)                 
            self.lock()

            
            self.update_from_selection(int(self.character_selector.get_value()[0][1]))
            self.mytheme.widget_background_color =(0,10,63)
        


    def buy_character(self):

        print("아이템을 구매합니다.")

        curs = Database().dct_db.cursor()
        self.id = User.user_id
        sql = "SELECT user_id, dchar1, dchar2, dchar3, user_coin FROM tusers2 WHERE user_id=%s" 
        curs.execute(sql,self.id) 
        data = curs.fetchone()  
        curs.close()
        
       
        # 캐릭터 셀릭터가 선택하고 있는 데이터를 get_value 로 가져와서, 그 중 Character 객체를 [0][1]로 접근하여 할당
        selected_idx = self.character_selector.get_value()[0][1]
        if(User.coin >= self.price[selected_idx]):
            User.buy_dcharacter = selected_idx + 6
            database = Database()
            database.buy_dchar()
            User.coin = Database().show_mycoin()
            self.item_description_widget.set_title(title = "Unlocked" )

        else:
            print("not enough money") 
            import menu.CharacterBuy_d
            menu.CharacterBuy_d.CharacterBuy_d(self.screen,self.character_data[selected_idx].name).show()    

    #잠금 표시
    def lock(self):

        curs = Database().dct_db.cursor()
        self.id = User.user_id
        sql = "SELECT user_id, dchar1, dchar2, dchar3 FROM tusers2 WHERE user_id=%s" 
        curs.execute(sql,self.id) 
        data = curs.fetchone()  
        curs.close()
 

        selected_idx = self.character_selector.get_value()[0][1]

        if(data[2] == 0):
            self.item_description_widget.set_title(title = "Locked")
        else:
            self.item_description_widget.set_title(title = "Unlocked" if data[selected_idx] == True else "Locked")
        
        if(data[3] == 0):
            self.item_description_widget.set_title(title = "Locked")
        else:
            self.item_description_widget.set_title(title = "Unlocked" if data[selected_idx] == True else "Locked")


    # 화면 크기 조정 감지 및 비율 고정
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
            self.menu.resize(new_w, new_h)
            self.menu._current._widgets_surface = make_surface(0, 0)
            self.size = window_size
            print(f'New menu size: {self.menu.get_size()}')
            font_size = new_w * 45 // 720
            self.mytheme.widget_font_size = font_size

    # 캐릭터 변경 시 실행
    def on_selector_change(self, selected, value: int) -> None:
        self.update_from_selection(value)

    # 캐릭터 선택 시 캐릭터 이미지 및 능력치 위젯 업데이트
    def update_from_selection(self, selected_value, **kwargs) -> None:
        self.current = selected_value
        self.image_widget.set_image(self.character_imgs2[selected_value])
        self.item_description_widget.set_title(title = self.price[selected_value])