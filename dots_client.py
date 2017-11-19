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
hostAddress=input("enter the host's IP address: \n")
HOST = str(hostAddress) # put your IP address here if playing on multiple computers
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
    self.me= Dot("lonely",self.width/2,self.height/2,True) #last parameter says it's me 
    self.otherStrangers=dict()
    self.dotGroup=pygame.sprite.Group()
    self.dotGroup.add(self.me)
    Game.startScreen=pygame.transform.scale(
            pygame.image.load('images/startScreen.jpg').convert_alpha(),
            (self.width, self.height))
    self.lobbyMode=True 
    self.namesDict=dict() #key is PID, value is the stringed name
  def keyPressed(self,code,mod):
    msg="" 
    if code == pygame.K_SPACE:
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
    self.dotGroup.update(dt,self.isKeyPressed,self.width,self.height,self.server)
    while (serverMsg.qsize() > 0):
      msg = serverMsg.get(False)
      try:
        processMessage(self,msg,BACKLOG)
      except:
        print("failed")
      serverMsg.task_done()
  def redrawAll(self,screen):
      #draw everything as same color? 
      self.dotGroup.draw(screen)
      if self.lobbyMode: screen.blit(Game.startScreen,(0,0))


##NOT TKINTER STUFF 
serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

#run(200, 200, serverMsg, server)

Game(1920//2,1200//2,serverMsg,server).run()
