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
        Piece.cowImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/cow.jpeg').convert_alpha(),
            (60, 100)), 0)
        Piece.squidImage=pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/Alpaca.png').convert_alpha(),
            (60, 100)), 0)
    def __init__(self, PID, xgrid, ygrid,isMe):
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
    def move(self, dx, dy,game):
        if (self.xgrid+dx >= Board.cols or self.xgrid+dx<0 or self.ygrid+dy<0 or \
        self.ygrid >= Board.rows):
            return False 
        self.xgrid += dx
        self.ygrid += dy
        game.gameBoard.board[self.ygrid][self.xgrid].interact(self,game) #if special square
        self.x=Square.margin+(self.xgrid+1/2)*Square.cellWidth
        self.y=Square.margin+(self.ygrid+1/2)*Square.cellHeight
        return True 

    def teleport(self, x, y):
        self.x = x
        self.y = y

    def changePID(self, PID):
        self.PID = PID

    def drawName(self,outerGame,screen):
        nameFont=pygame.font.SysFont('Comic Sans MS', 40)
        namesText=nameFont.render('%s' \
          %(outerGame.namesDict[self.PID]),False,(0,0,0))
        screen.blit(namesText,(self.x-self.size,self.y-self.size*3/2))
    def update(self, dt, keysDown, screenWidth, screenHeight,server):
        super(Piece, self).update(screenWidth, screenHeight)



