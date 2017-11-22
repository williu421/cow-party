#############################


import pygame
from Pieces import Piece
from pygamegame import PygameGame
from Square import Square 
import random
from Board import Board 
from displayMessage import displayMessage
from testGame import testGame
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
    self.lobbyMode=False 
    self.namesDict=dict() #key is PID, value is the stringed name
    self.myfont=pygame.font.SysFont('Comic Sans MS', 40)
    self.mode = 'PLAY'
    self.message=''
  def keyPressed(self,code,mod):
    if self.mode == 'DISPLAYMESSAGE':
        if code == pygame.K_k:
            self.mode = 'PLAY'
        return None #user can't do anything else in display mode 
    if self.mode == 'PLAY':
        if code == pygame.K_h:#help screen 
            self.message = ['Welcome to Cow Party! ',
                            "This is the help screen!"]
            self.mode='DISPLAYMESSAGE'
        if code == pygame.K_t:
            print('testing testGame')    
            a=testGame(1920*3//5,1200*3//5)
            a.run()
    msg="" 
    if code == pygame.K_RIGHT:
        if self.me.move(6,self):
            msg="playerMoved %d 0\n" %(self.me.dx)
    #don't actually want the user to hold down the space bar 
    '''if server != None: #basically so the offline version works 
        if (msg != ""):
            print ("sending from Pieces file: ", msg,)
            server.send(msg.encode())
    # send the message to other players!
    if (msg != ""):
      print ("sending: ", msg,)
      self.server.send(msg.encode())'''
  def timerFired(self,dt):
    self.PieceGroup.update(dt,self.isKeyPressed,self.width,self.height,self.server)
  def redrawAll(self,screen):
        self.gameBoard.squareGroup.draw(screen)
        self.PieceGroup.draw(screen)
        for Piece in self.PieceGroup: 
            Piece.drawBeans(self,screen)
            Piece.drawCoffee(self,screen)
            #Piece.drawName(self,screen)
        if self.lobbyMode: 
            screen.blit(Game.startScreen,(0,0))
            inc = 0
            for playerID in self.namesDict:
                namesText=self.myfont.render('%s name: %s' \
                %(playerID,self.namesDict[playerID]),False,(128,255,0))
                screen.blit(namesText,(self.width/10,self.height/10+inc))
                inc += self.width/5 
        if self.mode == 'DISPLAYMESSAGE':
            displayMessage(screen,self.width/2,self.height/2,self.message,self.width,self.height)




mygame=Game(1920*3//5,1200*3//5)
mygame.run()
