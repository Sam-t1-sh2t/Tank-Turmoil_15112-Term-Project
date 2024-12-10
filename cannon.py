from cmu_graphics import *
import math
class Cannon:
    def __init__(self,app,x,y,heading,velocity):
        self.x = x
        self.y = y
        if app.gameMode == 'multi':
            self.heading = heading
            self.rotateX = -math.sin(math.radians(self.heading))
            self.rotateY = math.cos(math.radians(self.heading))
        else: 
            self.heading = math.degrees(heading)
            self.rotateX = -math.sin(math.radians(self.heading-90))
            self.rotateY = math.cos(math.radians(self.heading-90))
        
        self.velocity = velocity
        self.dx = self.velocity * self.rotateX
        self.dy = self.velocity * self.rotateY
        self.size = 5
        self.steps = 0
        self.draw = True
        self.prevCollision = None
    
    def addX(self,x):
        self.x += x
    
    def addY(self,y):
        self.y += y
    
    def moveCannon(self,app):
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
        # print(self.heading,self.velocity,self.rotateX,self.rotateY)
            
    
    def __eq__(self,other):
        if isinstance(other, Cannon):
            return self.x == other.x and self.y == other.y and self.dx == other.dx and self.dy == other.dy
    
    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return f'Cannon ball at {self.x},{self.y} with a horizontal velocity of {self.dx} and a vertical velocity of {self.dy}'
    