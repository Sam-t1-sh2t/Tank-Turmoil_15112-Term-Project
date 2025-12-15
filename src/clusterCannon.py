from cmu_graphics import *
import random
import math
from cannon import Cannon

class clusterCannon:
    def __init__(self,app,x,y,heading,velocity,playerIndex):
        self.draw = True
        self.spreadNum = app.spreadNum
        self.spread = []
        self.x = x
        self.y = y
        if app.gameMode == 'multi':
            self.heading = heading
            self.rotateX = -math.sin(math.radians(self.heading))
            self.rotateY = math.cos(math.radians(self.heading))
        self.velocity = velocity
        self.dx = self.velocity * self.rotateX
        self.dy = self.velocity * self.rotateY
        self.size = 8
        self.steps = 0
        self.owner = playerIndex
        self.prevCollision = None
    
    def clusterExplode(self,app):
        self.draw = False
        degree = 360/self.spreadNum
        for i in range(self.spreadNum):
            app.existingWeapons.append(Cannon(app,self.x,self.y,self.heading+degree*i,self.velocity))
    
    def moveCluster(self,app):
        if not app.gameSettlement:
            for x,y in app.collisionList:
                if x[0] == x[1] and abs(self.x-x[0])<=self.size and y[0]<=self.y<=y[1]:
                    if self.prevCollision==None:
                        self.prevCollision = (x,y)
                        self.dx = -self.dx
                    if (x,y) != self.prevCollision:
                        self.dx = -self.dx
                        self.prevCollision = (x,y)
                elif y[0] == y[1] and abs(self.y-y[0])<=self.size and x[0]<=self.x<=x[1]:
                    if self.prevCollision==None:
                        self.prevCollision = (x,y)
                        self.dy = -self.dy
                    if (x,y) != self.prevCollision:
                        self.dy = -self.dy
                        self.prevCollision = (x,y)
            self.x+=self.dx
            self.y+=self.dy
            self.steps+=1
    
        