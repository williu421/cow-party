import socket
import threading
from queue import Queue #should be 'from Queue import Queue if python2.x 
import pygame
from Pieces import Piece
from pygamegame import PygameGame
import random
from inputbox import *
import pygame_textinput

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
    elif (command == "nameVal"): 
        self.namesDict[msg[2]]=self.namesDict.get(msg[2],'') 
        #in this case, the player hosting this hasn't  seen the others yet 
        if self.namesDict[msg[2]] != '' and self.namesDict[msg[2]]!=msg[3]:
            print("bad name conflict")
        self.namesDict[msg[2]]=msg[3]
        print(self.namesDict)
    elif (command == "newPlayer"):
        newPID = msg[1]
        self.namesDict[newPID]=''
        x = 0
        y = 0
        self.otherStrangers[newPID] = Piece(newPID, x, y,False)
        self.PieceGroup.add(self.otherStrangers[newPID])
        if len(self.PieceGroup)==BACKLOG:
            self.mode = 'PLAY'
    elif (command == "playerMoved"):
        PID = msg[1]
        dx = int(msg[2])
        dy = int(msg[3])
        self.otherStrangers[PID].move(dx, dy)
    elif (command == "playerTeleported"):
        PID = msg[1]
        x = int(msg[2])
        y = int(msg[3])
        self.otherStrangers[PID].teleport(x, y)