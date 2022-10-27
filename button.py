import pygame
import os
from pygame.locals import *
from data.Defs import *

class button():   # 버튼 class
   
    def __init__(self, board_width, board_height, x_rate, y_rate, width_rate, height_rate, img=''):   # 버튼 생성
        self.x = board_width * x_rate   # 버튼 x 좌표
        self.y = board_height * y_rate   # 버튼 y 좌표
        self.width = int(board_width * width_rate)   # 버튼의 너비
        self.height = int(board_height * height_rate)   # 버튼의 높이
        self.x_rate = x_rate   
        self.y_rate = y_rate
        self.width_rate = width_rate
        self.height_rate = height_rate
        self.image = img

    def change(self, board_width, board_height):   # 버튼 위치, 크기 바꾸기
        self.x = board_width * self.x_rate   # x 좌표
        self.y = board_height * self.y_rate   # y 좌표
        self.width = int(board_width * self.width_rate)   # 너비
        self.height = int(board_height * self.height_rate)   # 높이

    def draw(self, win, outline=None):   # 버튼 보이게 만들기 
        if outline:
            draw_image(win, self.image, self.x, self.y, self.width, self.height)
            
    def isOver(self, pos):   # pos[0]: 마우스의 x 좌표 / pos[1]: 마우스의 y 좌표
        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):   
            if pos[1] > self.y - (self.height / 2) and pos[1] < self.y + (self.height / 2):   
                return True
        return False

def draw_image(window, img_path, x, y, width, height):
    x = x - (width / 2)    
    y = y - (height / 2)
    image = pygame.image.load(os.path.abspath(img_path))
    image = pygame.transform.smoothscale(image, (width, height))
    window.blit(image, (x, y))
