'''This file written by William Liu, WLIU2'''


from Square import * 
import pygame
import math
from GameObject import GameObject
import random


class Board(object):
    mar=4/5 #basically only want the board to take up this much of 
                    #the screen 
    def __init__(self,gameHeight,gameWidth,colNum,rowNum,outerGame):
        Board.cols,Board.rows=colNum,rowNum
        Board.boardWidth,Board.boardHeight=gameWidth*Board.mar,gameHeight*Board.mar
        Board.cellWidth=Board.boardWidth/colNum
        Board.cellHeight=Board.boardHeight/rowNum
        Square.init(gameHeight,gameWidth,colNum,rowNum,\
        Board.cellHeight,Board.cellWidth)
        self.board = [([0]*colNum) for _ in range(rowNum)]
        self.squareGroup=pygame.sprite.Group()
        self.outerGame=outerGame
        Board.ordTrack = 0 #counts what ordinal we're making
        def mkSq(SqType,ygrid,xgrid,*args):
            self.board[ygrid][xgrid]=SqType(ygrid,xgrid,\
            Board.ordTrack,Board.rows,Board.cols,Board.boardHeight,Board.boardWidth,self.outerGame,*args)
            self.squareGroup.add(self.board[ygrid][xgrid])
            Board.ordTrack+=1
        mkSq(StartSquare,14,14)
        mkSq(BlueSquare,13,14)
        mkSq(RedSquare,12,14)
        mkSq(BlueSquare,11,14)
        mkSq(BlueSquare,9,14)
        mkSq(ForkSquare,8,14,6,39,'UP','LEFT')
        mkSq(BlueSquare,6,14)
        mkSq(BlueSquare,5,14)
        mkSq(ForkSquare,4,14,9,55,'UP','LEFT')
        mkSq(BlueSquare,2,14)
        mkSq(MiniGameSquare,1,14)
        mkSq(BlueSquare,1,13)
        mkSq(GreenSquare,1,12)
        mkSq(GreenSquare,1,11)
        mkSq(BlueSquare,1,10)
        mkSq(BlueSquare,1,9)
        mkSq(MiniGameSquare,1,8)
        mkSq(BlueSquare,1,7)
        mkSq(GreenSquare,1,6)
        mkSq(ForkSquare,1,4,64,20,'UP','DOWN')
        mkSq(MiniGameSquare,2,4)
        mkSq(RedSquare,3,4)
        mkSq(RedSquare,5,4)
        mkSq(BlueSquare,6,4)
        mkSq(GreenSquare,7,4)
        mkSq(GreenSquare,8,4)
        mkSq(BlueSquare,9,4)
        mkSq(BlueSquare,10,4)
        mkSq(BlueSquare,11,4)
        mkSq(BlueSquare,12,4)
        mkSq(BlueSquare,13,4)
        mkSq(BlueSquare,14,4)
        mkSq(BlueSquare,14,6)
        mkSq(BowserSquare,14,7)
        mkSq(BlueSquare,14,8)
        mkSq(BlueSquare,14,9)
        mkSq(BlueSquare,14,10)
        mkSq(BlueSquare,14,11)
        mkSq(BlueSquare,14,12)
        mkSq(BlueSquare,8,12)
        mkSq(BlueSquare,8,11)
        mkSq(RedSquare,8,10)
        mkSq(BlueSquare,8,9)
        mkSq(ForkSquare,8,8,49,44,'LEFT','DOWN')
        mkSq(BlueSquare,9,8)
        mkSq(BlueSquare,10,8)
        mkSq(BlueSquare,11,8)
        mkSq(BlueSquare,12,8)
        mkSq(RedSquare,13,8)
        mkSq(BlueSquare,8,7)
        mkSq(BlueSquare,9,6)
        mkSq(GreenSquare,10,6)
        mkSq(BlueSquare,11,6)
        mkSq(MiniGameSquare,12,6)
        mkSq(BlueSquare,13,6)
        mkSq(BlueSquare,4,12)
        mkSq(BlueSquare,5,11)
        mkSq(RedSquare,5,10)
        mkSq(BlueSquare,5,9)
        mkSq(BlueSquare,5,8)
        mkSq(BlueSquare,5,7)
        mkSq(BowserSquare,5,6)
        mkSq(BlueSquare,4,6)
        mkSq(BlueSquare,3,6)
        mkSq(BlueSquare,0,3)
        mkSq(MiniGameSquare,0,2)
        mkSq(BlueSquare,0,1)
        mkSq(BlueSquare,1,0)
        mkSq(BlueSquare,3,0)
        mkSq(BlueSquare,4,0)
        mkSq(RedSquare,7,0)
        mkSq(BlueSquare,8,0)
        mkSq(BlueSquare,9,0)
        mkSq(BlueSquare,10,0)
        mkSq(MiniGameSquare,11,0)
        mkSq(GreenSquare,12,0)
        mkSq(BlueSquare,13,0)
        mkSq(BlueSquare,14,0)
        mkSq(MiniGameSquare,14,1)
        mkSq(BlueSquare,14,2)

class CustomBoard(Board):
    mar=4/5
    def __init__(self,gameHeight,gameWidth,colNum,rowNum,outerGame):
        Board.cols,Board.rows=colNum,rowNum
        Board.boardWidth,Board.boardHeight=gameWidth*Board.mar,gameHeight*Board.mar
        Board.cellWidth=Board.boardWidth/colNum
        Board.cellHeight=Board.boardHeight/rowNum
        Square.init(gameHeight,gameWidth,colNum,rowNum,\
        Board.cellHeight,Board.cellWidth)
        self.board = [([0]*colNum) for _ in range(rowNum)]
        self.squareGroup=pygame.sprite.Group()
        self.outerGame=outerGame
        self.squareDict = dict()
        Board.ordTrack = 0 #counts what ordinal we're making
    def mkSq(self,SqType,ygrid,xgrid,dict):
            self.board[ygrid][xgrid]=SqType(ygrid,xgrid,\
            Board.ordTrack,Board.rows,Board.cols,Board.boardHeight,Board.boardWidth,self.outerGame,dict)
            self.squareGroup.add(self.board[ygrid][xgrid])
            self.squareDict[self.ordTrack]=self.board[ygrid][xgrid]
            Board.ordTrack+=1



