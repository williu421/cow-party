##########################
# DOT CLASS
# by Kyle Chin
##########################
import pygame
import math
from GameObject import GameObject
import random 
class Dot(GameObject):
    @staticmethod
    def init():
        Dot.dotImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/cow.jpeg').convert_alpha(),
            (60, 100)), 0)
        Dot.squidImage=pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/Alpaca.png').convert_alpha(),
            (60, 100)), 0)
    def __init__(self, PID, x, y,isMe):
        if isMe: super(Dot, self).__init__(x, y, Dot.dotImage, 30)
        else: super(Dot, self).__init__(x, y, Dot.squidImage, 30)
        self.isMe=isMe
        self.PID = PID
        self.x = x
        self.y = y
        self.dx,self.dy=10,10
        self.size = 30

    def move(self, dx, dy):
        print("moving cow", self.PID)
        self.x += dx
        self.y += dy

    def teleport(self, x, y):
        self.x = x
        self.y = y

    def changePID(self, PID):
        self.PID = PID

    def drawDot(self, canvas, color):
        r = self.size
        canvas.create_oval(self.x-r, self.y-r, 
                           self.x+r, self.y+r, fill=color)
        canvas.create_text(self.x, self.y, text=self.PID, fill="white")
    def update(self, dt, keysDown, screenWidth, screenHeight,server):
        if self.isMe==True: #dont' want to move other people's dots 
            msg=''
            if keysDown(pygame.K_LEFT):
                self.move(-self.dx,0)
                msg="playerMoved %d 0\n" %(-self.dx)
            if keysDown(pygame.K_RIGHT):
                self.move(self.dx,0)
                msg="playerMoved %d 0\n" %(self.dx)
            if keysDown(pygame.K_UP):
                self.move(0,-self.dy)
                msg="playerMoved 0 %d\n" %(-self.dy)
            if keysDown(pygame.K_DOWN):
                self.move(0,self.dy) 
                msg="playerMoved 0 %d\n" %(self.dy)
            '''elif keysDown(pygame.K_SPACE):
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                # teleport myself
                self.teleport(x, y)
                # update the message
                msg = "playerTeleported %d %d\n" % (x, y)'''
                #don't actually want the user to hold down the space bar 

            if (msg != ""):
                print ("sending from dots file: ", msg,)
                server.send(msg.encode())
        super(Dot, self).update(screenWidth, screenHeight)



