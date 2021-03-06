##outer framework from 112 class site

from pygamegame import PygameGame
import pygame
from displayMessage import *
import random
from pprint import pprint 
from TimedScreen import *
import numpy as np
import copy
import decimal
import constants as c
import math
pygame.init()
pygame.font.init()
pygame.display.set_mode((1,1), pygame.NOFRAME)
abstractOrange=pygame.transform.scale(
            pygame.image.load('images/abstractOrange.png').convert_alpha(),
            (c.GAMEWIDTH+30, c.GAMEHEIGHT+30))
class Point(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        pygame.draw.circle(self.image, (0, 0, 255), (x,y), 25, 0)
        self.rect = self.image.get_rect()

def inPolygon(x, y, l): #return true if x,y is in the polygon l
    if (x,y) in l:
        return False
    n = len(l)
    result = False
    p1x, p1y = l[0]
    for i in range(1, n + 1):
        p2x, p2y = l[i % n]
        if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
            if p1y != p2y:
                xgood = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
            if p1x == p2x or x <= xgood:
                result = not result
        p1x, p1y = p2x, p2y
    return result
def getTriples(l):
    outSet = set()
    for a in l:
        for b in l: 
            for c in l: 
                if not ((a,b,c) in outSet or (a,c,b) in outSet or (b,a,c) in\
                outSet or (b,c,a) in outSet or (c,a,b) in outSet or (c,b,a) in outSet):
                    if a!= b and b!= c and a!=c:
                        outSet.add((a,b,c))
    return outSet
def dist(p1,p2): #return distance from p1 to p2 
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def roundHalfUp(d): #from 15-112 course notes 
        # Round to nearest with ties going away from zero.
        rounding = decimal.ROUND_HALF_UP
        # See other rounding options here:
        # https://docs.python.org/3/library/decimal.html#rounding-modes
        return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
class hullGame(PygameGame): 
    def __init__(self, width, height, outerGame,serverMsg=None, server=None, fps=50, title="hullGame"):
        self.outerGame=outerGame
        self.server=outerGame.server
        self.serverMsg=outerGame.serverMsg
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.needUserInput=False
        self.bgColor = (102,204,0)
        self.isOuter=False
        self.timeCounter=15000 #milliseconds 
        self.mode='INTRO' #switch between intro and play 
        self.ready=False
        self.otherReady=False
        self.screenGroup=pygame.sprite.Group()
        self.pointGroup=pygame.sprite.Group()
        self.convexFlag=True
        self.pointList=[]
        self.hull=[]
        self.sheepList=[]
        for _ in range(18):
            x=random.randint(50,c.GAMEWIDTH-50)
            y=random.randint(50,c.GAMEHEIGHT-50)
            self.sheepList.append((x,y))
        hullGame.grabImages()
    @staticmethod
    def grabImages():
        def imageLoad(imagePath):
            return pygame.transform.scale(
            pygame.image.load(imagePath).convert_alpha(),
            (36,36))
        hullGame.sheep=imageLoad('images/miniSheep.png')
        hullGame.dog = imageLoad('images/miniDog.png')
        hullGame.background=pygame.transform.scale(
            pygame.image.load('images/hullBackground.jpg').convert_alpha(),
            (c.GAMEWIDTH+50,c.GAMEHEIGHT+50))
    def fenceLength(self):
        d=0
        for i in range(0,len(self.hull)):
            d+=dist(self.hull[i],self.hull[(i+1)%len(self.hull)])
        return d
    def updateHull(self):
        hullPoints=copy.copy(self.pointList)
        triples=getTriples(hullPoints)
        rerun=True
        while(rerun):
            rerun=False
            for (a,b,c) in triples: 
                for pX,pY in hullPoints: 
                    if inPolygon(pX,pY,(a,b,c)):
                        rerun=True
                        hullPoints.remove((pX,pY))
        cX=(sum([point[0] for point in hullPoints])/len(hullPoints))
        cY=(sum([point[1] for point in hullPoints])/len(hullPoints)) #centroid 
        hullPoints.sort(key=lambda point: math.atan2(point[1]-cY,point[0]-cX))
        self.hull=hullPoints
    def guardedSheep(self):
        guarded = set()
        for x,y in self.sheepList:
            unguarded=True 
            for dx,dy in self.pointList:
                if dist((x,y),(dx,dy))<=50:
                    unguarded=False
            if not unguarded:
                guarded.add((x,y))
        return guarded
    def drawHull(self,screen):
        pygame.draw.polygon(screen,(213,63,233),self.hull,5)
    def keyPressed(self,code,mod):
        if code == pygame.K_0:
            self.outerGame.mode='PLAY'
            self.playing=False
        if code == pygame.K_9: #for debugging 
            pprint(vars(self))
        if code == pygame.K_u:
            if self.pointList!=[]:
                self.pointList.pop()
                self.updateHull()
        if code == pygame.K_c:
            self.convexFlag=not self.convexFlag
        if self.mode == 'INTRO':
            if code == pygame.K_a:
                self.ready=True
                msg='Ready %s \n' %self.outerGame.me.PID
                print('sending: ',msg)
                self.outerGame.server.send(msg.encode())
                if self.otherReady:
                    self.mode='PLAY'
    def mousePressed(self,x,y):
        if self.mode == 'INTRO':
            return
        if len(self.pointGroup)<21: 
            self.pointList.append((x,y))
            self.updateHull()
    

    def timerFired(self,dt):
        self.screenGroup.update(dt)
        if self.mode=='PLAY':
            self.timeCounter-=dt
            if self.timeCounter<=0:
                self.mode='GAMEOVER'
                if self.fenceLength == 0:
                    self.score=0
                else: 
                    self.score = roundHalfUp((len(self.guardedSheep())*1000/(self.fenceLength())))
                gameOverText=Text("Game Over, covered %d sheep with %d fencing"\
                %(len(self.guardedSheep()),self.fenceLength()),self.width//2,self.height//2,c.NUMFONT,
                (153,51,255),40)
                self.screenGroup.add(TimedScreen(3000,self.outerGame,
                (102,204,0),[gameOverText]))
                try:
                    self.outerGame.minigameScores[-1][self.outerGame.me.PID]=self.score
                except:
                    self.outerGame.minigameScores[-1][self.outerGame.me.PID]=0
                msg  = 'Score %d \n' %(self.score)
                print('sending: ',msg)
                self.outerGame.server.send(msg.encode())
        if self.mode=='GAMEOVER' and len(self.screenGroup)==0:
            gameExitTextList=[]
            scoresDict=self.outerGame.minigameScores[-1]
            inc=0
            #DOESN'T WORK IF WE EXPAND TO MORE THAN TWO PLAYERS
            if scoresDict['Player1']==scoresDict['Player2']: #tie case
                newText= Text("It's a tie! Both players had %d matches; no beans awarded"\
                %(scoresDict['Player1']),
                self.width//2,self.height//2-40+80*inc,'Arial Bold',(0,0,0),40)
                gameExitTextList.append(newText)
            else:
                for PID in sorted(scoresDict,key=scoresDict.get,reverse=True):
                    self.outerGame.piecesDict[PID].beans+=5-5*inc 
                    if self.outerGame.piecesDict[PID].beans<=0:
                        self.outerGame.piecesDict[PID].beans=0
                    newText= Text('Score for %s: %d, receives %d beans'\
                    %(self.outerGame.namesDict[PID],scoresDict[PID],5-5*inc),
                    self.width//2,self.height//2-40+80*inc,'Arial Bold',(0,0,0),40)
                    gameExitTextList.append(newText)
                    inc+=1
            if len(gameExitTextList)!=0:
                print('exiting minigame')
                exitScreen=TimedScreen(2000,self.outerGame,
                (153,51,255),gameExitTextList)
                self.screenGroup.add(exitScreen) 
                self.mode='FINISHED'
        if self.mode=='FINISHED' and len(self.screenGroup)==0:
            self.playing=False
            self.outerGame.mode='PLAY'
        keysDown=self.isKeyPressed
        while (self.serverMsg.qsize() > 0):
            msg = self.serverMsg.get(False)
            try:
                print("received: ", msg, "\n")
                msg = msg.split()
                command = msg[0]
                if command == 'Ready':
                    self.otherReady=True
                    if self.ready:
                        self.mode = 'PLAY'
                if command == 'Score':
                    scorePID=msg[1]
                    score = int(msg[2])
                    self.outerGame.minigameScores[-1][scorePID]=score 
            except Exception as e:
                print("failed")
                print(e)
            self.serverMsg.task_done()  
    def redrawAll(self,screen):
        if self.mode!='FINISHED':
            screen.blit(abstractOrange,(0,0))
        if len(self.screenGroup)>0:
            self.screenGroup.draw(screen)
            for userScreen in self.screenGroup:
                userScreen.drawText(screen)
        if self.mode=='INTRO':
            Text("In this game, you are a farmer who wants to protect his goods.",
            self.width//2,self.height//2-120,'Arial Bold',(0,0,0),40).draw(screen)
            Text("You have a collection of sheep that you must protect with your 20 dogs.",
            self.width//2,self.height//2-80,'Arial Bold',(0,0,0),40).draw(screen)
            Text("However, sometimes try to run, so you have to fence them in.",
            self.width//2,self.height//2-40,'Arial Bold',(0,0,0),40).draw(screen)
            Text("Use your mouse to place the dogs.",
            self.width//2,self.height//2,'Arial Bold',(0,0,0),40).draw(screen)
            Text("Make sure to put a dog near every sheep!",
            self.width//2,self.height//2+40,'Arial Bold',(0,0,0),40).draw(screen)
            Text("The game will automatically calculate the fencing you need.",
            self.width//2,self.height//2+80,'Arial Bold',(0,0,0),40).draw(screen)
            Text("Press 'a' when you're ready.",
            self.width//2,self.height//2+160,'Arial Bold',(0,0,0),40).draw(screen)
        if self.mode=='PLAY':
            screen.blit(hullGame.background,(0,0))
            for x,y in self.sheepList:
                if (x,y) in self.guardedSheep():
                    pygame.draw.circle(screen,(0,255,0),(x,y),50)
                else: 
                    pygame.draw.circle(screen,(252,217,45),(x,y),50)
                screen.blit(hullGame.sheep,(x-13,y-13))
            for x,y in self.pointList: 
                screen.blit(hullGame.dog,(x-13,y-13))
            if self.convexFlag and len(self.pointList)>=3:
                self.drawHull(screen)
            Text("Time left: %d" %((self.timeCounter)//1000),
                self.width//10,self.height//10,'Arial Bold',(153,51,255),40).draw(screen)
            try:
                Text("Points: %s" %(format(len(self.guardedSheep())*1000/(self.fenceLength()),'7.2f')),
                    self.width//10,self.height//10+30,'Arial Bold',(153,51,255),40).draw(screen)
            except:
                pass