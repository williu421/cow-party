import pygame
from Pieces import Piece
from pygamegame import PygameGame
from Square import * 
import random
from Board import * 
from displayMessage import displayMessage
from boopGame import boopGame
from Dice import Dice 
import socket
import threading
from queue import Queue #should be 'from Queue import Queue if python2.x 
from processMessage import processMessage 
from TimedScreen import *
import constants as c
def setUpGame(self):
    cols,rows=15,15
    self.gameBoard = Board(self.height,self.width,cols,rows,self) 
    #uses the Board class 
    self.bgColor=c.BGCOLOR 
    self.mode='LOBBY'  #LOBBY, PLAY 
    self.myfont=pygame.font.SysFont('Arial Bold', 70)
    self.message = '' #for displayMessage
    self.turnHold=False 
    self.displayMessage=False 
    #signals if there needs to be an overlay with a message on it 
    self.isFork=False #change to true if we're at a fork 
    self.gonnaBeTurn=1 #the turn that is about to happen
    self.turnLimit=c.TURNLIMIT
    self.turnPlayer='Player1'  
    self.movesLeft=None#how many moves the turn player has left 
    self.currentMinigame=None #the actual instance of the current minigame 
    Piece.init()
    Dice.init()

    self.namesDict=dict() #key is PID, value is the stringed name
    self.piecesDict=dict() #key is PID, value is the Piece instance 
    self.otherStrangers=dict() #keeps track of every other player
    self.minigameScores=[] #list of dicts that track the scores of the players 

    self.PieceGroup=pygame.sprite.Group() 
    #use Pygame's Group to update all pieces simultaneously 
    self.me= Piece("lonely",14,14,True) #last parameter says it's me 
    self.PieceGroup.add(self.me)
    self.diceGroup=pygame.sprite.Group()
    self.meGroup=pygame.sprite.Group()
    self.meGroup.add(self.me)
    self.screenGroup=pygame.sprite.Group()

        #for screens that stop the flow of the game
    self.transScreenGroup=pygame.sprite.Group()
        #for screens that sit above the display, transparent
        # work for play mode only   
    self.doneReceiving = False 
    self.screenGroup=pygame.sprite.Group() 
    #for screens that stop the flow of the game 


def nextTurn(self): #when one turn is over 
    makeNewTurn=True 
    for PID in sorted(self.piecesDict.keys()):
        if self.piecesDict[PID].turnsDone<self.gonnaBeTurn:
            makeNewTurn=False 
            print('starting turn for: ',PID)
            self.turnPlayer=PID 
            self.piecesDict[PID].myMove(self)
            break
    if makeNewTurn:
        if self.gonnaBeTurn>self.turnLimit:
            self.mode='GAMEOVER'
            pygame.mixer.music.load('audio/jingleBells.mp3')
            pygame.mixer.music.play()
        else:
            self.gonnaBeTurn+=1
            self.mode = c.GAMESEQ.pop()
            self.screenGroup.add(minigameScreen(2500,self))
            self.movesLeft=None
def moveCheck(self,dt): 
    #check which player needs to move, if any 
    if self.movesLeft == None: #i.e. game just started 
        self.movesLeft=0
        nextTurn(self)
        return 
    if self.movesLeft == 0: 
        self.piecesDict[self.turnPlayer].turnsDone=self.gonnaBeTurn
        #signal that the previous player completed the turn
        nextTurn(self)
    else: 
        self.piecesDict[self.turnPlayer].move(self.movesLeft,self)
        self.movesLeft-=1
        self.screenGroup.add(TimedScreen(700,self))

def drawBeansAndCoffee(outerGame,screen,x,y,PID): 
    #draws the beans and coffee, duh
    piece=outerGame.piecesDict[PID]
    nameFont=pygame.font.SysFont(c.NUMFONT , c.PLAYSIZE)
    namesText=nameFont.render('%s' \
    %(outerGame.namesDict[PID]),False,(255,0,0))
    screen.blit(namesText,(x+30,y))

    screen.blit(Piece.beanImage,(x,y+30))
    namesText=nameFont.render('x %d' \
        %(piece.beans),False,(255,0,0))
    screen.blit(namesText,(x+60,y+50))

    screen.blit(Piece.coffeeImage,(x,y+80))
    namesText=nameFont.render('x %d' \
    %(piece.coffee),False,(255,0,0) )
    screen.blit(namesText,(x+60,y+110))
    
