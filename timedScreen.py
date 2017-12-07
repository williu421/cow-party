import pygame 
from Dice import Dice
from displayMessage import * 
from pygame.surfarray import *
from pygame.locals import *
import collections
import numpy 
import constants as c
class TimedScreen(pygame.sprite.Sprite):
    def __init__(self,time,game,color=None,TextList=None,transition=False):
        super().__init__()
        self.time=time
        self.outerGame=game
        self.width,self.height=game.width,game.height
        self.x,self.y=0,0 
        self.color=color
        self.image=pygame.Surface((int(self.width),int(self.height)))
        if self.color==None: self.image.set_alpha(0) 
        else: self.image.fill(color)
        self.aliveTime=0
        self.textList=TextList
        self.rect=self.image.get_rect()
        self.transition=transition
        self.alpha=0 
        self.fires=0
    def update(self,dt):
        if self.transition: 
            self.alpha+=(100/self.time)*(dt+20)
            self.image.set_alpha(self.alpha) 
        self.aliveTime+=dt
        if self.aliveTime>=self.time:
            print('killing screen')  
            self.kill()  
    def drawText(self,screen):
        if self.textList!=None:
            for Text in self.textList:
                Text.draw(screen)
        
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

class introScreen(TimedScreen):
    def __init__(self,time,game):
        super().__init__(time,game,None,None,True)
        self.totalTime=time
        self.time=time-1000
        self.image=pygame.image.load('images/introBackground.jpg')
        self.image=pygame.transform.scale(self.image,(self.width,self.height))
        self.rect=self.image.get_rect()
        self.image.set_alpha(0)
        self.currPrint=0
        self.TextQueue=collections.deque(list("In a world of farm animals...\nyou are a cow...\nyou must defeat the alpaca.\nRules: press the space bar on your turn to roll.\nPress 'h' at any time to view the help screen."))
        self.textLength=len(self.TextQueue)
        self.leftSide=self.width//2-200 #left margin of text
        self.charInc=0
        self.lineInc=0
        self.drawList=[]
        self.charTime=0
    def update(self,dt):
        self.charTime+=dt 
        self.aliveTime+=dt
        if self.aliveTime>=self.totalTime:
            self.outerGame.screenGroup.add(introScreen2(11000,self.outerGame))
            self.kill()
        self.alpha+=(255/self.time)*(dt)
        self.image.set_alpha(self.alpha) 
        self.fires+=1
        kernel=20
        spacing=65
        fontColor=(255,128,0)
        if self.charTime>=(self.time/self.textLength):
            if len(self.TextQueue)!=0:
                char = self.TextQueue.popleft()
                if char == '\n': 
                    self.lineInc+=1
                    self.charInc=0
                    self.drawList.append(Text(self.TextQueue.popleft(),\
                    self.width//3-200+self.charInc*kernel,self.height//3+self.lineInc*spacing,c.INTROFONT,fontColor,40))
                else:
                    self.drawList.append(Text(char,
                    self.width//3-200+self.charInc*kernel,self.height//3+self.lineInc*spacing,c.INTROFONT,fontColor,40))
                self.charInc+=1
                self.charTime-=(self.time/self.textLength)
    def drawText(self,screen):
        for text in self.drawList:
            text.draw(screen)

class introScreen2(TimedScreen):
    def __init__(self,time,game):
        super().__init__(time,game,None,None,True)
        self.totalTime=time
        self.time=time-1000
        self.image=pygame.image.load('images/blueLightBackground.jpg')
        self.image=pygame.transform.scale(self.image,(self.width,self.height))
        self.rect=self.image.get_rect()
        self.image.set_alpha(255)
        self.currPrint=0
        self.TextQueue=collections.deque(list("This game is turn based, and lasts "+str(c.TURNLIMIT)+" total moves.\nThe object of the game is to collect the most beans:\nthe blue squares grant you beans,\nthe red squares make you lose beans,\nthe yellow squares enter you into a minigame,\nand the rest is up to you to figure out!"))
        self.textLength=len(self.TextQueue)
        self.leftSide=self.width//2-200 #left margin of text
        self.charInc=0
        self.lineInc=0
        self.drawList=[]
        self.charTime=0
    def update(self,dt):
        self.charTime+=dt 
        self.aliveTime+=dt
        if self.aliveTime>=self.totalTime:
            self.outerGame.mode='PLAY'
            self.kill()
        self.fires+=1
        kernel=17
        spacing=65
        fontColor=(233,89,89)
        if self.charTime>=(self.time/self.textLength):
            if len(self.TextQueue)!=0:
                char = self.TextQueue.popleft()
                if char == '\n': 
                    self.lineInc+=1
                    self.charInc=0
                    self.drawList.append(Text(self.TextQueue.popleft(),\
                    self.width//3-200+self.charInc*kernel,self.height//3+self.lineInc*spacing,c.INTROFONT,fontColor,40))
                else:
                    self.drawList.append(Text(char,
                    self.width//3-200+self.charInc*kernel,self.height//3+self.lineInc*spacing,c.INTROFONT,fontColor,40))
                self.charInc+=1
                self.charTime-=(self.time/self.textLength)
    def drawText(self,screen):
        for text in self.drawList:
            text.draw(screen)

class minigameScreen(TimedScreen):
    def __init__(self,time,game):
        super().__init__(time,game,None,None,True)
        self.time=time
        self.image=pygame.image.load('images/party.jpg')
        self.image=pygame.transform.scale(self.image,(c.GAMEWIDTH,c.GAMEHEIGHT))
        self.rect=self.image.get_rect()
        self.image.set_alpha(255)
        self.drawList=[]
        t1=Text("It's time for a CRAZYYYY MINIGAME!",c.GAMEWIDTH//2,c.GAMEHEIGHT//5,
        'Comic Sans MS Bold',(137,48,205),60)
        self.drawList.append(t1)
    def update(self,dt):
        self.aliveTime+=dt
        if self.aliveTime>=self.time:
            self.kill()  
    def drawText(self,screen):
        for text in self.drawList:
            text.draw(screen)

