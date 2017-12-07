#############################
# From Sockets Client Demo
# by Rohan Varma
# adapted by Kyle Chin
# adapted again by William Liu 
#############################
##outer framework from 112 class site  


import socket
import threading
from queue import Queue #should be 'from Queue import Queue if python2.x 
from processMessage import processMessage 
import constants as c
#hostAddress=input("enter the host's IP address: \n")
#HOST = str(hostAddress) # put your IP address here if playing  on multiple computers

HOST=c.IP
PORT = 50009
BACKLOG=2
#need to make sure host, port match the server 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

# events-example0.py from 15-112 website
# Barebones timer, mouse, and keyboard events

import pygame
from Pieces import Piece
from pygamegame import PygameGame
from Square import Square 
import random
from Board import Board 
from displayMessage import *
from boopGame import boopGame
from Dice import Dice 
from clientHelpers import *
from TimedScreen import *
from pprint import pprint 
from memoryGame import memoryGame
pygame.font.init()
####################################
# customize these functions
####################################
class Game(PygameGame): #mimics game.py 
  @staticmethod
  def modeList():
    return ['PLAY','BOOPGAME','MEMORYGAME']
  def init(self):
    Game.startScreen=pygame.transform.scale(
            pygame.image.load('images/startScreen.jpg').convert_alpha(),
            (self.width, self.height))
    Game.cowBackground=pygame.transform.scale(
            pygame.image.load('images/cowBackground.jpg').convert_alpha(),
            (self.width, self.height))
    setUpGame(self)
  def keyPressed(self,code,mod):
    if code == pygame.K_9: #for debugging 
      pprint(vars(self))
    msg=''
    print('mode is: ',self.mode)
    if self.displayMessage:
      if code == pygame.K_h:
        self.displayMessage=False
    if self.mode == 'PLAY':
      if self.turnPlayer==self.me.PID:
        if len(self.diceGroup.sprites())>0:
            #there's a die flying around 
            dice=self.diceGroup.sprites()[0]
            if code==pygame.K_SPACE:#don't interfere with other dice 
                print('you rolled a %d!' %(dice.value%6+1))
                c.BOXINGSOUND.play()
                self.movesLeft=(dice.value%6+1)
                msg='playerRolled %d \n'%(dice.value)                
                self.screenGroup.add(diceScreen(1000,self,dice.value))
                dice.kill()
        if self.isFork==True: 
          print('pressed key',code,' in the isFork case')
          fork=self.gameBoard.board[self.me.ygrid][self.me.xgrid]
          if code == pygame.K_a:
              fork.choice=1
              msg='forkChoice 1 \n'
              print ("sending: ", msg,)
              self.server.send(msg.encode()) 
              fork.moveOn(self.me,self)
          elif code==pygame.K_b:
              fork.choice=2
              msg = 'forkChoice 2 \n'
              print ("sending: ", msg,)
              self.server.send(msg.encode())
              fork.moveOn(self.me,self)
          msg='' #don't want to send message twice 
      if code == pygame.K_h:#help screen 
            self.message = ['Welcome to Cow Party! ',
                            "This is the help screen!",
                            "Press 'k' to continue"]
            self.displayMessage=True
      # send the message to other players!
      if (msg != ""):
        print ("sending: ", msg,)
        self.server.send(msg.encode())
  def timerFired(self,dt):
    if self.mode == 'INTRO':
      self.screenGroup.update(dt)
    if self.mode in Game.modeList():
      self.screenGroup.update(dt)
      self.diceGroup.update(dt)
      self.PieceGroup.update(dt,self.isKeyPressed,self.width,self.height,self.server)
      if self.mode == 'BOOPGAME' and len(self.screenGroup)==0:
        print('testing boopGame')    
        self.currentMinigame=boopGame(1920*3//5,1200*3//5,self)
        self.minigameScores.append(dict())
        self.currentMinigame.run()
      elif self.mode == 'MEMORYGAME' and len(self.screenGroup)==0:
        print('testing memoryGame')    
        self.currentMinigame=memoryGame(1920*3//5,1200*3//5,self)
        self.minigameScores.append(dict())
        self.currentMinigame.run()
      elif self.mode == 'PLAY' and\
      len(self.screenGroup)==0 and len(self.diceGroup)==0 and not self.isFork:
        print('about to movecheck')
        moveCheck(self,dt)
    while (serverMsg.qsize() > 0):
      msg = serverMsg.get(False)
      try:
        processMessage(self,msg,BACKLOG)
      except Exception as e:
        print("failed")
        print(e)
      serverMsg.task_done()
  def redrawAll(self,screen):
      #draw everything as same color? 
      if self.mode=='INTRO':
        self.screenGroup.draw(screen)
        for userScreen in self.screenGroup:
          userScreen.drawText(screen)
      if self.mode in Game.modeList(): 
        screen.blit(Game.cowBackground,(0,0))
        self.gameBoard.squareGroup.draw(screen)
        self.PieceGroup.draw(screen)
        self.diceGroup.draw(screen)
        self.screenGroup.draw(screen)
        for userScreen in self.screenGroup:
          userScreen.drawText(screen)
        for Piece in self.PieceGroup:
            Piece.drawName(self,screen)
        drawBeansAndCoffee(self,screen,0,0,'Player1')
        drawBeansAndCoffee(self,screen,self.width-150,self.height//30,'Player2')
        if self.movesLeft!=None:
          Text('movesLeft: %d' %(self.movesLeft),
          100,self.height//4,'Arial Bold',(0,0,0),40).draw(screen)
          Text('Turns completed: %d' %(self.gonnaBeTurn-1),
          100,self.height//4+60,'Arial Bold',(0,0,0),40).draw(screen)
      if self.mode=='LOBBY': 
          screen.blit(Game.startScreen,(0,0))
          inc = 0
          for playerID in self.namesDict:
              Text('%s name: %s'%(playerID,self.namesDict[playerID]),self.width//3,self.height//10+inc,'Impact',
              c.TEXTCOLOR,70).draw(screen)
              inc += self.width/5 
      if self.displayMessage:
        displayMessage(screen,self.width/2,self.height/2,self.message,self.width,self.height) 


##NOT TKINTER STUFF 
serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

#run(200, 200, serverMsg, server)

Game(c.GAMEWIDTH,c.GAMEHEIGHT,serverMsg,server).run()
