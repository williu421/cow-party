'This file written by William Liu, WLIU2'
import pygame 

class Text: #from https://stackoverflow.com/questions/32673965/pygame-blitting-center
    # Constructror
    def __init__(self,text,x,y,fontChoice,color,fontSize):
        self.x = x #Horizontal center of box
        self.y = y #Vertical center of box
        # Start PyGame Font
        pygame.font.init()
        font = pygame.font.SysFont(fontChoice, fontSize)
        self.txt = font.render(text, True, color)
        self.size = font.size(text) #(width, height)
    # Draw Method
    def Draw(self, screen):
        drawX = self.x - (self.size[0] / 2.)
        drawY = self.y - (self.size[1] / 2.)
        coords = (drawX, drawY)
        screen.blit(self.txt, coords)

def displayMessage(screen,x,y,messageList,width,height):
    s = pygame.Surface((width,height))  # the size of your rect
    s.fill((76,0,153))           # this fills the entire surface
    s.set_alpha(100)                # alpha level
    screen.blit(s, (0,0))    # (0,0) are the top-left coordinates
    nameFont=pygame.font.SysFont('Comic Sans MS', 40)
    inc = 0
    for message in messageList:
        Text(message,
            width//2,height//2-len(messageList)//2*40+inc,
            'Arial Bold',(255,255,0),40).Draw(screen)
        inc += 40

