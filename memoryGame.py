##outer framework from 112 class site

from pygamegame import PygameGame
import pygame
from displayMessage import *
import random
from pprint import pprint 
from TimedScreen import *
import numpy as np
import copy
import constants as c
pygame.init()
pygame.font.init()
pygame.display.set_mode((1,1), pygame.NOFRAME)
abstractOrange=pygame.transform.scale(
            pygame.image.load('images/abstractOrange.png').convert_alpha(),
            (c.GAMEWIDTH+30, c.GAMEHEIGHT+30))
class memoryGame(PygameGame): 
    def __init__(self, width, height, outerGame,serverMsg=None, server=None, fps=50, title="memoryGame"):
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
        memoryGame.grabImages()
        self.matchCount=0
        self.gameGrid=[([0] for _ in range(3)) for i in range(3)]
        self.initGrid()
        self.cellWidth,self.cellHeight=250,250
        self.show=None
        self.show2=None 
        self.clearedPairs=[] 
    @staticmethod
    def grabImages():
        def imageLoad(imagePath):
            return pygame.transform.scale(
            pygame.image.load(imagePath).convert_alpha(),
            (200, 200))
        memoryGame.background=pygame.transform.scale(
            pygame.image.load('images/memoryGameBackground.png').convert_alpha(),
            (c.GAMEWIDTH+30, c.GAMEHEIGHT+30))
        memoryGame.cow1=imageLoad('images/cow1.png') #image from clip art 
        memoryGame.milk=imageLoad('images/milk.png') #from clip art 
        memoryGame.poop=imageLoad('images/poop.png')
        memoryGame.grass=imageLoad('images/grass.png')
        memoryGame.brownCow=imageLoad('images/brownCow.png')
        memoryGame.door=imageLoad('images/door.png')
    
    def initGrid(self): #get a random grid of images
        grid=((memoryGame.cow1,memoryGame.cow1,memoryGame.milk),
                (memoryGame.milk,memoryGame.poop,memoryGame.grass),
                (memoryGame.grass,memoryGame.brownCow,memoryGame.brownCow))
        self.gameGrid=np.random.permutation(grid)
        self.displayGrid= [[memoryGame.door for _ in range(3)] for i in range(3)]

    def drawGrid(self,grid,screen):
        if self.show==None: 
            for row in range(len(grid)):
                for col in range(len(grid[row])):
                    screen.blit(grid[row][col],
                    (row*self.cellWidth+200,col*self.cellHeight+10))
        elif self.show!= None and self.show2 == None: 
                row1,col1=self.show 
                screen.blit(self.gameGrid[row1][col1],
                (row1*self.cellWidth+200,col1*self.cellHeight+10))
                for row in range(len(grid)):
                    for col in range(len(grid[row])):
                        if (row,col)!=(row1,col1):
                            screen.blit(grid[row][col],\
                            (row*self.cellWidth+200,col*self.cellHeight+10))
        elif self.show!= None and self.show2!= None: 
            row1,col1=self.show
            row2,col2=self.show2
            screen.blit(self.gameGrid[row1][col1],\
                (row1*self.cellWidth+200,col1*self.cellHeight+10))
            screen.blit(self.gameGrid[row2][col2],\
                            (row2*self.cellWidth+200,col2*self.cellHeight+10))
            for row in range(len(grid)):
                    for col in range(len(grid[row])):
                        if (row1,col1)!= (row,col) and (row,col)!=(row2,col2):
                            screen.blit(grid[row][col],\
                            (row*self.cellWidth+200,col*self.cellHeight+10))

    def mouseHelper(self,x,y,grid):
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if row*self.cellWidth+200 <= x and x<= (row+1)*self.cellWidth+200\
                and col*self.cellHeight+10<= y and y<= (col+1)*self.cellHeight+10:
                    return row,col
        return None 
    def keyPressed(self,code,mod):
        if code == pygame.K_0:
            self.outerGame.mode='PLAY'
            self.playing=False
        if code == pygame.K_9: #for debugging 
            pprint(vars(self))
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
        coords = self.mouseHelper(x,y,self.gameGrid)
        if coords != None: 
            row,col=coords 
            if self.show == None: 
                self.show = (row,col)
                self.screenGroup.add(TimedScreen(500,self,None,None))
            elif self.show != (row,col): 
                self.show2 = (row,col)
                self.screenGroup.add(TimedScreen(500,self,None,None))
    def timerFired(self,dt):
        self.screenGroup.update(dt)
        if len(self.screenGroup)==0: 
            if self.show!= None and self.show2!= None and\
            self.gameGrid[self.show[0]][self.show[1]]==\
            self.gameGrid[self.show2[0]][self.show2[1]]: 
                self.clearedPairs.append(self.show)
                self.clearedPairs.append(self.show2)
                self.matchCount+=1
                self.displayGrid[self.show[0]][self.show[1]] = self.gameGrid[self.show[0]][self.show[1]]
                self.displayGrid[self.show2[0]][self.show2[1]]=self.gameGrid[self.show2[0]][self.show2[1]]
                self.show,self.show2=None,None
                if len(self.clearedPairs)==8: 
                    print('game over')
            elif self.show!= None and self.show2!=None: 
                self.show,self.show2=None,None
        if self.mode=='PLAY':
            self.timeCounter-=dt
            if self.timeCounter<=0:
                self.mode='GAMEOVER'
                gameOverText=Text("Game Over! Your score was %d matches"\
                %(self.matchCount),self.width//2,self.height//2,'Arial Bold',
                (153,51,255),40)
                self.screenGroup.add(TimedScreen(1000,self.outerGame,
                (102,204,0),[gameOverText]))
            
                msg='Score %d \n' %self.matchCount
                print('sending: ',msg)
                self.outerGame.server.send(msg.encode())
                self.outerGame.minigameScores[-1][self.outerGame.me.PID]=self.matchCount
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
            if len(gameExitTextList)==1:
                print('exiting minigame')
                exitScreen=TimedScreen(1500,self.outerGame,
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
        screen.blit(abstractOrange,(0,0))
        if len(self.screenGroup)>0:
            self.screenGroup.draw(screen)
            for userScreen in self.screenGroup:
                userScreen.drawText(screen)
        if self.mode=='INTRO':
            Text('Welcome to the Memory Game!',
            self.width//2,self.height//2-40,'Arial Bold',(0,0,0),40).draw(screen)
            Text("Click on a door to see what's behind it!",
            self.width//2,self.height//2,'Arial Bold',(0,0,0),40).draw(screen)
            Text("Match as many as you can before time is out!",
            self.width//2,self.height//2+40,'Arial Bold',(0,0,0),40).draw(screen)
            Text("Press 'a' when you're ready!",
            self.width//2,self.height//2+80,'Arial Bold',(0,0,0),40).draw(screen)
        if self.mode=='PLAY':
            screen.blit(OfflineMemoryGame.background,(0,0))
            self.drawGrid(self.displayGrid,screen)
            Text("Time left: %d" %((self.timeCounter)//1000),
                self.width//10,self.height//10,'Arial Bold',(153,51,255),40).draw(screen)
            