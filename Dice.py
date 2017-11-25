'Adapted from Explosion class by Lukas Peraza'

import pygame
import random
class Dice(pygame.sprite.Sprite):
    @staticmethod
    def init():
        image = pygame.image.load('images/diceSheet.png')
        rows, cols = 7, 6
        width, height = image.get_size()
        cellWidth, cellHeight = width / cols, height / rows
        Dice.frames = []
        for i in range(rows):
            for j in range(cols):
                subImage = image.subsurface(
                    (j * cellWidth, i * cellHeight, cellWidth, cellHeight))
                Dice.frames.append(subImage)
    def __init__(self, x, y,piece):
        super(Dice, self).__init__()
        self.x, self.y = x, y
        self.piece=piece
        self.frame = 0
        self.frameRate = 10
        self.aliveTime = 0
        self.updateImage()
        self.fires=0
        self.value=1
        self.going=True #when the crap is still spinning 
    def updateImage(self):
        self.value=random.randint(0,41)
        self.image = Dice.frames[self.value]
        w, h = self.image.get_size()
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)
    def update(self, dt):
        self.fires+=1
        if self.fires%2==0 and self.going==True:
            self.updateImage()