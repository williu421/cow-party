TEXTFONT = 'Verdana'
TEXTCOLOR = (195,27,27)
PLAYSIZE = 25
GAMEHEIGHT=1200*3//5
GAMEWIDTH=1900*3//5
MARGINRATIO = 4/5 
CELLWIDTH = GAMEWIDTH//15
CELLHEIGHT=GAMEHEIGHT//15
SQUAREMARGIN = GAMEWIDTH*1/10 
LARGEFONT = 50
TURNLIMIT = 10
IP='128.237.189.207'
INTROFONT = 'Courier New Bold'
BGCOLOR = (0,255,255)
import pygame
pygame.mixer.init()
pygame.mixer.music.load('audio/main.mp3')
BOINGSOUND=pygame.mixer.Sound('audio/boing.wav')
BOXINGSOUND=pygame.mixer.Sound('audio/boxingBell.wav')
BOXINGSOUND.set_volume(.4)
CHING=pygame.mixer.Sound('audio/ching.wav')
LAUGH=pygame.mixer.Sound('audio/laugh.wav')
AWW=pygame.mixer.Sound('audio/aww.wav')
