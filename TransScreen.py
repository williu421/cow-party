import pygame 
from Dice import Dice
from displayMessage import * 
from pygame.surfarray import *
from pygame.locals import *
import collections
import numpy 

class TransScreen(pygame.sprite.sprite):
    def __init__(self,game): 
        self.outerGame=game
        self.width,self.height=game.width,game.height
        self.x,self.y=0,0
        self.color=(204,0,204)#purple
        self.image=pygame.Surface((int(self.width),int(self.height)))
        self.image.set_alpha(100) 
        self.rect=self.image.get_rect()
    def update(self,dt):
        pass
    def drawText(self,screen):
        pass 
class HelpScreen(TransScreen):
    def __init__(self,game):
        super().__init__(self,game)
    def drawText(self,screen):
        t1=Text("Welcome ")