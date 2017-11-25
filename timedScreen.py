import pygame 
from Dice import Dice
from displayMessage import * 
class TimedScreen(pygame.sprite.Sprite):
    def __init__(self,time,game,color=None):
        super().__init__()
        print('made TimedScreen', time)
        self.time=time 
        self.width,self.height=game.width,game.height
        self.x,self.y=0,0 
        self.color=color
        self.image=pygame.Surface((int(self.width),int(self.height)))
        if self.color==None: self.image.set_alpha(0) 
        else: self.image.fill(color)
        self.aliveTime=0
        self.rect = self.image.get_rect()
    def update(self,dt):
        self.aliveTime+=dt
        if self.aliveTime>=self.time:
            print('killing screen')  
            self.kill()  

class diceScreen(TimedScreen): 
    def __init__(self,time,game,value):
        super().__init__(time,game)
        self.x,self.y=game.width//2,game.height//2
        self.image.fill((76,153,0))
        self.image.set_alpha(100)
        self.value=value 
        self.image = Dice.frames[self.value]
        w, h = self.image.get_size()
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)




