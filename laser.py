from cmu_graphics import *
from segments import Segment
import math
class Laser:
    def __init__(self,app,x,y,heading):
        self.x = x
        self.y = y
        if app.gameMode == 'multi':
            self.heading = heading
            self.rotateX = -math.sin(math.radians(self.heading))
            self.rotateY = math.cos(math.radians(self.heading))
        self.maximumDist = 1000
        self.currDist = 0
        self.laserWidth = 5
        self.color = 'red'
        self.flyTime = 1 #second
        self.velocity = 5
        self.dx = self.velocity * self.rotateX
        self.dy = self.velocity * self.rotateY
        self.tempdx = self.dx
        self.tempdy = self.dy
        self.draw = True
        self.prevCollision = None
        # print(app.collisionList)
        self.pointCollisionL = []
        self.segments = self.setupSegments(app)
        
        # self.setupCollision()
        
    
    # def setupCollision(self):
    #     for segment in self.segments:
    #         point0, point1 = segment[0],segment[1]
    #         x0,y0,x1,y1 = point0[0],point0[1],point1[0],point1[1]
    #         dist = distance(x0,y0,x1,y1)
    #         count = int(dist/self.velocity)
    #         for i in range(count):
    #             x = x0+segment[2]*i
    #             y = y0+segment[3]*i
    #             self.pointCollisionL.append((x,y))

            
        
    

    def setupSegments(self,app):
        #backtracking?
        # segments = []
        # maxDist = self.maximumDist
        # listLen = self.flyTime*app.stepsPerSecond
        return self.segmentHelper(app,(self.x,self.y),(self.x,self.y),0,[],True)
 
    def segmentHelper(self,app,currPoint,prevPoint,dist,segments,neverCollided):
        if dist>=self.maximumDist:
            if neverCollided:
                segments.append((prevPoint,currPoint,self.dx,self.dy))
                self.tempdx = self.tempdx
                self.tempdy = self.tempdy
            return segments
        else:
            if self.checkCollision(app,prevPoint,currPoint):
                neverCollided = False
                if currPoint!=prevPoint:
                    segments.append((prevPoint,currPoint,self.dx,self.dy))
                    prevPoint = currPoint
                    self.tempdx = self.tempdx
                self.tempdy = self.tempdy
            currPoint = (currPoint[0]+self.dx,currPoint[1]+self.dy)
            self.pointCollisionL.append(currPoint)
            dist+=self.velocity
            return self.segmentHelper(app,currPoint,prevPoint,dist,segments,neverCollided)
    
    def checkCollision(self,app,prevPoint,currPoint):
        collided = False
        # print(currPoint,self.dx,self.dy)
        for x,y in app.collisionList:
            if x[0] == x[1] and abs(currPoint[0]-x[0])<=abs(self.dx) and y[0]<=currPoint[1]<=y[1]:
                # print(x,y)
                collided = True
                if self.prevCollision==None:
                    self.prevCollision = (x,y)
                    self.dx = -self.dx
                if (x,y) != self.prevCollision:
                    self.dx = -self.dx
                    self.prevCollision = (x,y)
            elif y[0] == y[1] and abs(currPoint[1]-y[0])<=abs(self.dy) and x[0]<=currPoint[0]<=x[1]:
                # print(x,y)
                collided = True
                if self.prevCollision==None:
                    self.prevCollision = (x,y)
                    self.dy = -self.dy
                if (x,y) != self.prevCollision:
                    self.dy = -self.dy
                    self.prevCollision = (x,y)
        return collided
            
def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

