'''MIT License

Copyright (c) 2018 TimurKhayrullin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

import random
import time
from math import *
from sys import *

import pygame
from data.Defs import *

from boss.Bullet import Bullet
from boss.Gun import Gun


class Boss():

    
    def __init__(self, screen,image_path_list,bullet_image_path):
        #image and position
        self.boundary = pygame.display.get_surface().get_size()
        self.org_boundary = [Default.game.value["size"]["x"],Default.game.value["size"]["y"]]
        self.image_path_list = image_path_list
        self.load_images(image_path_list)
        self.x = screen[0]*0.5
        self.y = 0
        self.size = Default.boss.value["size"]
        self.org_gun_size = Default.boss.value["gun_size"]
        self.gun_size = self.org_gun_size
        self.sx, self.sy = (self.size["x"], self.size["y"])
        self.change_img_size()
        self.img = self.orig_imgs[0]
        self.bullet_image_path = bullet_image_path

        #boss properties init
        self.phase = 0
        self.max_health = Default.boss.value["health"]
        self.health = self.max_health
        self.velocity = Default.boss.value["velocity"]
        self.bullet_size = Default.boss.value["bullet_size"]
        ##timers for attack balancing
        self.pause_timer = 120
        #firing time is reset if firing speed is reached
        self.firing_speed = Default.boss.value["firing_speed"]
        self.firing_time = 0
        #grace time is reset if grace time is reached
        self.grace_timers = Default.boss.value["grace_timers"]
        self.grace_time = Default.boss.value["grace_time"]
        #attacks init
        self.attacks = [False, False, False, False]
        self.directions = 0
        #counter of how much boss moved
        self.frames_spent_moving = 0

        ##vars for gun positions and angles for attack patterns
        # 이미지 아웃라인에 Gun 생성
        self.random_pos_gun_on_outline()
        self.gun_queue = random.sample(self.gun_pos, len(self.gun_pos))
        #chosen angle and chosen gun 
        self.target_angle = 0
        self.target_gun = self.gun_pos[0]
        #angles to shoot at 
        self.angles_double = [85, 95]
        self.angles_triple = [45, 90, 135]
        self.angles_quad = [18, 36, 54, 72]
        self.angles_quint = [15, 30, 45, 60, 75]
        #Colors for HP display
        self.colors = [Color.BLUE.value,Color.GREEN.value,Color.RED.value]

        self.last_bombed = 0.0
        self.hit_interval = 1.0

    def change_img_size(self):
        x_scale = self.boundary[0]/self.org_boundary[0]
        y_scale = self.boundary[1]/self.org_boundary[1]
        x = int(self.size["x"]*x_scale)
        y = int(self.size["y"]*y_scale)
        self.gun_size = int(self.org_gun_size*x_scale)
        for i in range(len(self.orig_imgs)):
            self.orig_imgs[i] = pygame.transform.scale(self.orig_imgs[i],(x,y)) # 그림의 크기를 조정한다.
            self.sx, self.sy = self.orig_imgs[i].get_size()
      
    def move(self,boundary):
        #범위 내에서 이동하고, 총 위치도 이동
        if self.directions == 0:
            if self.y < boundary[1] * 0.8 - self.sy:
                self.y += self.velocity[self.phase]
                for gun in self.gun_pos:
                    gun.y += self.velocity[self.phase]
        elif self.directions == 1:
            if 0 < self.y:
                self.y -= self.velocity[self.phase]
                for gun in self.gun_pos:
                    gun.y -= self.velocity[self.phase]
        elif self.directions == 2:
            if 0 < self.x:
                self.x -= self.velocity[self.phase]
                for gun in self.gun_pos:
                    gun.x -= self.velocity[self.phase]
        elif self.directions == 3:
            if self.x < boundary[0] - self.sx:
                self.x += self.velocity[self.phase]
                for gun in self.gun_pos:
                    gun.x += self.velocity[self.phase]
    
    
    #attack coreography
    def attack1(self,enemyBullets,player):
        #shoots 5 pellet spread from random gun
        if self.attacks[0]:
            self.target_gun = self.gun_pos[random.randint(0,3)]
            for angle in self.angles_quint:
                #finds point on circle based on angle and radius, fires enemyBullet there
                self.target_angle = (self.target_gun.x + 50 * cos(radians(angle + 45)), 
                                          self.target_gun.y + 50 * sin(radians(angle + 45)))            
                enemyBullets.append(Bullet(self.bullet_image_path,self.bullet_size,10,(self.target_gun.x,self.target_gun.y),self.target_angle))
                 #ends attack
            self.attacks[0] = False
    
    def attack2(self,enemyBullets,player):
        # shoots triple shots in random gun pattern
        if self.attacks[1]:
            for i in range(len(self.gun_queue)):
                #checks if timer conditions are just right
                if self.firing_time == self.firing_speed[self.phase] * i:
                    #sets target gun based on random queue
                    self.target_gun = self.gun_queue[i]
                    for angle in self.angles_triple:
                        #finds point on circle based on angle and radius, fires enemyBullet there
                        self.target_angle = (self.target_gun.x + 50 * cos(radians(angle)), 
                                                  self.target_gun.y + 50 * sin(radians(angle)))            
                        enemyBullets.append(Bullet(self.bullet_image_path,self.bullet_size,10,(self.target_gun.x,self.target_gun.y),self.target_angle))
                #ends attack
                if self.firing_time == self.firing_speed[self.phase] * len(self.gun_queue):
                    self.attacks[1] = False
                    self.firing_time = 0 
                    break
            else:
                self.firing_time += 1
            
    def attack3(self,enemyBullets,player):
        #shoots stream of bullets from left to right from random guns
        if self.attacks[2]:
            for angle in range(60, 120, -self.phase + 3):
                #checks if timer conditions are just right
                if self.firing_time + 60 == angle:
                    for i in range(2):
                        #chooses random gun (twice)
                        self.target_gun = self.gun_queue[i]
                        #finds point on circle based on angle and radius, fires enemyBullet there
                        self.target_angle = (self.target_gun.x + 50 * cos(radians(angle)), 
                                                  self.target_gun.y + 50 * sin(radians(angle)))            
                        enemyBullets.append(Bullet(self.bullet_image_path,self.bullet_size,10,(self.target_gun.x,self.target_gun.y),self.target_angle))
                #ends attack
                if self.firing_time + 60 >= 120:
                    self.attacks[2] = False
                    self.firing_time = 0
                    break
            else: self.firing_time += 1
            
    def attack4(self,enemyBullets,player):
        #shoots stream of bullets from left to right
        if self.attacks[3]:
            for angle in range(120, 60, -(-self.phase + 3)):
                #checks if timer conditions are just right
                if self.firing_time + 60 == angle:
                    for i in range(2):
                        #chooses random gun (twice)
                        self.target_gun = self.gun_queue[i]
                        #finds point on circle based on angle and radius, fires enemyBullet there
                        # self.target_angle = (self.target_gun[0]+self.x + 50 * cos(radians(180 - angle)), 
                        #                           self.target_gun[1]+self.y + 50 * sin(radians(180 -angle)))            
                        enemyBullets.append(Bullet(self.bullet_image_path,self.bullet_size,10,(self.target_gun.x,self.target_gun.y),(player.x,player.y)))
                #ends attack
                if self.firing_time + 60 >= 120:
                    self.attacks[3] = False
                    self.firing_time = 0
                    break
            else: self.firing_time += 1        

    #draws itself and it's health
    def draw(self,screen):
        screen.blit(self.orig_imgs[self.phase], (self.x, self.y))

        # 총 그리기
        for gun in self.gun_pos:
            pygame.draw.circle(screen, (255,0,0), (int(gun.x),int(gun.y)), self.gun_size)

        #체력 표시
        font = pygame.font.Font(Default.font.value, int(self.sy * 0.08)) #폰트설정 (폰트,크기)
        boss_health_text = font.render("HP : %i/%i" %(self.health, self.max_health), True, self.colors[self.phase]) # 폰트렌더링(문자열,안티앨리어싱,컬러)
        screen.blit(boss_health_text,(self.x,self.y-20))

        #다음 액션 타이밍 예고
        pygame.draw.rect(screen,(255,0,0),pygame.Rect(self.x+self.sx+10,self.y+(self.sy*0.2),5,self.grace_time))

    
    def update(self,enemyBullets,player,boundary):

        if self.grace_time == 0:
            #handles attack timings with some randomness
            self.attacks[random.randint(0,3)] = True
            self.gun_queue = random.sample(self.gun_pos, len(self.gun_pos))
            self.directions = random.randint(0,3)
            
            #resets movement during attacks
            self.frames_spent_moving = 0
            
            #handles in between attack grace timers
            if self.attacks[0] == True: 
                self.grace_time = self.grace_timers[self.phase] // 8
            else: self.grace_time = self.grace_timers[self.phase]
        else: 
            #handles movement between attacks
            if self.frames_spent_moving <= 30:
                self.move(boundary)
                self.frames_spent_moving += 1
            self.grace_time -= 1
      
        #tries to fire each attack
        self.attack1(enemyBullets,player) # random quintuple shot
        self.attack2(enemyBullets,player) # random sequence of triple shots
        self.attack3(enemyBullets,player) #chooses 2 random guns to fire from, goes from left to right
        self.attack4(enemyBullets,player) #chooses 2 random guns to fire from, aim player
    
    #checks itself for health, changes phases after certain point
    def check(self,player,game):
        for bullet in player.missiles_fired:
            if(bullet.check_crash(self)):
                self.health -= bullet.power
                player.missiles_fired.remove(bullet)
        for effect in game.effect_list:
            if effect.check_crash(self):
                if time.time()-self.last_bombed > self.hit_interval:
                    self.last_bombed = time.time()
                    self.health -= Default.item.value["bomb"]["power"]
        # checks if it is supposed to die
        if self.health <= 0:
            game.stage_cleared = True
        #changes phases
        elif self.health <= self.max_health // 3 and self.phase<2:
            self.phase = 2
            self.img = self.orig_imgs[self.phase]
            self.random_pos_gun_on_outline()
        elif self.health <= self.max_health // 3 * 2 and self.phase<1:
            self.phase = 1
            self.img = self.orig_imgs[self.phase]
            self.random_pos_gun_on_outline()
              

    def load_images(self,image_path_list):
        self.orig_imgs = []
        for image_path in image_path_list:
            self.orig_imgs.append(pygame.image.load(image_path).convert_alpha())
      
    def random_pos_gun_on_outline(self):
        mask = pygame.mask.from_surface(self.img)
        random_pos =[]
        for tu in random.sample(mask.outline(10),4):
            random_pos.append(Gun(tu[0]+self.x,tu[1]+self.y))
        self.gun_pos = random_pos

    #크기 조정 함수
    def on_resize(self, game):
        old_boundary = self.boundary
        self.boundary = game.size
        self.load_images(self.image_path_list)
        self.change_img_size()
        self.reposition(old_boundary)
        for gun in self.gun_pos:
            gun.on_resize(game)
    def get_pos(self):
        return (self.x + (self.sx/2), self.y + (self.sy/2))

    def reposition(self, old_boundary):
        x_scale = self.x/old_boundary[0]
        y_scale = self.y/old_boundary[1]
        self.x = int(self.boundary[0] * x_scale)
        self.y = int(self.boundary[1] * y_scale)