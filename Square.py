import pygame
import math
from GameObject import GameObject
import random
class Square(GameObject): 
    margin = 10
    ordDict=dict()
    @staticmethod
    def init(gameHeight,gameWidth,colNum,rowNum):
        def loadImage(imagePath):
            return pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load(imagePath).convert_alpha(),
            (60, 60)), 0)
        Square.brownSquare = loadImage('images/brownSquare.png')
        Square.blank=loadImage('images/blank.png')
        Square.rightArrow=loadImage('images/rightArrow.png')
        Square.leftArrow=loadImage('images/leftArrow.jpeg')
        Square.upArrow=loadImage('images/upArrow.jpeg')
        Square.downArrow=loadImage('images/downArrow.jpeg')
        Square.blueSquare=loadImage('images/blueSquare.png')
        Square.redSquare=loadImage('images/redSquare.png')
        Square.greenSquare=loadImage('images/greenSquare.png')
        Square.miniGameSquare=loadImage('images/MiniGameSquare.png')
        Square.mushroomSquare=loadImage('images/MushroomSquare.png')
        Square.bowserSquare=loadImage('images/bowserSquare.png')
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
        Square.ordDict[self.ordinal]=self
    def land(self,piece,game):#when piece lands on it 
        pass
    def tap(self,piece,game):#when piece passes on it 
        pass
    def getNext(self): #return y,x coords of the next square in line 
        nextSq=Square.ordDict[(self.ordinal+1)%86]
        return nextSq.ycoord,nextSq.xcoord
class BlankSquare(Square): 
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.blank)
class RightSquare(Square):
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.rightArrow) 
    def tap(self,piece,game):
        piece.move(1,game)
class BlueSquare(Square):
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.blueSquare)
    def land(self,piece,game):
        piece.beans += 3
class RedSquare(Square): 
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.redSquare)
    def land(self,piece,game):
        piece.beans -= 3
        if piece.beans <= 0:
            piece.beans=0
class GreenSquare(Square): 
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.greenSquare)
    def land(self,piece,game):
        pass  
class MiniGameSquare(Square):
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.minigameSquare)
class MushroomSquare(Square):
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.mushroomSquare)
class BowserSquare(Square):
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.bowserSquare)