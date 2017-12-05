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
    self.bgColor=(102,255,255) 
    self.mode='LOBBY'  #LOBBY, PLAY 
    self.myfont=pygame.font.SysFont(c.TEXTFONT , c.PLAYSIZE)
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

    self.screenGroup=pygame.sprite.Group()

        #for screens that stop the flow of the game
    self.transScreenGroup=pygame.sprite.Group()
        #for screens that sit above the display, transparent
        # work for play mode only   
    self.doneReceiving = False 
    self.screenGroup=pygame.sprite.Group() 
    #for screens that stop the flow of the game 

def makeBoardMouseHelper(self,x,y): 
    for row in range(15):
        for col in range(15):
            if col*c.CELLWIDTH <= x and x<= col*c.CELLWIDTH+c.CELLWIDTH and \
            row*c.CELLHEIGHT <= y and y<= row*c.CELLHEIGHT+c.CELLHEIGHT:
                self.gameBoard.mkSq(self.makeMode,row,col,self.gameBoard.squareDict)
                print('made square')
                return 
def drawBlankGrid(self,screen):
    for square in self.gameBoard.squareDict.values():
        if isinstance(square,BlueSquare): 
            pygame.draw.rect(screen,(0,0,255),(square.xcoord*c.CELLWIDTH,square.ycoord*c.CELLHEIGHT,
            c.CELLWIDTH,c.CELLHEIGHT),0)
        elif isinstance(square,RedSquare): 
            pygame.draw.rect(screen,(255,0,0),(square.xcoord*c.CELLWIDTH,square.ycoord*c.CELLHEIGHT,
            c.CELLWIDTH,c.CELLHEIGHT),0)
        elif isinstance(square,MiniGameSquare):
            pygame.draw.rect(screen,(0,255,0),(square.xcoord*c.CELLWIDTH,square.ycoord*c.CELLHEIGHT,
            c.CELLWIDTH,c.CELLHEIGHT),0)
    for row in range(15):
        for col in range(15): 
            pygame.draw.rect(screen,(0,0,0),(col*c.CELLWIDTH,row*c.CELLHEIGHT,
            c.CELLWIDTH,c.CELLHEIGHT),5)
def nextTurn(self): #when one turn is over 
    makeNewTurn=True 
    for PID in sorted(self.piecesDict.keys()):
        if self.piecesDict[PID].turnsDone<self.gonnaBeTurn:
            makeNewTurn=False 
            print('starting turn for: ',PID)
            self.turnPlayer=PID 
            if PID == 'Player2': 
                value = random.randint(0,41)
                print('bot rolled: ',value)
                self.movesLeft=(value%6+1)              
                self.screenGroup.add(diceScreen(1000,self,value))
            else: 
                self.piecesDict[PID].myMove(self)
            break
    if makeNewTurn:
        if self.gonnaBeTurn>self.turnLimit:
            self.mode='GAMEOVER'
            pygame.mixer.music.load('audio/jingleBells.mp3')
            pygame.mixer.music.fadeout(300)
        else:
            self.gonnaBeTurn+=1
            print('made new turn, turn is: ',self.gonnaBeTurn)
def moveCheck(self,dt): 
    #check which player needs to move, if any 
    if self.movesLeft == None: #i.e. game just started 
        self.movesLeft=0
        nextTurn(self)
        return 
    if self.movesLeft == 0: 
        self.piecesDict[self.turnPlayer].turnsDone+=1 
        #signal that the previous player completed the turn
        nextTurn(self)
    else: 
        self.piecesDict[self.turnPlayer].move(self.movesLeft,self)
        self.movesLeft-=1
        self.screenGroup.add(TimedScreen(700,self))

def drawBeansAndCoffee(outerGame,screen,x,y,PID): 
    #draws the beans and coffee, duh
    piece=outerGame.piecesDict[PID]
    nameFont=pygame.font.SysFont(c.TEXTFONT , c.PLAYSIZE)
    namesText=nameFont.render('%s' \
    %(outerGame.namesDict[PID]),False,c.TEXTCOLOR)
    screen.blit(namesText,(x,y))

    screen.blit(Piece.beanImage,(x,y+50))
    namesText=nameFont.render('x %d' \
        %(piece.beans),False,c.TEXTCOLOR )
    screen.blit(namesText,(x+60,y+50))

    screen.blit(Piece.coffeeImage,(x,y+100))
    namesText=nameFont.render('x %d' \
    %(piece.coffee),False,c.TEXTCOLOR )
    screen.blit(namesText,(x+60,y+100))

    
