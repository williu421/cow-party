import pygame 
from Dice import Dice
from displayMessage import * 
class TimedScreen(pygame.sprite.Sprite):
    def __init__(self,time,game,color=None,textList=None):
        super().__init__()
        print('made TimedScreen', time)
        self.outerGame=game
        self.time=time 
        self.width,self.height=game.width,game.height
        self.x,self.y=0,0 
        self.color=color
        self.image=pygame.Surface((int(self.width),int(self.height)))
        if self.color==None: self.image.set_alpha(0) 
        else: self.image.fill(color)
        self.aliveTime=0
        self.textList=textList
        self.rect=self.image.get_rect()
    def update(self,dt):
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
        self.time=time-5000
        self.image=pygame.image.load('images/introBackground.jpg')
        self.image=pygame.transform.scale(self.image,(self.width,self.height))
        self.rect=self.image.get_rect()
        self.image.set_alpha(255)
        self.currPrint=0
        self.TextQueue=collections.deque(list("In a world of farm animals...\nyou are a cow...\nyou must defeat the alpaca.\n \
        Rules: press the space bar on your turn to roll the die.\n\
        Do as the minigames say, and you will be victorious."))
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
                    self.width//3-200+self.charInc*kernel,self.height//3+self.lineInc*spacing,"Arial Bold",fontColor,40))
                else:
                    self.drawList.append(Text(char,
                    self.width//3-200+self.charInc*kernel,self.height//3+self.lineInc*spacing,"Arial Bold",fontColor,40))
            self.charInc+=1
            self.charTime-=(self.time/self.textLength)
    def drawText(self,screen):
        for text in self.drawList:
            text.draw(screen)






