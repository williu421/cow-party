#############################

'Version of the game_client meant for offline debugging'
'This file written by William Liu, WLIU2'
import pygame
from Pieces import Piece
from pygamegame import PygameGame
from Square import Square 
import random
from Board import Board 
from displayMessage import displayMessage
from boopGame import boopGame
from Dice import Dice 
pygame.font.init()
####################################
# customize these functions
####################################
class Game(PygameGame): #mimics game.py 
  def init(self):
    cols,rows=15,15
    self.gameBoard = Board(self.height,self.width,cols,rows,self)
    self.bgColor=(102,255,255)
    Piece.init()
    self.me= Piece("lonely",rows-1,cols-1,True) #last parameter says it's me 
    self.otherStrangers=dict()
    self.PieceGroup=pygame.sprite.Group()
    self.PieceGroup.add(self.me)
    Game.startScreen=pygame.transform.scale(
            pygame.image.load('images/startScreen.jpg').convert_alpha(),
            (self.width, self.height))
    Game.cowBackground=pygame.transform.scale(
            pygame.image.load('images/cowBackground.jpg').convert_alpha(),
            (self.width, self.height))
    self.namesDict=dict() #key is PID, value is the stringed name
    self.piecesDict=dict()
    self.namesDict['lonely']=self.me
    self.piecesDict['lonely']=self.me
    #WHEN MOVING TO ONLINE REMOVE THE ABOVE^
    self.myfont=pygame.font.SysFont('Comic Sans MS', 40)
    self.mode = 'PLAY'
    self.turnHold=False 
    self.message=''
    self.diceGroup=pygame.sprite.Group()
    Dice.init()
    self.isFork=False #change to true if we're at a fork 
    self.gonnaBeTurn=1 #the turn that is about to happen  
  def keyPressed(self,code,mod):
    if len(self.diceGroup.sprites())>0:
        #there's a dice flying around 
        dice=self.diceGroup.sprites()[0]
        if code==pygame.K_SPACE:
            if dice.going==False: 
                dice.piece.move(dice.value%6+1,self)
                dice.kill()
                return None
            print('landed on %d!' %(dice.value%6+1))
            dice.going=False
    if self.isFork==True: 
        if self.me.isMyTurn==False: return None 
        fork=self.gameBoard.board[self.me.ygrid][self.me.xgrid]
        if code == pygame.K_a:
            fork.choice=1
            fork.moveOn(self.me,self)
        elif code==pygame.K_b:
            fork.choice=2
            fork.moveOn(self.me,self)
    if self.displayMessage:
        if code == pygame.K_k:
            self.mode = 'PLAY'
        return None #user can't do anything else in display mode 
    if self.mode == 'PLAY':
        if code == pygame.K_h:#help screen 
            self.message = ['Welcome to Cow Party! ',
                            "This is the help screen!"]
            self.displayMessage=True
        if code == pygame.K_t:
            print('testing boopGame')    
            a=boopGame(1920*3//5,1200*3//5)
            a.run()
        msg="" 
        if code == pygame.K_RIGHT:
            self.me.move(6,self)
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
    for PID in sorted(self.piecesDict.keys()):
        if self.piecesDict[PID].turnsDone<self.gonnaBeTurn:
            if not self.piecesDict[PID].isMyTurn:
                print('starting turn for: ',PID) 
                self.piecesDict[PID].myMove(self)
            self.piecesDict[PID].isMyTurn=True
            if not self.turnHold:
                print('turn for ',PID,' is over')
                self.piecesDict[PID].isMyTurn=False
                self.piecesDict[PID].turnsDone+=1
            else: break 
 
    self.diceGroup.update(dt)
    self.PieceGroup.update(dt,self.isKeyPressed,self.width,self.height,self.server)
  def redrawAll(self,screen):
        screen.blit(Game.cowBackground,(0,0))
        self.gameBoard.squareGroup.draw(screen)
        self.PieceGroup.draw(screen)
        self.diceGroup.draw(screen)
        for Piece in self.PieceGroup: 
            Piece.drawBeans(self,screen)
            Piece.drawCoffee(self,screen)
            #Piece.drawName(self,screen)
        '''if self.lobbyMode: 
            screen.blit(Game.startScreen,(0,0))
            inc = 0
            for playerID in self.namesDict:
                namesText=self.myfont.render('%s name: %s' \
                %(playerID,self.namesDict[playerID]),False,(128,255,0))
                screen.blit(namesText,(self.width/10,self.height/10+inc))
                inc += self.width/5 '''
        if self.displayMessage:
            displayMessage(screen,self.width/2,self.height/2,self.message,self.width,self.height)




mygame=Game(1920*3//5,1200*3//5)
mygame.run()
