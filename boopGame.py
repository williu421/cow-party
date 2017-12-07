##outer framework from 112 class site

from pygamegame import PygameGame
import pygame
from displayMessage import *
import random
from pprint import pprint 
from TimedScreen import *
import constants as c
pygame.init()
pygame.font.init()

class boopGame(PygameGame):
    def __init__(self, width, height, outerGame,serverMsg=None, server=None, fps=50, title="boopGame"):
        self.outerGame=outerGame
        self.server=outerGame.server
        self.serverMsg=outerGame.serverMsg
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (102,204,0)
        self.needUserInput=False 
        self.isOuter=False
        self.timeCounter=10000 #milliseconds 
        self.boopCount=0
        image=pygame.image.load('images/boop.jpg')
        width, height = image.get_size()
        cellWidth, cellHeight = width // 2, height 
        self.boop1=image.subsurface((0,0,cellWidth,cellHeight))
        self.boop2=image.subsurface((cellWidth+10,0,cellWidth-10,cellHeight))
        self.cellWidth, self.cellHeight = cellWidth, cellHeight
        self.mode='INTRO' #switch between intro and play 
        self.ready=False
        self.otherReady=False
        self.doggo=self.boop1
        self.doggoX,self.doggoY=self.width//2-self.cellWidth//2,self.height//2-self.cellHeight//2
        self.screenGroup=pygame.sprite.Group() 
    def getRandom(self):
        self.doggoX=random.randint(0,self.width-self.cellWidth)
        self.doggoY=random.randint(0,self.height-self.cellHeight)
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
        if self.mode == 'PLAY': 
            self.noseX,self.noseY=self.doggoX+135,self.doggoY+170
            if self.noseX-60<= x and x<= self.noseX+60 and self.noseY-50<=y and y<= self.noseY+50:
                print('good hit')
                self.doggo=self.boop2
                self.boopCount+=1
    def mouseReleased(self,x,y):
        if self.doggo==self.boop2:
            self.getRandom()
        self.doggo=self.boop1
    def timerFired(self,dt):
        self.screenGroup.update(dt)
        if self.mode=='PLAY':
            self.timeCounter-=dt
            if self.timeCounter<=0:
                self.mode='GAMEOVER'
                gameOverText=Text("Game Over! Your score was %d boops"\
                %(self.boopCount),self.width//2,self.height//2,'Arial Bold',
                (153,51,255),40)
                self.screenGroup.add(TimedScreen(1000,self.outerGame,
                (102,204,0),[gameOverText]))
                msg='Score %d \n' %self.boopCount
                print('sending: ',msg)
                self.outerGame.server.send(msg.encode())
                self.outerGame.minigameScores[-1][self.outerGame.me.PID]=self.boopCount
        if self.mode=='GAMEOVER' and len(self.screenGroup)==0:
            gameExitTextList=[]
            scoresDict=self.outerGame.minigameScores[-1]
            inc=0
            #DOESN'T WORK IF WE EXPAND TO MORE THAN TWO PLAYERS
            if not (('Player1' in scoresDict) or ('Player2' in scoresDict)): 
                pass
            else:
                if scoresDict['Player1']==scoresDict['Player2']: #tie case
                    newText= Text("It's a tie! Both players had %d boops; no beans awarded"\
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
                if len(gameExitTextList)>0:
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
        screen.blit(OfflineGame.abstractOrange,(0,0))
        if len(self.screenGroup)>0:
            self.screenGroup.draw(screen)
            for userScreen in self.screenGroup:
                userScreen.drawText(screen)
        else:
            if self.mode=='INTRO':
                Text('Welcome to the Boop Game!',
                self.width//2,self.height//2-40,'Arial Bold',(0,0,0),40).draw(screen)
                Text("The goal is to boop clicking the dog's nose, as fast as possible!",
                self.width//2,self.height//2,'Arial Bold',(0,0,0),40).draw(screen)
                Text("Press 'a' when you're ready!",
                self.width//2,self.height//2+40,'Arial Bold',(0,0,0),40).draw(screen)
            if self.mode=='PLAY':
                screen.blit(self.doggo,
                (self.doggoX,self.doggoY))
                Text("Current score: %d" %(self.boopCount),
                self.width//10,self.height*3//10,'Arial Bold',(153,51,255),40).draw(screen)
                Text("Time left: %d" %((self.timeCounter)//1000),
                self.width//10,self.height//10,'Arial Bold',(153,51,255),40).draw(screen)

            