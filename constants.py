TEXTFONT = 'Arial Bold'
TEXTCOLOR = (195,27,27)
PLAYSIZE = 45
GAMEHEIGHT=1200*3//5
GAMEWIDTH=1900*3//5
MARGINRATIO = 4/5 
CELLWIDTH = GAMEWIDTH//15
CELLHEIGHT=GAMEHEIGHT//15
SQUAREMARGIN = GAMEWIDTH*1/10 

import pygame 
pygame.mixer.init()
pygame.mixer.music.load('audio/main.mp3')
BOINGSOUND=pygame.mixer.Sound('audio/boing.wav')
BOXINGSOUND=pygame.mixer.Sound('audio/boxingBell.wav')
BOXINGSOUND.set_volume(.4)
