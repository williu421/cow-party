#############################
# Sockets Client Demo
# by Rohan Varma
# adapted by Kyle Chin
# adapted again by William Liu 
#############################

import socket
import threading
from queue import Queue #should be 'from Queue import Queue if python2.x 
from processMessage import processMessage 
import inputbox
#hostAddress=input("enter the host's IP address: \n")
#HOST = str(hostAddress) # put your IP address here if playing  on multiple computers
HOST='128.237.143.116'
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
from displayMessage import displayMessage
from testGame import testGame
from Dice import Dice 
from clientHelpers import *
from timedScreen import *
from pprint import pprint 
pygame.font.init()
####################################
# customize these functions
####################################
class Game(PygameGame): #mimics game.py 
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
      if code == pygame.K_k:
        self.displayMessage=False
    if self.isFork==True: 
      print('pressed key',code,' in the isFork case')
      fork=self.gameBoard.board[self.me.ygrid][self.me.xgrid]
      if code == pygame.K_a:
          fork.choice=1
          msg='forkChoice 1 \n' 
          fork.moveOn(self.me,self)
      elif code==pygame.K_b:
          fork.choice=2
          msg = 'forkChoice 2 \n'
          fork.moveOn(self.me,self)
    if self.mode == 'PLAY':
      if self.turnPlayer==self.me.PID:
    #MAKE SURE THE DICE WORKS ACROSS MULTIPLE PLAYERS
        print('pressed key on my turn')
        if len(self.diceGroup.sprites())>0:
            #there's a die flying around 
            dice=self.diceGroup.sprites()[0]
            if code==pygame.K_SPACE:#don't interfere with other dice 
                print('you rolled a %d!' %(dice.value%6+1))
                self.movesLeft=(dice.value%6+1)
                msg='playerRolled %d \n'%(dice.value)                
                self.screenGroup.add(diceScreen(2000,self,dice.value))
                dice.kill()
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
    if self.mode=='PLAY':
      self.screenGroup.update(dt)
      self.diceGroup.update(dt)
      self.PieceGroup.update(dt,self.isKeyPressed,self.width,self.height,self.server)
      if len(self.screenGroup)==0 and len(self.diceGroup)==0 and not self.isFork:
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
      if self.mode == 'PLAY': 
        screen.blit(Game.cowBackground,(0,0))
        self.gameBoard.squareGroup.draw(screen)
        self.PieceGroup.draw(screen)
        self.diceGroup.draw(screen)
        self.screenGroup.draw(screen)
        for Piece in self.PieceGroup:
            Piece.drawName(self,screen)
        drawBeansAndCoffee(self,screen,0,0,'Player1')
        drawBeansAndCoffee(self,screen,self.width-150,self.height//30,'Player2')
      if self.mode=='LOBBY': 
          screen.blit(Game.startScreen,(0,0))
          inc = 0
          for playerID in self.namesDict:
              namesText=self.myfont.render('%s name: %s' \
              %(playerID,self.namesDict[playerID]),False,(128,255,0))
              screen.blit(namesText,(self.width/10,self.height/10+inc))
              inc += self.width/5 
      if self.displayMessage:
        displayMessage(screen,self.width/2,self.height/2,self.message,self.width,self.height) 


##NOT TKINTER STUFF 
serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

#run(200, 200, serverMsg, server)

Game(1920*3//5,1200*3//5,serverMsg,server).run()
