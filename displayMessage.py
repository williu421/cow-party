import pygame 

def displayMessage(screen,x,y,messageList,width,height):
    s = pygame.Surface((width,height))  # the size of your rect
    s.set_alpha(200)                # alpha level
    s.fill((102,204,0))           # this fills the entire surface
    screen.blit(s, (0,0))    # (0,0) are the top-left coordinates
    nameFont=pygame.font.SysFont('Comic Sans MS', 40)
    inc = 0
    for message in messageList:
        namesText=nameFont.render('%s' \
            %(message),False,(0,0,0))
        screen.blit(namesText,(width/2-20*len(message)/2,height/2-20+inc))
        inc += height//10

    namesText=nameFont.render('press "k" to continue',False,(0,0,0))
    screen.blit(namesText,(width/5,height/5))

