import pygame, time
from data.database_user import *


class StoryManager():
    def __init__(self, stageinfo):
        self.db = Database()
        self.mapinfo = stageinfo
        # 게임창 설정
        pygame.init()
        infoObject = pygame.display.Info()
        self.size = [infoObject.current_w,infoObject.current_h] # 512, 556
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        
        clock = pygame.time.Clock()
        

        # sound init
        self.test_sound = pygame.mixer.Sound("./Sound/message.wav")

        # bg init
        bg_y = 0 # 배경이동을 위한 변수
        if self.mapinfo == "map1":
            bg = pygame.image.load("./Image/background/police_background.png")
        elif self.mapinfo == "map2":
            bg = pygame.image.load("./Image/background/firefighter_background.png")
        else:
            bg = pygame.image.load("./Image/background/doctor_background.png")

        text_box = pygame.Rect(0, 400, infoObject.current_w, 165)

        # dialogue init
        font = pygame.font.SysFont("malgungothic", 20)
        self.texts1 = ["시민 : 도둑이 나타났다!!", '도둑 두목 : 날 잡을 수 있으면 잡아보시지!', '경찰 : 도둑을 어서 체포하자!', '경찰 : %s! 함께 현장으로 가자!'%(self.db.get_nickname())]
        self.texts2 = ["시민 : 불이야~! 불이났다!!", "거대한 불 : 모든 것을 태워버리겠다!", "소방관 : 어서 화재를 진압하자!", "소방관 : %s! 함께 현장으로 가자!"%(self.db.get_nickname())]
        self.texts3 = ["시민 : 의사선생님 몸이 너무 아파요!", "슈퍼 바이러스 : 날 치료할 수 있으면 해보시지!", "의사 : 어서 환자를 치료하자!", "의사 : %s! 함께 치료를 진행하자!"%(self.db.get_nickname())]
        
        if self.mapinfo == "map1":
            text_renders = [font.render(text, True, (255, 255, 255)) for text in self.texts1]
        elif self.mapinfo == "map2":
            text_renders = [font.render(text, True, (255, 255, 255)) for text in self.texts2]
        else:
            text_renders = [font.render(text, True, (255, 255, 255)) for text in self.texts3]
        
        index = -1
        self.space_released = True

        while True:
            
            clock.tick(60)
            
            # 화면 흰색으로 채우기
            self.screen.fill((255, 255, 255))
            
            bg = pygame.transform.scale(bg, self.size)
            bg_width = bg.get_width()
            bg_height = bg.get_height()
            bg2 = bg.copy()
            self.screen.blit(bg, (0, bg_y))
            self.screen.blit(bg2, (0, 0), pygame.Rect(0, bg_height - bg_y, bg_width, bg_y))
            

            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE: #화면이 리사이즈 되면
                        #화면 크기가 최소 300x390은 될 수 있도록, 변경된 크기가 그것보다 작으면 300x390으로 바꿔준다
                        width, height = max(event.w,300), max(event.h,390)

                        #크기를 조절해도 화면의 비율이 유지되도록, 가로와 세로 중 작은 것을 기준으로 종횡비(10:13)으로 계산
                        if(width<=height):
                            height = int(width * (13/10))
                        else:
                            width = int(height * (10/13))
                        
                        w_ratio = width/self.size[0]
                        h_ratio = height/self.size[1]

                        self.size =[width,height] #게임의 size 속성 변경
                        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE) #창 크기 세팅
                        # text박스 크기도 변경 필요
                        text_box = pygame.Rect(0, self.size[1]*0.80, self.size[0], 165)
            
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_SPACE] and space_released:
                space_released = False
                index = (index + 1) #if (index + 1) != len(text_renders) else 0
                self.test_sound.play() # 정의한 소리 한번 재생
            elif not keys[pygame.K_SPACE]:
                space_released = True
            
            if index != -1:
                pygame.draw.rect(self.screen, (0, 0, 0, 0), text_box, 0)
                if index == len(text_renders):
                    print("스토리라인이 종료됩니다.")
                    time.sleep(2)
                    return
                else:
                    self.screen.blit(text_renders[index], (40, self.size[1]*0.85))
                    
                

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            
            pygame.display.update()
    def get_currentSize(self):
        return self.size
            