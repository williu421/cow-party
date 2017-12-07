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
from OfflineHullGame import *
import constants as c
pygame.font.init()

####################################
# customize these functions
####################################
class OfflineGame(PygameGame): #mimics game.py
  @staticmethod
  def modeList():
    return ['PLAY','BOOPGAME','MEMORYGAME','HULLGAME']
  def init(self):
    def imageLoad(path):
      return pygame.transform.scale(
            pygame.image.load(path).convert_alpha(),
            (c.GAMEWIDTH+30, c.GAMEHEIGHT+30))
    OfflineGame.selectionScreen=imageLoad('images/selectionScreen.jpg')
    OfflineGame.redBackground=imageLoad('images/redBackground.png')
    OfflineGame.startScreen=imageLoad('images/startScreen.jpg')
    OfflineGame.woodBackground=imageLoad('images/Background.jpg')
    OfflineGame.cowBackground=imageLoad('images/cowBackground.jpg')
    OfflineGame.endScreen=imageLoad('images/santa.jpg')
    OfflineGame.cartoonBackground=imageLoad('images/cartoonBackground.jpg')
    OfflineGame.blueLightBackground=imageLoad('images/blueLightBackground.jpg')
    OfflineGame.customizeBackground=imageLoad('images/customizeBackground.jpg')
    OfflineGame.abstractOrange=imageLoad('images/abstractOrange.png')
    setUpGame(self)
    self.mode = 'SELECTION' 
    ##REMINDER: uncomment below: 
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
      if code == pygame.K_h:
        self.displayMessage=False
        return
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
        self.mode = 'CUSTOMIZE'
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
      elif self.mode == 'HULLGAME' and len(self.screenGroup)==0:
        print('testing OfflineHullGame')    
        self.currentMinigame=OfflineHullGame(1920*3//5,1200*3//5,self)
        self.minigameScores.append(dict())
        self.currentMinigame.run()
      elif self.mode == 'PLAY' and\
      len(self.screenGroup)==0 and len(self.diceGroup)==0 and not self.isFork:
        print('about to movecheck')
        moveCheck(self,dt)
  def mousePressed(self,x,y):
      if self.mode == 'CUSTOMIZE': 
        if 60 <= x and x<= 395 and 110<= y and y<= 270:
          self.chosenBackground=OfflineGame.woodBackground
        elif 410 <= x and x<= 410+335 and 110<= y and y<= 270:
          self.chosenBackground = OfflineGame.blueLightBackground
        elif 760 <= x and x<= 760+335 and 110<= y and y<= 270:
          self.chosenBackground = OfflineGame.cartoonBackground
        if 194<= x and x<=950 and 380<=y and y<=415: 
          self.chosenSong='carey'
        elif 351<=x and x<=785 and 455<=y and y<= 500: 
          self.chosenSong='macdonald'
        elif 370<=x and x<=752 and 530<=y and y<= 570: 
          self.chosenSong='gorillaz'
        if self.chosenBackground!= None and self.chosenSong!=None: 
          if 482<= x and x<= 482+176 and 613<=y and y<= 613+69:
            if self.chosenSong == 'gorillaz': 
              pygame.mixer.music.load('audio/feelGoodInc.mp3')
            elif self.chosenSong == 'carey': 
              pygame.mixer.music.load('audio/carey.mp3')
            elif self.chosenSong == 'macdonald': 
              pygame.mixer.music.load('audio/macdonald.mp3') 
            self.mode = 'PLAY'#REMINDER: CHANGE TO INTRO
            #pygame.mixer.music.play(-1)
            #self.screenGroup.add(introScreen(8000,self))
      if self.mode == 'SELECTION': 
        if 60<= x and x<=395 and 210<=y and y<= 270:
          self.mode = 'CUSTOMIZE'
        elif 690<= x and x<= 1130 and 210<=y and y<= 270: 
          self.mode = 'MAKEBOARD'
          self.makeMode = BlueSquare
          self.gameBoard = CustomBoard(self.height,self.width,15,15,self) 
      elif self.mode == 'MAKEBOARD': 
        makeBoardMouseHelper(self,x,y)
  def redrawAll(self,screen):
      #draw everything as same color?
      if self.mode == 'CUSTOMIZE':
        customizecolor=(58,222,85)
        customizefont='Verdana Bold'
        framecolor=(0,0,0)
        def imageLoad(path):
            return pygame.transform.scale(
            pygame.image.load(path).convert_alpha(),
            (325,150))
        miniWood=imageLoad('images/Background.jpg')
        miniBlue=imageLoad('images/blueLightBackground.jpg')
        miniCartoon=imageLoad('images/cartoonBackground.jpg')
        screen.blit(OfflineGame.abstractOrange,(0,0)) 
        Text('Choose Background:',c.GAMEWIDTH//2,c.GAMEHEIGHT//10,customizefont,customizecolor,c.LARGEFONT).draw(screen)
        pygame.draw.rect(screen,framecolor,(60,110,395-60,270-110),0)
        pygame.draw.rect(screen,framecolor,(410,110,335,270-110),0)
        pygame.draw.rect(screen,framecolor,(760,110,335,270-110),0)
        screen.blit(miniWood,(65,115))
        screen.blit(miniBlue,(415,115))
        screen.blit(miniCartoon,(765,115))
        if self.chosenBackground == OfflineGame.woodBackground:
          pygame.draw.rect(screen,(0,255,0),(60,110,395-60,270-110),5)
        elif self.chosenBackground == OfflineGame.blueLightBackground:
          pygame.draw.rect(screen,(0,255,0),(410,110,335,270-110),5)
        elif self.chosenBackground == OfflineGame.cartoonBackground:
          pygame.draw.rect(screen,(0,255,0),(760,110,335,270-110),5)

        Text('Choose Song:',c.GAMEWIDTH//2,330,customizefont,customizecolor,c.LARGEFONT).draw(screen)
        b=Text("'All I want for Christmas is you', Mariah Carey",c.GAMEWIDTH//2,400,customizefont,(0,0,0),c.LARGEFONT)
        if self.chosenSong!='carey':
          pygame.draw.rect(screen,(15,167,172),(b.x-(b.size[0]/2),b.y-(b.size[1]/2),b.size[0],b.size[1]),0)
        else: 
          pygame.draw.rect(screen,(43,226,92),(b.x-(b.size[0]/2),b.y-(b.size[1]/2),b.size[0],b.size[1]),0)
        b.draw(screen)
        b=Text("'Old MacDonald had a farm",c.GAMEWIDTH//2,475,customizefont,(0,0,0),c.LARGEFONT)
        if self.chosenSong!='macdonald':
          pygame.draw.rect(screen,(15,167,172),(b.x-(b.size[0]/2),b.y-(b.size[1]/2),b.size[0],b.size[1]),0)
        else: 
          pygame.draw.rect(screen,(43,226,92),(b.x-(b.size[0]/2),b.y-(b.size[1]/2),b.size[0],b.size[1]),0)
        b.draw(screen)
        b=Text("'Feel Good Inc.', Gorillaz",c.GAMEWIDTH//2,550,customizefont,(0,0,0),c.LARGEFONT)
        if self.chosenSong!='gorillaz':
          pygame.draw.rect(screen,(15,167,172),(b.x-(b.size[0]/2),b.y-(b.size[1]/2),b.size[0],b.size[1]),0)
        else: 
          pygame.draw.rect(screen,(43,226,92),(b.x-(b.size[0]/2),b.y-(b.size[1]/2),b.size[0],b.size[1]),0)
        b.draw(screen)

        a=Text('PLAY',c.GAMEWIDTH//2,c.GAMEHEIGHT*9//10,customizefont,(0,0,0),2*c.LARGEFONT)
        if self.chosenBackground==None or self.chosenSong==None:
          pygame.draw.rect(screen,(15,167,172),(a.x-(a.size[0]/2),a.y-(a.size[1]/2),a.size[0],a.size[1]),0)
        else: 
          pygame.draw.rect(screen,(43,226,92),(a.x-(a.size[0]/2),a.y-(a.size[1]/2),a.size[0],a.size[1]),0)
        a.draw(screen)
      if self.mode == 'GAMEOVER':
        OVERCOLOR = (0,255,0)
        score1=self.piecesDict['Player1'].beans
        score2=self.piecesDict['Player2'].beans
        screen.blit(OfflineGame.endScreen,(0,0))
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
      if self.mode == 'MAKEBOARD':
        drawBlankGrid(self,screen)
      if self.mode == 'SELECTION':
        selectionFont=(30,85,181) 
        screen.blit(OfflineGame.redBackground,(0,0))
        Text('Welcome to the offline mode',c.GAMEWIDTH//2,c.GAMEHEIGHT//8,c.TEXTFONT,selectionFont,c.LARGEFONT).draw(screen)
        Text('PLAY VS AI',c.GAMEWIDTH//5,c.GAMEHEIGHT//3,c.TEXTFONT,selectionFont,c.LARGEFONT).draw(screen)
        Text('CUSTOM BOARD',c.GAMEWIDTH*4//5,c.GAMEHEIGHT//3,c.TEXTFONT,selectionFont,c.LARGEFONT).draw(screen)
        pygame.draw.rect(screen,selectionFont,(50,200,395-50,270-200),5)
        pygame.draw.rect(screen,selectionFont,(680,200,1130-680,270-200),5)
      if self.mode=='INTRO':
        self.screenGroup.draw(screen)
        for userScreen in self.screenGroup:
          userScreen.drawText(screen)
      if self.mode in OfflineGame.modeList(): 
        screen.blit(self.chosenBackground,(0,0))
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
       # drawBeansAndCoffee(self,screen,self.width-150,self.height//30,'Player2')
        if self.movesLeft!=None:
          Text('Moves Left %d' %(self.movesLeft),
          120,self.height//4,c.NUMFONT,(255,0,0),c.PLAYSIZE).draw(screen)
          Text('Turns Done %d' %(self.gonnaBeTurn-1),
          120,self.height//4+150,c.NUMFONT,(255,0,0),c.PLAYSIZE).draw(screen)
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

