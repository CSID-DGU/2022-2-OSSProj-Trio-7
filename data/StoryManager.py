import pygame
import time
from data.database_user import *


class StoryManager():
    def __init__(self, stageinfo):
        print("stageinfo", stageinfo)
        self.db = Database()
        self.mapinfo = stageinfo
        pygame.init()
        screen = pygame.display.set_mode((512, 556))
        clock = pygame.time.Clock()

        # sound init
        self.test_sound = pygame.mixer.Sound("./Sound/message.wav")

        # bg init

        if self.mapinfo == "police":
            bg = pygame.image.load("./Image/background/police_background.png")
        elif self.mapinfo == "firefighter":
            bg = pygame.image.load(
                "./Image/background/firefighter_background.png")
        else:
            bg = pygame.image.load("./Image/background/doctor_background.png")
        bg = pygame.transform.scale(bg, (512, 556))

        text_box = pygame.Rect(0, 400, 512, 160)

        font = pygame.font.SysFont("malgungothic", 20)
        self.texts1 = ["시민 : 도둑이 나타났다!!", '도둑 두목 : 날 잡을 수 있으면 잡아보시지!',
                       '경찰 : 도둑을 어서 체포하자!', '경찰 : %s! 함께 현장으로 가자!' % (self.db.get_userId())]
        self.texts2 = ["시민 : 불이야~! 불이났다!!", "거대한 불 : 모든 것을 태워버리겠다!",
                       "소방관 : 어서 화재를 진압하자!", "소방관 : %s! 함께 현장으로 가자!" % (self.db.get_userId())]
        self.texts3 = ["시민 : 의사선생님 몸이 너무 아파요!", "슈퍼 바이러스 : 날 치료할 수 있으면 해보시지!",
                       "의사 : 어서 환자를 치료하자!", "의사 : %s! 함께 치료를 진행하자!" % (self.db.get_userId())]

        if self.mapinfo == "police":
            text_renders = [font.render(text, True, (255, 255, 255))
                            for text in self.texts1]
        elif self.mapinfo == "firefighter":
            text_renders = [font.render(text, True, (255, 255, 255))
                            for text in self.texts2]
        else:
            text_renders = [font.render(text, True, (255, 255, 255))
                            for text in self.texts3]

        index = -1
        self.space_released = True

        while True:

            clock.tick(60)
            screen.blit(bg, (0, 0))
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and space_released:
                space_released = False
                # if (index + 1) != len(text_renders) else 0
                index = (index + 1)
                self.test_sound.play()  # 정의한 소리 한번 재생
            elif not keys[pygame.K_SPACE]:
                space_released = True

            if index != -1:
                pygame.draw.rect(screen, (0, 0, 0, 0), text_box, 0)
                if index == len(text_renders):
                    print("스토리라인이 종료됩니다.")
                    time.sleep(2)
                    return
                else:
                    screen.blit(text_renders[index], (40, 430))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            pygame.display.update()
