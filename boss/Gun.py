import pygame
from data.Defs import Default


class Gun(): #Gun class for boss gun
    def __init__(self,x,y): #need to save location
        self.boundary = pygame.display.get_surface().get_size()
        self.org_boundary = [Default.game.value["size"]["x"],Default.game.value["size"]["y"]]
        self.x = x
        self.y = y

    # 크기 조정 함수
    def on_resize(self, game):
        old_boundary = self.boundary
        self.boundary = game.size
        self.reposition(old_boundary)

    # 변경된 비율에 따라 위치 조정
    def reposition(self, old_boundary):
        x_scale = self.x/old_boundary[0]
        y_scale = self.y/old_boundary[1]
        self.x = int(self.boundary[0] * x_scale)
        self.y = int(self.boundary[1] * y_scale)