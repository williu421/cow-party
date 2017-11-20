#############################
# Sockets Client Demo
# by Rohan Varma
# adapted by Kyle Chin
#############################

import socket
import threading
from queue import Queue #should be 'from Queue import Queue if python2.x 
from processMessage import processMessage 
import inputbox
#hostAddress=input("enter the host's IP address: \n")
#HOST = str(hostAddress) # put your IP address here if playing  on multiple computers
HOST='128.237.170.84'
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
pygame.font.init()
####################################
# customize these functions
####################################
class Game(PygameGame): #mimics game.py 
  def init(self):
    cols,rows=15,15
    self.gameBoard = Board(self.height,self.width,cols,rows)
    self.bgColor=(102,255,255)
    Piece.init()
    self.me= Piece("lonely",0,0,True) #last parameter says it's me 
    self.otherStrangers=dict()
    self.PieceGroup=pygame.sprite.Group()
    self.PieceGroup.add(self.me)
    Game.startScreen=pygame.transform.scale(
            pygame.image.load('images/startScreen.jpg').convert_alpha(),
            (self.width, self.height))
    self.lobbyMode=True  
    self.namesDict=dict() #key is PID, value is the stringed name
    self.myfont=pygame.font.SysFont('Comic Sans MS', 40)
  def keyPressed(self,code,mod):
    if code == pygame.K_SEMICOLON:
      pygame.quit()
    msg="" 
    if code == pygame.K_LEFT:
        if self.me.move(-self.me.dx,0):
            msg="playerMoved %d 0\n" %(-self.me.dx)
    if code == pygame.K_RIGHT:
        if self.me.move(self.me.dx,0):
            msg="playerMoved %d 0\n" %(self.me.dx)
    if code == pygame.K_UP:
        if self.me.move(0,-self.me.dy):
            msg="playerMoved 0 %d\n" %(-self.me.dy)
    if code == pygame.K_DOWN:
        if self.me.move(0,self.me.dy):
            msg="playerMoved 0 %d\n" %(self.me.dy)
    # send the message to other players!
    if (msg != ""):
      print ("sending: ", msg,)
      self.server.send(msg.encode())
  def timerFired(self,dt):
    self.PieceGroup.update(dt,self.isKeyPressed,self.width,self.height,self.server)
    while (serverMsg.qsize() > 0):
      msg = serverMsg.get(False)
      try:
        processMessage(self,msg,BACKLOG)
      except:
        print("failed")
      serverMsg.task_done()
  def redrawAll(self,screen):
      #draw everything as same color? 
      self.gameBoard.squareGroup.draw(screen)
      self.PieceGroup.draw(screen)
      for Piece in self.PieceGroup:
          Piece.drawName(self,screen)
      if self.lobbyMode: 
          screen.blit(Game.startScreen,(0,0))
          inc = 0
          for playerID in self.namesDict:
              namesText=self.myfont.render('%s name: %s' \
              %(playerID,self.namesDict[playerID]),False,(128,255,0))
              screen.blit(namesText,(self.width/10,self.height/10+inc))
              inc += self.width/5 


##NOT TKINTER STUFF 
serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

#run(200, 200, serverMsg, server)

Game(1920//2,1200//2,serverMsg,server).run()
