'This file written by William Liu, WLIU2'
import socket
import threading
from queue import Queue #should be 'from Queue import Queue if python2.x 
import pygame
from Pieces import Piece
from pygamegame import PygameGame
import random
from TimedScreen import *
from displayMessage import *

def namesCheck(self,BACKLOG): 
    if self.doneReceiving:
        return 
    flag=True
    for i in range(1,BACKLOG+1):
        if self.namesDict['Player%d'%i]=='':
            flag = False
            break
    if flag: 
        self.doneReceiving=True 
        self.mode='INTRO'
        self.screenGroup.add(introScreen(12000,self))
def processMessage(self, msg,BACKLOG):
    print("received: ", msg, "\n")
    msg = msg.split()
    command = msg[0]
    if (command == "myIDis"):
        myPID = msg[1]
        self.me.changePID(myPID)
        self.needUserInput=True #stop the program for a second 
        myName=input("Enter your name: \n")
        self.namesDict[myPID]=myName
        self.piecesDict[myPID]=self.me
        self.needUserInput=False 
        myMsg='newName %s %s\n'%(myPID, myName)
        print("sending: ",myMsg,)
        self.server.send(myMsg.encode())
    elif (command == "newName"): #update our dictionary and push it to everyone 
        namePID = msg[2]
        newName = msg[3] 
        self.namesDict[namePID]=newName 
        for playerPID in self.namesDict: 
            myMsg = 'nameVal %s %s\n'%(playerPID,self.namesDict[playerPID])
            print("sending: ", myMsg,)
            self.server.send(myMsg.encode())
        namesCheck(self,BACKLOG)
    elif (command == "nameVal"): 
        self.namesDict[msg[2]]=self.namesDict.get(msg[2],'') 
        #in this case, the player hosting this hasn't  seen the others yet 
        if self.namesDict[msg[2]] != '' and self.namesDict[msg[2]]!=msg[3]:
            print("bad name conflict")
        self.namesDict[msg[2]]=msg[3]
        namesCheck(self,BACKLOG)
    elif (command == "newPlayer"):
        newPID = msg[1]
        self.namesDict[newPID]=''
        self.piecesDict[newPID] = Piece(newPID, 14,14,False)
        self.PieceGroup.add(self.piecesDict[newPID])
    elif (command == "playerMoved"):
        PID = msg[1]
        val = int(msg[2])
        self.piecesDict[PID].move(val.self)
    elif (command == 'playerRolled'):
        PID=msg[1]
        val=int(msg[2])
        self.movesLeft=(val%6+1)
        self.diceGroup.empty()
        self.screenGroup.add(diceScreen(1000,self,val))
    elif (command == 'forkChoice'):
        PID=msg[1]
        choice=int(msg[2])
        piece=self.piecesDict[PID]
        fork = self.gameBoard.board[piece.ygrid][piece.xgrid]
        fork.choice=choice
        fork.moveOn(piece,self)
    elif command=='turnOver':
        self.turnHold=False