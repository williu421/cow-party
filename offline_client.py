#############################

'This file written by William Liu, WLIU2'
import pygame
from Pieces import Piece
from pygamegame import PygameGame
from Square import Square 
import random
from Board import * 
from displayMessage import *
from OfflineBoopGame import *
from Dice import Dice 
from OfflineClientHelpers import *
from TimedScreen import *
from pprint import pprint 
from OfflineMemoryGame import *
import constants as c
pygame.font.init()

####################################
# customize these functions
####################################
class OfflineGame(PygameGame): #mimics game.py
  @staticmethod
  def modeList():
    return ['PLAY','BOOPGAME','MEMORYGAME']
  def init(self):
    OfflineGame.selectionScreen=pygame.transform.scale(
            pygame.image.load('images/selectionScreen.jpg').convert_alpha(),
            (self.width, self.height))
    OfflineGame.startScreen=pygame.transform.scale(
            pygame.image.load('images/startScreen.jpg').convert_alpha(),
            (self.width, self.height))
    OfflineGame.cowBackground=pygame.transform.scale(
            pygame.image.load('images/cowBackground.jpg').convert_alpha(),
            (self.width, self.height))
    setUpGame(self)
    self.mode = 'SELECTION' 
    ##REMINDER:/ CHANGE^ TO INTRO/ and uncomment below: 
    #self.screenGroup.add(introScreen(12000,self)) 
    self.me.PID= 'Player1'  
    self.namesDict['Player1'] = 'bob' #input('please enter your name\n') REMINDER: UNCOMMENT THIS
    self.piecesDict['Player1'] = self.me
    self.bot = Piece("Player2",14,14,False)
    self.piecesDict['Player2']  = self.bot 
    self.namesDict['Player2'] = 'CPU'
    self.PieceGroup.add(self.bot)
  def keyPressed(self,code,mod):
    if code == pygame.K_9: #for debugging 
      pprint(vars(self))
    print('mode is: ',self.mode)
    if self.displayMessage:
      if code == pygame.K_k:
        self.displayMessage=False
    if self.mode == 'MAKEBOARD': 
      if code == pygame.K_h:#help screen 
            #REMINDER: copy this over to online client 
            self.message = ["When making the custom board, use 'B','R','M' to toggle",
                            "between blue, red, and minigame squares.",
                            "Use your mouse to place the squares IN THE ORDER YOU TO MOVE IN",
                            "Press 'D' when you're done!"
                            "Press 'K' to exit this screen",]
            self.displayMessage=True
      if code == pygame.K_b:
        self.makeMode = BlueSquare
      elif code == pygame.K_r:
        self.makeMode = RedSquare
      elif code == pygame.K_m:
        self.makeMode = MiniGameSquare
      elif code == pygame.K_d:
        for piece in self.PieceGroup: 
          piece.xgrid = self.gameBoard.squareDict[0].xcoord
          piece.ygrid = self.gameBoard.squareDict[0].ycoord
        self.mode = 'INTRO'
        pygame.mixer.music.play()
        self.screenGroup.add(introScreen(7000,self))
    if self.mode == 'PLAY':
      if self.turnPlayer==self.me.PID:
    #MAKE SURE THE DICE WORKS ACROSS MULTIPLE PLAYERS
        print('pressed key on my turn')
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
              fork.moveOn(self.me,self)
          elif code==pygame.K_b:
              fork.choice=2
              msg = 'forkChoice 2 \n'
              fork.moveOn(self.me,self)
          msg='' #don't want to send message twice 
      if code == pygame.K_h:#help screen 
            #REMINDER: copy this over to online client 
            self.message = ['Welcome to Cow Party! ',
                            "On your turn, press the spacebar to roll the die",
                            "Your piece does different things based on the square you land on",
                            'Blue squares increase your bean count',
                            'Red squares decrease your bean count', 
                            'Special minigame squares start up games',
                            'Games are also played at the end of every turn',
                            'The player with the most beans at the end of the game wins!']
            self.displayMessage=True
  def timerFired(self,dt):
    if self.mode == 'INTRO':
      self.screenGroup.update(dt)
    if self.mode in OfflineGame.modeList():
      self.screenGroup.update(dt)
      self.diceGroup.update(dt)
      self.PieceGroup.update(dt,self.isKeyPressed,self.width,self.height,self.server)
      if self.mode == 'BOOPGAME' and len(self.screenGroup)==0:
        print('testing boopGame')    
        self.currentMinigame=OfflineBoopGame(1920*3//5,1200*3//5,self)
        self.minigameScores.append(dict())
        self.currentMinigame.run()
      elif self.mode == 'MEMORYGAME' and len(self.screenGroup)==0:
        print('testing OfflineMemoryGame')    
        self.currentMinigame=OfflineMemoryGame(1920*3//5,1200*3//5,self)
        self.minigameScores.append(dict())
        self.currentMinigame.run()
      elif self.mode == 'PLAY' and\
      len(self.screenGroup)==0 and len(self.diceGroup)==0 and not self.isFork:
        print('about to movecheck')
        moveCheck(self,dt)
  def mousePressed(self,x,y):
      if self.mode == 'SELECTION': 
        if 60<= x and x<=395 and 210<=y and y<= 270:
          self.mode ='INTRO'
          self.screenGroup.add(introScreen(7000,self))
          pygame.mixer.music.play() 
        elif 690<= x and x<= 1130 and 210<=y and y<= 270: 
          print('making board')
          self.mode = 'MAKEBOARD'
          self.makeMode = BlueSquare
          self.gameBoard = CustomBoard(self.height,self.width,15,15,self) 
      elif self.mode == 'MAKEBOARD': 
        makeBoardMouseHelper(self,x,y)
  def redrawAll(self,screen):
      #draw everything as same color?
      if self.mode == 'MAKEBOARD':
        drawBlankGrid(self,screen)
      if self.mode == 'SELECTION': 
        screen.blit(OfflineGame.selectionScreen,(0,0))
        Text('Welcome to the offline mode!',c.GAMEWIDTH//2,c.GAMEHEIGHT//8,c.TEXTFONT,c.TEXTCOLOR,80).draw(screen)
        Text('PLAY VS AI',c.GAMEWIDTH//5,c.GAMEHEIGHT//3,c.TEXTFONT,c.TEXTCOLOR,70).draw(screen)
        Text('CUSTOM BOARD',c.GAMEWIDTH*4//5,c.GAMEHEIGHT//3,c.TEXTFONT,c.TEXTCOLOR,70).draw(screen)
        pygame.draw.rect(screen,c.TEXTCOLOR,(60,210,395-60,270-210),5)
        pygame.draw.rect(screen,c.TEXTCOLOR,(690,210,1130-690,270-210),5)
      if self.mode=='INTRO':
        self.screenGroup.draw(screen)
        for userScreen in self.screenGroup:
          userScreen.drawText(screen)
      if self.mode in OfflineGame.modeList(): 
        screen.blit(OfflineGame.cowBackground,(0,0))
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
       # drawBeansAndCoffee(self,screen,self.width-150,self.height//30,'Player2')
        if self.movesLeft!=None:
          Text('movesLeft: %d' %(self.movesLeft),
          100,self.height//4,c.TEXTFONT,c.TEXTCOLOR,c.PLAYSIZE).draw(screen)
          Text('Turns Done: %d' %(self.gonnaBeTurn-1),
          100,self.height//4+60,c.TEXTFONT,c.TEXTCOLOR,c.PLAYSIZE).draw(screen)
      if self.mode=='LOBBY': 
          screen.blit(OfflineGame.startScreen,(0,0))
          inc = 0
          for playerID in self.namesDict:
              namesText=self.myfont.render('%s name: %s' \
              %(playerID,self.namesDict[playerID]),False,(128,255,0))
              screen.blit(namesText,(self.width/10,self.height/10+inc))
              inc += self.width/5 
      if self.displayMessage:
        displayMessage(screen,self.width/2,self.height/2,self.message,self.width,self.height) 





mygame=OfflineGame(1920*3//5,1200*3//5)
mygame.run()
