import pygame
import math
from data.Stage import Stage
from data.database_user import Database

pygame.init()



class StoryManager():
    def __init__(self, stage):
        self.scene = 0
        self.ACT = stage # 챕터에 따라 메시지 출력
        print(stage)
        ## StoryManager *UI
        
        font = pygame.font.Font(None, 30)
        self.word = "This is a text \ This is the second line"
        self.text = pygame.font.Font(None, 25).render(self.word, True, (200,200,200), (0,0,0))
        self.boarder = pygame.Rect(10,5, 600,130)
        self.name = Database().get_userId() # 스토리라인에 삽입할 유저 이름을 db에서 가져옴

        ## StoryManager *Sounds
        self.sounds = []
        self.sounds = ["./Sound/message.wav"]


        ## StoryManager *Tools
        self.timer = 15
        self.isScene = False
        self.sceneEnd = False
        

    def PlaySound(self, type=0):
        pygame.mixer.Sound(self.sounds[type]).play()
        # pygame.mixer.music.load("./Sound/message.wav")
        # pygame.mixer.music.play(-1)

    def Update(self): # 다음 대사로 업데이트 해줌
        self.timer -= 0.1
        if self.timer <= 0:
            self.NextPhase()

    def NextPhase(self):
        self.scene += 1
        self.PlaySound()
        if self.ACT == "map1": # 경찰맵일 경우
            #Phase 1
            if self.scene == 1:
                self.isScene = True
                self.word = "으아악!!!!... 도둑이다!!"
                self.text = pygame.font.Font(None, 25).render("시민 : " + self.word, True, (0,0,255), (0,0,0))
                self.timer = 20
                
            #Phase 2
            if self.scene == 2:
                self.word = "도둑이 돈다발을 훔쳐서 달아나고 있어!"
                self.text = pygame.font.Font(None, 25).render(self.name + ": " + self.word, True, (0,0,255), (0,0,0))
                self.timer = 5

            #Phase 3
            if self.scene == 3:
                self.word = "서둘러서 체포하자!"
                self.text = pygame.font.Font(None, 25).render(self.name + ": " + self.word, True, (0,0,255), (0,0,0))
                self.timer = 5
            
            if self.scene == 24:
                self.isScene = False
                self.sceneEnd = True
                self.timer = 30
                self.scene = 0
            