import pygame
from Pieces import Piece
from pygamegame import PygameGame
from Square import Square 
import random
from Board import Board 
from displayMessage import displayMessage
from boopGame import boopGame
from Dice import Dice 
import socket
import threading
from queue import Queue #should be 'from Queue import Queue if python2.x 
from processMessage import processMessage 
import inputbox
from TimedScreen import *

def setUpGame(self):
    cols,rows=15,15
    self.gameBoard = Board(self.height,self.width,cols,rows,self) 
    #uses the Board class 
    self.bgColor=(102,255,255) 
    self.mode='LOBBY'  #LOBBY, PLAY 
    self.myfont=pygame.font.SysFont('Comic Sans MS', 40)
    self.message = '' #for displayMessage
    self.turnHold=False 
    self.displayMessage=False 
    #signals if there needs to be an overlay with a message on it 
    self.isFork=False #change to true if we're at a fork 
    self.gonnaBeTurn=1 #the turn that is about to happen
    self.turnPlayer='Player1'  
    self.movesLeft=None#how many moves the turn player has left 
    self.currentMinigame=None #the actual instance of the current minigame 
    Piece.init()
    Dice.init()

    self.namesDict=dict() #key is PID, value is the stringed name
    self.piecesDict=dict() #key is PID, value is the Piece instance 
    self.otherStrangers=dict() #keeps track of every other player 

    self.PieceGroup=pygame.sprite.Group() 
    #use Pygame's Group to update all pieces simultaneously 
    self.me= Piece("lonely",14,14,True) #last parameter says it's me 
    self.PieceGroup.add(self.me)
    self.diceGroup=pygame.sprite.Group()
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
        self.screenGroup.add(TimedScreen(1000,self))

    '''if self.mode == 'PLAY' or self.mode=='DISPLAYMESSAGE':
      newTurn = True #flag if all the pieces have moved this turn
      for PID in sorted(self.piecesDict.keys()):
        if self.piecesDict[PID].turnsDone<self.gonnaBeTurn:
            newTurn=False
            if not self.piecesDict[PID].isMyTurn: 
                #if it's not yet this piece's turn, make it its turn
                print('starting turn for: ',PID) 
                self.piecesDict[PID].myMove(self)
            self.piecesDict[PID].isMyTurn=True
            if not self.turnHold:
                print('turn for ',PID,' is over')
                self.piecesDict[PID].isMyTurn=False
                self.piecesDict[PID].turnsDone+=1
                if self.piecesDict[PID]==self.me:
                  msg='turnOver\n'
                  print ("sending: ", msg)
                  self.server.send(msg.encode())
            else: break  
      if newTurn:
        self.gonnaBeTurn+=1'''
def drawBeansAndCoffee(outerGame,screen,x,y,PID): 
    #draws the beans and coffee, duh
    piece=outerGame.piecesDict[PID]
    nameFont=pygame.font.SysFont('Comic Sans MS', 40)
    namesText=nameFont.render('%s' \
    %(outerGame.namesDict[PID]),False,(0,0,0))
    screen.blit(namesText,(x,y))

    screen.blit(Piece.beanImage,(x,y+50))
    namesText=nameFont.render('x %d' \
        %(piece.beans),False,(0,0,0))
    screen.blit(namesText,(x+60,y+50))

    screen.blit(Piece.coffeeImage,(x,y+100))
    namesText=nameFont.render('x %d' \
    %(piece.coffee),False,(0,0,0))
    screen.blit(namesText,(x+60,y+100))

    