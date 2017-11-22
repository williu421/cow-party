from pygamegame import PygameGame
import pygame
class testGame(PygameGame):
    def __init__(self, width=600, height=400,serverMsg=None, server=None, fps=50, title="112 Pygame Game"):
        self.server=server
        self.serverMsg=serverMsg
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (239,70,70)
        self.needUserInput=False 
        self.standbyColor= (239,70,70)
        self.isOuter=False
    def keyPressed(self,code,mod):
        if code == pygame.K_j:
            self.playing=False 