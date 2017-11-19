#############################
# Sockets Client Demo
# by Rohan Varma
# adapted by Kyle Chin
#############################

import socket
import threading
from queue import Queue

HOST = "128.237.198.124" # put your IP address here if playing on multiple computers
PORT = 50009
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
from dots import Dot
from pygamegame import PygameGame
import random
####################################
# customize these functions
####################################
class Game(PygameGame): #mimics game.py 
  def init(self):
    self.bgColor=(102,255,255)
    Dot.init()
    self.me= Dot("lonely",self.width/2,self.height/2)
    self.otherStrangers=dict()
    self.myDotGroup=pygame.sprite.Group()
    self.myDotGroup.add(self.me)
    self.otherDotGroup=pygame.sprite.Group()
  
  def keyPressed(self,code,mod):
    msg="" 
    if code == pygame.K_DOWN:
      self.me.move(0,self.me.dy)
      msg="playerMoved 0 %d\n" %(self.me.dy)
    elif code == pygame.K_UP:
      self.me.move(0,-self.me.dy)
      msg="playerMoved 0 %d\n" %(-self.me.dy)
    elif code == pygame.K_RIGHT:
      self.me.move(self.me.dx,0)
      msg="playerMoved %d 0\n" %(self.me.dx)
    elif code == pygame.K_LEFT:
      self.me.move(-self.me.dx,0)
      msg="playerMoved %d 0\n" %(-self.me.dx)
    elif code == pygame.K_SPACE:
      x = random.randint(0, self.width)
      y = random.randint(0, self.height)
      # teleport myself
      self.me.teleport(x, y)
      # update the message
      msg = "playerTeleported %d %d\n" % (x, y)

    # send the message to other players!
    if (msg != ""):
      print ("sending: ", msg,)
      self.server.send(msg.encode())
  def timerFired(self,dt):
    self.myDotGroup.update(dt,self.isKeyPressed,self.width,self.height,self.server,True) #isMe is True 
    self.otherDotGroup.update(dt,self.isKeyPressed,self.width,self.height,self.server,False)
    while (serverMsg.qsize() > 0):
      msg = serverMsg.get(False)
      try:
        print("received: ", msg, "\n")
        msg = msg.split()
        command = msg[0]

        if (command == "myIDis"):
          myPID = msg[1]
          self.me.changePID(myPID)
        elif (command == "newPlayer"):
          newPID = msg[1]
          x = self.width/2
          y = self.height/2
          self.otherStrangers[newPID] = Dot(newPID, x, y)
          self.otherDotGroup.add(self.otherStrangers[newPID])

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
      except:
        print("failed")
      serverMsg.task_done()
  def redrawAll(self,screen):
      #draw everything as same color? 
      self.myDotGroup.draw(screen)
      self.otherDotGroup.draw(screen)

##NOT TKINTER STUFF 
serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

#run(200, 200, serverMsg, server)

Game(900,900,serverMsg,server).run()
