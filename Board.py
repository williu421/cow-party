from Square import * 
import pygame
import math
from GameObject import GameObject
import random


class Board(object):
    mar=4/5 #basically only want the board to take up this much of 
                    #the screen 
    def __init__(self,gameHeight,gameWidth,colNum=15,rowNum=15):
        Board.cols,Board.rows=colNum,rowNum
        Square.init()
        self.board = [([0]*colNum) for _ in range(rowNum)]
        self.squareGroup=pygame.sprite.Group()
        inc = 0
        for row in range(rowNum): 
                for col in range(colNum):
                    if row%2==0 and col%2==0: 
                        self.board[row][col]=\
                        Square(col,row,inc,rowNum,colNum,gameHeight*Board.mar,
                        gameWidth*Board.mar)
                        self.squareGroup.add(self.board[row][col])
                    else: 
                        self.board[row][col]=\
                        BlankSquare(col,row,inc,rowNum,colNum,gameHeight*Board.mar,
                        gameWidth*Board.mar)
                        self.squareGroup.add(self.board[row][col])
                        inc +=1 

