# Character : 이동속도, 투사체 속도, 크기, 이미지, 투사체 사운드
# stage : 목표점수, 배경이미지, 배경 사운드

# 게임 : 목숨, 시간
# 로직 : 세이브파일 변경 후 저장 필요

import random
import time
from collections import OrderedDict
from typing import Sized
from menu.LeaderBoardMenu import *
import pygame
import pygame_menu
from boss.Boss import Boss
from boss.Bullet import Bullet
from data.Animation import AnimationManager
from data.Defs import *
from data.StageDataManager import *
from object.Effect import *
from object.Item import *
from object.Mob import Mob
from pygame_menu.locals import ALIGN_CENTER
from pygame_menu.utils import make_surface
from data.database_user import *
from data.Defs import User

class InfiniteGame:

    def __init__(self,character,mode,mapimg,attimg):
        # 1. 게임초기화 
        pygame.init()

        # 2. 게임창 옵션 설정
        infoObject = pygame.display.Info()
        title = "Infinite game"
        pygame.display.set_caption(title) # 창의 제목 표시줄 옵션
        self.size = [infoObject.current_w,infoObject.current_h]
        self.screen = pygame.display.set_mode(self.size,pygame.RESIZABLE)
        self.font_size = self.size[0] * 40 //720
        self.scale = (self.size[0]*0.00015,self.size[1]*0.00015)
        

        # 3. 게임 내 필요한 설정
        self.clock = pygame.time.Clock() # 이걸로 FPS설정함
        self.mode = mode #Game mode = hard/easy
        self.menu = pygame_menu.Menu('Game Over!!', self.size[0], self.size[1],
                            theme=pygame_menu.themes.THEME_DEFAULT)

        # 4. 게임에 필요한 객체들을 담을 배열 생성, 변수 초기화
        self.animation = AnimationManager()
        self.mobList = []
        self.item_list = []
        self.effect_list = []
        self.missileList = []
        self.character = character
        self.score = 0
        self.life = 3
        self.start_time = time.time()
        self.mob_gen_rate = 0.01
        self.mob_image = attimg
        self.background_image = mapimg
        self.background_music = "./Sound/bgm/bensound-evolution.wav"
        self.SB = 0
        self.dy = 2
        self.mob_velocity = 2
        self.coin = 0
        self.enemyBullets =[]

        # 5. 캐릭터 초기화
        self.character.reinitialize(self)

        # user
        self.database = Database()
        self.user=User.user_id

        #일시정지 버튼 
        self.changed_screen_size = self.screen.get_size()
        self.board_width=self.changed_screen_size[0] # x
        self.board_height=self.changed_screen_size[1] # y
        import button
        self.stop = button.button(self.board_width, self.board_height, 0.95,0.05,0.1,0.1, "Image/catthema/stop.png")

    def main(self):
        from menu.gameselectMenu import soundset
        # 메인 이벤트
        pygame.mixer.init()
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(soundset)
        background1_y = 0 # 배경 움직임을 위한 변수
        while self.SB==0:
            #fps 제한을 위해 한 loop에 한번 반드시 호출해야합니다.
            self.clock.tick(30)
            
            #화면 흰색으로 채우기
            self.screen.fill(Color.WHITE.value)
            # 배경 크기 변경 처리 및 그리기
            # 창크기가 바뀜에 따라 배경화면 크기 변경 필요
            
            background1 =  pygame.image.load(self.background_image)
            background1 = pygame.transform.scale(background1, self.size)
            background_width = background1.get_width()
            background_height = background1.get_height()
            background2 = background1.copy()
            self.screen.blit(background1, (0, background1_y))
            self.screen.blit(background2, (0, 0), pygame.Rect(0,background_height - background1_y,background_width,background1_y))
            self.stop.change(self.screen.get_size()[0],self.screen.get_size()[1]) # 화면 사이즈 변경되면 버튼사이즈 바꿔줌.
            self.stop.draw(self.screen,(0,0,0))

            # 입력 처리
            for event in pygame.event.get(): #동작을 했을때 행동을 받아오게됨
                if event.type ==pygame.QUIT:
                    self.SB=1 # SB 가 1이되면 while 문을 벗어나오게 됨
                if event.type == pygame.KEYDOWN: # 어떤 키를 눌렀을때!(키보드가 눌렸을 때)
                    if event.key == pygame.K_x:
                        self.SB=1
                    if event.key == pygame.K_z: #테스트용
                        self.score += 30
                pos = pygame.mouse.get_pos() # mouse
                if event.type == pygame.MOUSEBUTTONUP: 
                    if self.stop.isOver(pos): #마우스로 일시정지 버튼 클릭하면
                        self.StopGame()

                if event.type == pygame.VIDEORESIZE: #창크기가 변경되었을 때
                    #화면 크기가 최소 300x390은 될 수 있도록, 변경된 크기가 그것보다 작으면 300x390으로 바꿔준다
                    width, height = max(event.w,300), max(event.h,390)

                    #크기를 조절해도 화면의 비율이 유지되도록, 가로와 세로 중 작은 것을 기준으로 종횡비(10:13)으로 계산
                    if(width<=height):
                        height = int(width * (13/10))
                    else:
                        width = int(height * (10/13))
                    
                    self.size =[width,height] #게임의 size 속성 변경
                    self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE) #창 크기 세팅
                    self.check_resize()
                    self.animation.on_resize(self)

            #몹을 확률적으로 발생시키기
            if(random.random()<self.mob_gen_rate):
                newMob = Mob(self.mob_image,{"x":50, "y":50},self.mob_velocity,0)
                newMob.set_XY((random.randrange(0,self.size[0]),0)) #set mob location randomly
                self.mobList.append(newMob)
            
            if random.random() < Default.item.value["powerup"]["spawn_rate"]:
                new_item = PowerUp(self.animation.animations["powerup"])
                new_item.set_XY((random.randrange(0,self.size[0]-new_item.sx),0))
                self.item_list.append(new_item)

            if random.random() < Default.item.value["bomb"]["spawn_rate"]:
                new_item = Bomb(self.animation.animations["bomb"])
                new_item.set_XY((random.randrange(0,self.size[0]-new_item.sx),0))
                self.item_list.append(new_item)

            if random.random() < Default.item.value["health"]["spawn_rate"]:
                new_item = Health(self.animation.animations["health"])
                new_item.set_XY((random.randrange(0,self.size[0]-new_item.sx),0))
                self.item_list.append(new_item)

            if random.random() < Default.item.value["coin"]["spawn_rate"]:
                new_item = Coin(self.animation.animations["coin"])
                new_item.set_XY((random.randrange(0,self.size[0]-new_item.sx),0))
                self.item_list.append(new_item)

            if random.random()< Default.item.value["speedup"]["spawn_rate"]:
                new_item = SpeedUp(self.animation.animations["speedup"])
                new_item.set_XY((random.randrange(0,self.size[0]-new_item.sx),0))
                self.item_list.append(new_item)
            

            #플레이어 객체 이동
            self.character.update(self)

            #몹 객체 이동
            for mob in self.mobList:
                mob.move(self.size,self)

            for item in self.item_list:
                item.move(self)

            for effect in self.effect_list:
                effect.move(self)
        
            #적 투사체 이동
            for bullet in self.enemyBullets:
                bullet.move(self.size,self)
                bullet.show(self.screen)

            for item in list(self.item_list):
                if item.rect_collide(self.character.rect):
                    item.use(self)

            #발사체와 몹 충돌 감지
            for missile in list(self.character.get_missiles_fired()):
                for mob in list(self.mobList):
                    if self.check_crash(missile,mob):
                        self.score += 10
                        if missile in self.character.missiles_fired:
                            self.character.missiles_fired.remove(missile)
                        mob.destroy(self)

            #몹과 플레이어 충돌 감지
            for mob in list(self.mobList):
                if(self.check_crash(mob,self.character)):
                    if self.character.is_collidable == True:
                        self.character.last_crashed = time.time()
                        self.character.is_collidable = False
                        print("crash!")
                        self.life -= 1
                        mob.destroy(self)
                   
            #화면 그리기
            for effect in self.effect_list:
                effect.show(self.screen)
            #플레이어 그리기
            self.character.show(self.screen)
            
            #몹 그리기
            for mob in self.mobList:
                mob.show(self.screen)

            for item in list(self.item_list):
                item.show(self.screen)

            for i in self.character.get_missiles_fired():
                i.show(self.screen)
                if hasattr(i, "crosshair"):
                    if i.locked_on == True:
                        i.crosshair.show(self.screen)
            
            #점수와 목숨 표시
            font = pygame.font.Font(Default.font.value, self.size[0]//40)
            score_life_text = font.render("Score : {} Life: {} Bomb: {} Coin : {}".format(self.score,self.life,self.character.bomb_count, self.coin), True, Color.YELLOW.value) # 폰트가지고 랜더링 하는데 표시할 내용, True는 글자가 잘 안깨지게 하는 거임 걍 켜두기, 글자의 색깔
            self.screen.blit(score_life_text,(10,5)) # 이미지화 한 텍스트라 이미지를 보여준다고 생각하면 됨 
            
            # 현재 흘러간 시간
            play_time = (time.time() - self.start_time)
            time_text = font.render("Time : {:.2f}".format(play_time), True, Color.YELLOW.value)
            self.screen.blit(time_text,(self.size[0]//2,5))

            # 화면갱신
            pygame.display.flip() # 그려왔던데 화면에 업데이트가 됨


            #목숨이 0 이하면 랭킹 등록 화면
            if(self.life<1):
                self.register_ranking()
                self.show_ranking_register_screen()
                return

            self.mode.update_difficulty(self)


        # While 빠져나오면 랭킹등록 스크린 실행
        self.register_ranking()
        self.show_ranking_register_screen()
                
    #충돌 감지 함수
    def check_crash(self,o1,o2):
        o1_mask = pygame.mask.from_surface(o1.img)
        o2_mask = pygame.mask.from_surface(o2.img)

        offset = (int(o2.x - o1.x), int(o2.y - o1.y))
        collision = o1_mask.overlap(o2_mask, offset)
        
        if collision:
            return True
        else:
            return False

    #홈버튼 클릭 시
    def Home(self, menu):
        menu.disable()
        pygame.mixer.music.stop()

    def show_ranking_register_screen(self):
        pygame.mixer.music.stop()
        ranking_register_screen = pygame_menu.themes.THEME_DEFAULT.copy()
        ranking_register_screen.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
        ranking_register_screen.title_close_button_cursor = pygame_menu.locals.CURSOR_HAND
        ranking_register_screen.title_font_color = Color.WHITE.value
        self.menu = pygame_menu.Menu('Game Over', self.size[0], self.size[1],
                            theme=ranking_register_screen)
        self.menu.add.image(Images.lose.value, scale=self.scale)
        self.menu.add.label("Score : {}".format(self.score),font_size = self.font_size)
        self.menu.add.button('Ranking', self.show_register_result,font_size = self.font_size) # 랭킹화면으로 넘어가도록 설정했음.
        self.menu.add.button('Retry', self.retry, font_size = self.font_size)
        self.menu.add.button('to Home', self.gameselectmenu,font_size = self.font_size)
        self.menu.mainloop(self.screen,bgfun = self.check_resize_end)
        pygame.display.flip()
        User.coin = User.coin + self.coin
        self.database = Database()
        self.database.set_coin()
    
    def register_ranking(self): # 랭크 기록
        current_score = self.score # 현재 게임 기록
        print(self.user)
        print(current_score)
        if(isinstance(self.mode,InfiniteGame.EasyMode)): # easy mode
            if self.database.rank_not_exists(self.user,"easy") is True : # 기록 없는 경우
                self.database.update_score2("easy",current_score) # 기록추가
                print("enter")
            else : 
                if (self.database.high_score("easy") <= current_score) : # 데이터 베이스에 저장되어 있는 점수 비교 후 등록
                    self.database.update_score('easy',current_score) # 새로운 점수가 더 높으면 기록           
        else : # hard mode
            if self.database.rank_not_exists(self.user,"hard") is True : # 기록 없는 경우
                self.database.update_score2("hard",current_score)
            else :
                if (self.database.high_score("hard") <= current_score) : # 데이터 베이스에 저장되어 있는 점수 비교 후 등록
                    self.database.update_score('hard',current_score) 
                     

    # 랭킹 등록 결과 화면
    def show_register_result(self):
        #self.menu.remove_widget(self.result_frame)
        LeaderBoardMenu(self.screen).rank()  

    def gameselectmenu(self):
        import menu.gameselectMenu
        game=menu.gameselectMenu.GameselectMenu(self.screen)

        while True:
            game.show(self.screen)
            pygame.display.flip()    

    #Continue 클릭 시
    def Continue(self, menu):
        menu.disable()
        pygame.mixer.music.unpause()
    
    # 일시정지 화면
    def StopGame(self):
        pygame.mixer.music.pause()
        stageclear_theme = pygame_menu.themes.THEME_SOLARIZED.copy()
        stageclear_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
        stageclear_theme.title_close_button_cursor = pygame_menu.locals.CURSOR_HAND
        stageclear_theme.title_font_color = Color.WHITE.value
        self.menu = pygame_menu.Menu('Paused', self.size[0], self.size[1],
                                    theme=stageclear_theme)   
        self.menu.add.image(Images.win.value, scale=self.scale)
        self.menu.add.label("")
        self.menu.add.label('Paused',font_size = self.screen.get_size()[0]*40//720)
        self.menu.add.button('Continue', self.Continue, self.menu, font_size = self.font_size)
        self.menu.add.button("Restart",self.retry,font_size = self.font_size)
        self.menu.add.button("Home",self.gameselectmenu,font_size = self.font_size,)
        self.menu.mainloop(self.screen,bgfun=self.check_resize)

    def check_resize_end(self):
        if self.check_resize():
            self.menu.disable()
            self.show_ranking_register_screen()

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
            print(self.screen)
            font_size = new_w * 40 //720
            self.font_size = font_size
            self.scale = (new_w*0.00015,new_h*0.00015)
            return True

    #재시도 버튼 클릭 시 실행
    def retry(self):
        InfiniteGame(self.character,self.mode, self.background_image,self.mob_image).main()
        self.menu.disable()
    
    #난이도를 나누는 모드 클래스 (상속하여 사용)
    class Mode:
        def update_difficulty():
            pass

    class EasyMode(Mode): #이지 모드
        @staticmethod
        def update_difficulty(game):
            play_time = (time.time() - game.start_time) #게임 진행 시간
            if(game.mob_gen_rate < 0.215): #최대값 제한
                game.mob_gen_rate = play_time//10/10 + 0.015 #10초마다 mob_gen_rate 0.1 증가(기본 0.015)
            if(game.dy<20):#최대값 제한
                game.dy = play_time//5*2 + 2 #5초마다 dy(배경 이동 속도) 2 증가 (기본 2)
            if(game.mob_velocity < 3):#최대값 제한
                game.mob_velocity = play_time//10*1 + 2 #10초마다 mob_velocity(몹 이동 속도) 1 증가 (기본 2)

    class HardMode(Mode): #하드 모드
        @staticmethod
        def update_difficulty(game):
            play_time = (time.time() - game.start_time) #게임 진행 시간
            if(game.mob_gen_rate < 0.315):#최대값 제한
                game.mob_gen_rate = play_time//10/10 + 0.015 #10초마다 mob_gen_rate 0.1 증가(기본 0.015)
            if(game.dy<20):#최대값 제한
                game.dy = play_time//5*2 + 2 #5초마다 dy(배경 이동 속도) 2 증가 (기본 2)
            if(game.mob_velocity < 6):#최대값 제한
                game.mob_velocity = play_time//10*2 + 2 #10초마다 mob_velocity(몹 이동 속도) 2 증가 (기본 2)
