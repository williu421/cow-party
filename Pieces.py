##########################
# Based on the Piece CLASS
# by Kyle Chin
##outer framework from 112 class site
##########################
import pygame
from pygamegame import PygameGame
from Square import Square 
import random
from Board import Board 
from GameObject import GameObject
from Dice import Dice 
from TimedScreen import *
pygame.font.init()
class Piece(GameObject):
    @staticmethod
    def init():
        def imageLoad(imagePath):
            return pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load(imagePath).convert_alpha(),
            (60, 60)), 0)
        Piece.cowImage = imageLoad('images/cow.jpeg')
        Piece.squidImage=imageLoad('images/Alpaca.png')
        Piece.beanImage=imageLoad('images/bean.png')
        Piece.coffeeImage=imageLoad('images/coffee.jpeg')
    def __init__(self, PID, xgrid, ygrid,isMe,beans=0,coffee=0):
        xpoint=Square.margin+(xgrid+1/2)*Board.cellWidth
        ypoint=Square.margin+(ygrid+1/2)*Board.cellHeight
        if isMe: super(Piece, self).__init__(xpoint, ypoint, Piece.cowImage, 30)
        else: super(Piece, self).__init__(xpoint, ypoint, Piece.squidImage, 30)
        self.isMe=isMe
        self.isMyTurn=False 
        self.PID = PID
        self.xgrid = xgrid
        self.ygrid = ygrid
        self.dx,self.dy=1,1
        self.size = 30
        self.beans=beans 
        self.coffee=0
        self.turnsDone = 0#the number of turns this guy has completed 
        self.movesLeft=0 #for moving around the board
    def myMove(self,game): 
        #game.turnHold=True 
        if self==game.me: 
            print("that's me")
        game.diceGroup.add(Dice(game.width//2,game.height//2,self))
    def move(self, moves,game):
        print('moving with: ',moves)
        currSq=game.gameBoard.board[self.ygrid][self.xgrid]
        self.ygrid,self.xgrid = currSq.getNext()
        newSq=game.gameBoard.board[self.ygrid][self.xgrid]
        self.x=Square.margin+(self.xgrid+1/2)*Board.cellWidth
        self.y=Square.margin+(self.ygrid+1/2)*Board.cellHeight
        print(self.ygrid,self.xgrid,newSq.ordinal)
        newSq.tap(self,game,moves-1) 
    def changePID(self, PID):
        self.PID = PID
    def updateVisual(self):
        self.x=Square.margin+(self.xgrid+1/2)*Board.cellWidth
        self.y=Square.margin+(self.ygrid+1/2)*Board.cellHeight
    def drawName(self,outerGame,screen):
        nameFont=pygame.font.SysFont('Comic Sans MS', 40)
        namesText=nameFont.render('%s' \
          %(outerGame.namesDict[self.PID]),False,(0,0,0))
        screen.blit(namesText,(self.x-self.size,self.y-self.size*3/2))  
    def drawBeans(self,outerGame,screen):
        screen.blit(Piece.beanImage,(outerGame.width//30,outerGame.height//30))
        nameFont=pygame.font.SysFont('Comic Sans MS', 40)
        namesText=nameFont.render('x %d' \
          %(self.beans),False,(0,0,0))
        screen.blit(namesText,(outerGame.width//30+60,outerGame.height//30))
    def drawCoffee(self,outerGame,screen):
        screen.blit(Piece.coffeeImage,(outerGame.width//30,outerGame.height//7))
        nameFont=pygame.font.SysFont('Comic Sans MS', 40)
        namesText=nameFont.render('x %d' \
          %(self.coffee),False,(0,0,0))
        screen.blit(namesText,(outerGame.width//30+60,outerGame.height//7))
    def update(self, dt, keysDown, screenWidth, screenHeight,server):
        super(Piece, self).update(screenWidth, screenHeight)



