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
from hullGame import *
pygame.font.init()


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

####################################
# customize these functions
####################################
class Game(PygameGame): #mimics game.py 
  @staticmethod
  def modeList():
    return ['PLAY','BOOPGAME','MEMORYGAME','HULLGAME']
  def init(self):
    def imageLoad(path):
      return pygame.transform.scale(
            pygame.image.load(path).convert_alpha(),
            (c.GAMEWIDTH+30, c.GAMEHEIGHT+30))
    Game.selectionScreen=imageLoad('images/selectionScreen.jpg')
    Game.redBackground=imageLoad('images/redBackground.png')
    Game.startScreen=imageLoad('images/startScreen.jpg')
    Game.woodBackground=imageLoad('images/Background.jpg')
    Game.cowBackground=imageLoad('images/cowBackground.jpg')
    Game.endScreen=imageLoad('images/santa.jpg')
    Game.cartoonBackground=imageLoad('images/cartoonBackground.jpg')
    Game.blueLightBackground=imageLoad('images/blueLightBackground.jpg')
    Game.customizeBackground=imageLoad('images/customizeBackground.jpg')
    Game.abstractOrange=imageLoad('images/abstractOrange.png')
    setUpGame(self)
    self.mode = 'LOBBY'   
  def keyPressed(self,code,mod):
    if code == pygame.K_9: #for debugging 
      pprint(vars(self))
    msg=''
    print('mode is: ',self.mode)
    if self.displayMessage:
      if code == pygame.K_h:
        self.displayMessage=False
        return 
    if self.mode == 'PLAY':
      if self.turnPlayer==self.me.PID:
        if len(self.diceGroup.sprites())>0:
            #there's a die flying around 
            dice=self.diceGroup.sprites()[0]
            if code==pygame.K_SPACE:#don't interfere with other dice 
                print('you rolled a %d!' %(dice.value%6+1))
                c.BOXINGSOUND.play(maxtime=500)
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
                            "On your turn, press the spacebar to roll the die",
                            "Your piece does different things based on the square you land on",
                            'Blue squares increase your bean count',
                            'Red squares decrease your bean count', 
                            'Special minigame squares start up games',
                            'Games are also played at the end of every turn',
                            'The player with the most beans at the end of the game wins!']
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
        self.currentMinigame=boopGame(1920*3//5,1200*3//5,self)
        self.minigameScores.append(dict())
        self.currentMinigame.run()
      elif self.mode == 'MEMORYGAME' and len(self.screenGroup)==0: 
        self.currentMinigame=memoryGame(1920*3//5,1200*3//5,self)
        self.minigameScores.append(dict())
        self.currentMinigame.run()
      elif self.mode == 'HULLGAME' and len(self.screenGroup)==0:   
        self.currentMinigame=hullGame(1920*3//5,1200*3//5,self)
        self.minigameScores.append(dict())
        self.currentMinigame.run()
      elif self.mode == 'PLAY' and\
      len(self.screenGroup)==0 and len(self.diceGroup)==0 and not self.isFork:
        moveCheck(self,dt)
    while (self.serverMsg.qsize() > 0):
      msg = self.serverMsg.get(False)
      try:
        processMessage(self,msg,c.BACKLOG)
      except Exception as e:
        print("failed")
        print(e)
      self.serverMsg.task_done()
  def redrawAll(self,screen):
      #draw everything as same color? 
      if self.mode == 'GAMEOVER':
        OVERCOLOR = (0,255,0)
        score1=self.piecesDict['Player1'].beans
        score2=self.piecesDict['Player2'].beans
        screen.blit(Game.endScreen,(0,0))
        a=Text("Game Over! Thanks for playing!",c.GAMEWIDTH//2,
        c.GAMEHEIGHT//2,'Arial Black',OVERCOLOR,60)
        a.draw(screen)
        if score1 > score2: 
          b=Text("The winner was Player1",c.GAMEWIDTH//2,
          c.GAMEHEIGHT*3//4,'Arial Black',OVERCOLOR,60)
        elif score2>score1: 
          b=Text("The winner was Player2",c.GAMEWIDTH//2,
          c.GAMEHEIGHT*3//4,'Arial Black',OVERCOLOR,60)
        elif score1==score2: 
          b=Text("Tie game",c.GAMEWIDTH//2,
          c.GAMEHEIGHT*3//4,'Arial Black',OVERCOLOR,60)
        b.draw(screen)
      if self.mode=='INTRO':
        self.screenGroup.draw(screen)
        for userScreen in self.screenGroup:
          userScreen.drawText(screen)
      if self.mode in Game.modeList(): 
        screen.blit(Game.cowBackground,(0,0))
        self.gameBoard.squareGroup.draw(screen)
        if (self.piecesDict['Player1'].xgrid!=self.piecesDict['Player2'].xgrid) or \
        (self.piecesDict['Player1'].ygrid != self.piecesDict['Player2'].ygrid):
          #basically when the players are on the same square
          self.PieceGroup.draw(screen)
          for Piece in self.PieceGroup:
            Piece.drawName(self,screen)
        else: 
          self.meGroup.draw(screen)
          self.me.drawName(self,screen)
        self.diceGroup.draw(screen)
        self.screenGroup.draw(screen)
        for userScreen in self.screenGroup:
          userScreen.drawText(screen)
        drawBeansAndCoffee(self,screen,0,0,'Player1')
        drawBeansAndCoffee(self,screen,self.width-120,0,'Player2')
        if self.movesLeft!=None:
          Text('Moves Left %d' %(self.movesLeft),
          120,self.height//4,c.NUMFONT,(255,0,0),c.PLAYSIZE).draw(screen)
          Text('Turns Done %d' %(self.gonnaBeTurn-1),
          120,self.height//4+150,c.NUMFONT,(255,0,0),c.PLAYSIZE).draw(screen)
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
'''
#run(200, 200, serverMsg, server)
HOST=c.IP
PORT = 50009
BACKLOG=2
#need to make sure host, port match the server 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST,PORT))
print("connected to server")
serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
Game(c.GAMEWIDTH,c.GAMEHEIGHT,serverMsg,server).run()'''
