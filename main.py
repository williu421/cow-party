from pygamegame import PygameGame
from offline_client import * 
from game_client import *   
import constants as c
import socket 
import socket
import threading
from queue import Queue #should be 'from Queue import Queue if python2.x 

class mainGame(PygameGame):
    def init(self):
        def imageLoad(path):
            return pygame.transform.scale(
                    pygame.image.load(path).convert_alpha(),
                    (c.GAMEWIDTH+30, c.GAMEHEIGHT+30))
        mainGame.mainScreen=imageLoad('images/mainScreen.png')
        self.isOuter = False
    def mousePressed(self,x,y):
        if 40<= x and x<= 535 and 315 <= y and y <= 395:
            self.playing=False
            OfflineGame(c.GAMEWIDTH,c.GAMEHEIGHT).run()
        elif 595 <= x and x<= 1115 and 315<=y and y<= 395: 
            self.playing=False 
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((c.IP,c.PORT))
            print("connected to server")
            serverMsg = Queue(100)
            threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
            Game(c.GAMEWIDTH,c.GAMEHEIGHT,serverMsg,server).run()
    def redrawAll(self,screen):
        selectionFont=(0,0,255) 
        screen.blit(mainGame.mainScreen,(0,0))
        Text('COW PARTY',c.GAMEWIDTH//2,c.GAMEHEIGHT//8,c.TECHFONT,selectionFont,2*c.LARGEFONT).draw(screen)
        Text('ONE PLAYER',c.GAMEWIDTH//4,c.GAMEHEIGHT//2,c.TECHFONT,(175,56,199),c.LARGEFONT).draw(screen)
        Text('TWO PLAYER',c.GAMEWIDTH*3//4,c.GAMEHEIGHT//2,c.TECHFONT,(105,243,161),c.LARGEFONT).draw(screen)
        pygame.draw.rect(screen,(175,56,199),(40,315,535-40,395-315),5)
        pygame.draw.rect(screen,(105,243,161),(595,315,1115-595,395-315),5)

mygame=mainGame(c.GAMEWIDTH,c.GAMEHEIGHT)
mygame.run()
