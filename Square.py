import pygame
import math
from GameObject import GameObject
import random

class Square(GameObject): 
    margin = 10
    @staticmethod
    def init():
        Square.brownSquare = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/brownSquare.png').convert_alpha(),
            (60, 60)), 0)
        Square.blank=pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/blank.png').convert_alpha(),
            (60, 60)), 0)
    def __init__(self,xcoord,ycoord,ordinal,rows,cols,boardHeight,\
    boardWidth,image=None): 
        Square.margin = max(boardHeight,boardWidth)*1/10
        if image == None:
            image = Square.brownSquare
        cellWidth=boardWidth/cols
        cellHeight=boardHeight/rows
        Square.cellWidth,Square.cellHeight=cellWidth,cellHeight
        super(Square,self).__init__(Square.margin+cellWidth*(xcoord+1/2),\
        Square.margin+cellHeight*(ycoord+1/2),\
        image,cellWidth/2)
        self.xcoord=xcoord
        self.ycoord=ycoord 
        self.ordinal=ordinal 

class BlankSquare(Square): 
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.blank)

