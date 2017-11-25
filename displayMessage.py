'This file written by William Liu, WLIU2'
import pygame 

def displayMessage(screen,x,y,messageList,width,height):
    s = pygame.Surface((width,height))  # the size of your rect
    s.fill((76,0,153))           # this fills the entire surface
    s.set_alpha(100)                # alpha level
    screen.blit(s, (0,0))    # (0,0) are the top-left coordinates
    nameFont=pygame.font.SysFont('Comic Sans MS', 40)
    inc = 0
    for message in messageList:
        namesText=nameFont.render('%s' \
            %(message),False,(255,255,0))
        screen.blit(namesText,(width/2-20*len(message)/2,height/2-20+inc))
        inc += height//10


