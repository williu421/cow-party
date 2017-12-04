import pygame
import math
from GameObject import GameObject
import random
from boopGame import boopGame
class Square(GameObject): 
    margin = 10
    ordDict=dict()
    @staticmethod
    def init(gameHeight,gameWidth,colNum,rowNum,cellHeight,cellWidth):
        #ALL IMAGES COPYRIGHT OF NINTENDO 
        def loadImage(imagePath):
            return pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load(imagePath).convert_alpha(),
            (int(cellWidth), int(cellHeight))), 0)
        Square.brownSquare = loadImage('images/brownSquare.png')
        Square.blank=loadImage('images/blank.png')
        Square.rightArrow=loadImage('images/rightArrow.png')
        '''Square.leftArrow=loadImage('images/leftArrow.jpeg')
        Square.upArrow=loadImage('images/upArrow.jpeg')
        Square.downArrow=loadImage('images/downArrow.jpeg')'''
        Square.blueSquare=loadImage('images/blueSquare.png')
        Square.redSquare=loadImage('images/redSquare.png')
        Square.greenSquare=loadImage('images/greenSquare.png')
        Square.minigameSquare=loadImage('images/MiniGameSquare.png')
        Square.mushroomSquare=loadImage('images/MushroomSquare.png')
        Square.bowserSquare=loadImage('images/bowserSquare.png')
        Square.startSquare=loadImage('images/startSpace.png')
        Square.forkSquare=loadImage('images/forkSpace.png')
    def __init__(self,ycoord,xcoord,ordinal,rows,cols,boardHeight,\
    boardWidth,image,outerGame,ordDict=None): #coords are the grid locations 
        Square.margin = max(boardHeight,boardWidth)*1/10
        cellWidth=boardWidth/cols
        cellHeight=boardHeight/rows
        Square.cellWidth,Square.cellHeight=cellWidth,cellHeight
        super(Square,self).__init__(Square.margin+cellWidth*(xcoord+1/2),\
        Square.margin+cellHeight*(ycoord+1/2),\
        image,cellWidth/2)
        self.xcoord=xcoord
        self.ycoord=ycoord 
        self.outerGame=outerGame
        self.ordinal=ordinal 
        Square.ordDict[self.ordinal]=self
        self.BoardsOrdDict=ordDict
    def tap(self,piece,game,moves):#when piece passes on it 
        pass
    def getNext(self): #return y,x coords of the next square in line 
        #hardcord in some merges
        if self.BoardsOrdDict==None:
            if (self.ycoord,self.xcoord)==(13,8):
                return 14,8
            elif (self.ycoord,self.xcoord)==(13,6):
                return 14,6
            elif (self.ycoord,self.xcoord)==(14,12):
                return 14,14
            elif (self.ycoord,self.xcoord)==(3,6):
                return 1,6
            elif (self.ycoord,self.xcoord)==(14,2):
                return 14,4
            nextSq=Square.ordDict[(self.ordinal+1)%86]
        else: 
            nextSq=self.BoardsOrdDict[(self.ordinal+1)%len(self.BoardsOrdDict)]
        return nextSq.ycoord,nextSq.xcoord
class BlankSquare(Square): 
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,outerGame):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.blank,outerGame)
class ForkSquare(Square):
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,outerGame,nextOrd1,nextOrd2,dir1,dir2):
        #nextOrd1 is the ordinal of the first option, which is dir1 
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.forkSquare,outerGame)
    #self.nextOrd=nextOrd
        self.nextOrd1,self.nextOrd2=nextOrd1,nextOrd2
        self.dir1=dir1
        self.dir2=dir2
        self.choice=None #1 or 2, depending on what the user chooses 
    def tap(self,piece,game,moves):
        if game.turnPlayer==game.me.PID: 
            print('now landed on fork',self.nextOrd1,self.nextOrd2)
            self.outerGame.message=["you have reached a fork!", "press 'a' to go %s" %self.dir1,
            "press 'b' to go %s" %self.dir2]
            self.outerGame.isFork=True
            self.outerGame.displayMessage=True
        else: 
            try: 
                print('got here at try block: 0', piece.PID)
                assert(piece.PID==self.outerGame.bot.PID)
                print('now here')
                choice = random.randint(1,2)
                self.choice=choice
                print('bot chose: ', choice)
                self.moveOn(self.outerGame.bot,self.outerGame)
            except:
                print('%s landed on fork, waiting for their decision'%piece.PID)
                self.outerGame.message=["waiting on other player"] 
                self.outerGame.isFork=True
                self.outerGame.displayMessage=True
    def moveOn(self,piece,game):
        self.outerGame.isFork=False 
        self.outerGame.mode='PLAY'
        self.outerGame.displayMessage=False
        if self.choice==1:
            newSq=Square.ordDict[self.nextOrd1]
            piece.ygrid,piece.xgrid=newSq.ycoord,newSq.xcoord
            piece.updateVisual()
        elif self.choice==2: 
            newSq=Square.ordDict[self.nextOrd2]
            piece.ygrid,piece.xgrid=newSq.ycoord,newSq.xcoord
            piece.updateVisual()
        newSq.tap(piece,game,1)
    def getNext(self):
        pass
class RightSquare(Square):
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,outerGame):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.rightArrow,outerGame) 
    def tap(self,piece,game):
        piece.move(1,game)
class BlueSquare(Square):
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,outerGame,dic=None):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.blueSquare,outerGame,dic)
    '''def tap(self,piece,game,moves):
        if moves==1:
            piece.beans+=1'''
    def tap(self,piece,game,moves):
        return##REMINDER TO CHANGE THIS 
        if moves == 0:
            if game.gonnaBeTurn%2==0:
                game.mode='MEMORYGAME'
            else:
                game.mode='BOOPGAME'
class RedSquare(Square): 
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,outerGame,dic=None):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.redSquare,outerGame,dic)
    def tap(self,piece,game,moves):
        if moves == 0:
            piece.beans -= 3
            if piece.beans <= 0:
                piece.beans=0
class GreenSquare(Square): 
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,outerGame):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.greenSquare,outerGame)
    def land(self,piece,game):
        pass  
class MiniGameSquare(Square):
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,outerGame):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.minigameSquare,outerGame)

    def tap(self,piece,game,moves):
        if moves == 0:
            game.mode='BOOPGAME'

class MushroomSquare(Square):
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,outerGame):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.mushroomSquare,outerGame)
class BowserSquare(Square):
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,outerGame):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.bowserSquare,outerGame)
class StartSquare(Square): 
    def __init__(self,xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,outerGame):
        super().__init__(xcoord,ycoord,ordinal,rowNum,colNum,boardHeight,\
    boardWidth,Square.startSquare,outerGame)