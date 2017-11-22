##########################
# Piece CLASS
# by Kyle Chin
##########################
import pygame
from pygamegame import PygameGame
from Square import Square 
import random
from Board import Board 
from GameObject import GameObject
pygame.font.init()
class Piece(GameObject):
    @staticmethod
    def init():
        def imageLoad(imagePath):
            return pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load(imagePath).convert_alpha(),
            (60, 100)), 0)
        Piece.cowImage = imageLoad('images/cow.jpeg')
        Piece.squidImage=imageLoad('images/Alpaca.png')
        Piece.beanImage=imageLoad('images/bean.png')
        Piece.coffeeImage=imageLoad('images/coffee.jpeg')
    def __init__(self, PID, xgrid, ygrid,isMe,beans=0,coffee=0):
        xpoint=Square.margin+(xgrid+1/2)*Square.cellWidth
        ypoint=Square.margin+(ygrid+1/2)*Square.cellHeight
        if isMe: super(Piece, self).__init__(xpoint, ypoint, Piece.cowImage, 30)
        else: super(Piece, self).__init__(xpoint, ypoint, Piece.squidImage, 30)
        self.isMe=isMe
        self.PID = PID
        self.xgrid = xgrid
        self.ygrid = ygrid
        self.dx,self.dy=1,1
        self.size = 30
        self.beans=beans 
        self.coffee=0
    def move(self, moves,game):
        currSq=game.gameBoard.board[self.ygrid][self.xgrid]
        self.ygrid,self.xgrid = currSq.getNext()
        newSq=game.gameBoard.board[self.ygrid][self.xgrid]
        if moves == 0: 
            newSq.land(self,game)
        else: 
            newSq.tap(self,game) #tap if only passing on it 
            self.move(moves-1,game)
    def teleport(self, x, y):
        print("why are we teleporting")
        self.x = x
        self.y = y

    def changePID(self, PID):
        self.PID = PID

    def drawName(self,outerGame,screen):
        nameFont=pygame.font.SysFont('Comic Sans MS', 40)
        namesText=nameFont.render('%s' \
          %(outerGame.namesDict[self.PID]),False,(0,0,0))
        screen.blit(namesText,(self.x-self.size,self.y-self.size*3/2))  
    def drawBeans(self,outerGame,screen):
        screen.blit(Piece.beanImage,(self.width//15,self.height//10))
        nameFont=pygame.font.SysFont('Comic Sans MS', 40)
        namesText=nameFont.render('x %d' \
          %(self.beans),False,(0,0,0))
        screen.blit(namesText,(self.width//10+60,self.height//10))
    def drawCoffee(self,outerGame,screen):
        screen.blit(Piece.coffeeImage,(self.width//15,self.height//3))
        nameFont=pygame.font.SysFont('Comic Sans MS', 40)
        namesText=nameFont.render('x %d' \
          %(self.coffee),False,(0,0,0))
        screen.blit(namesText,(self.width//10+60,self.height//3))
    def update(self, dt, keysDown, screenWidth, screenHeight,server):
        super(Piece, self).update(screenWidth, screenHeight)



