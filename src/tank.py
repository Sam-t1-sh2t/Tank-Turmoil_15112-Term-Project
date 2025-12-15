from cmu_graphics import *
import math
class Tank:
    def __init__(self,app,playerIndex,tankSpeed,turnSpeed): 
        self.scores = 0
        self.speed = tankSpeed
        self.turnSpeed = turnSpeed
        self.tankReset(app,playerIndex)
        self.weaponType = 'cannon'
    
    def tankReset(self,app,playerIndex):
        if playerIndex == 0: #this is the player in solo mode
            self.x,self.y = 50,50
            self.heading = 0  #0 is down, 90 is left, 180 is up, 270 is right
            self.index = playerIndex
            if app.gameMode == 'multi':
                self.aimMode = 'tank-sync'
                self.color = 'blue'
            else:
                self.aimMode = 'cursor'
                self.color = 'blue'
        else: #this is the bot in solo mode
            self.x,self.y = app.width-50,app.height-50
            self.heading = 180
            self.index = playerIndex
            self.aimMode = 'tank-sync'
            self.color = 'yellow'
        self.dx = 0
        self.dy = 0
        self.wid = 35
        self.hei = 56
        self.turretLen = 40
        self.prevTankBox = None
        self.halfDiagonal = distance(0,0,self.wid/2,self.hei/2)
        self.collisionTolerance = self.halfDiagonal - 10
        self.weaponType = 'cannon'
        self.rotateX = math.sin(math.radians(self.heading))
        self.rotateY = math.cos(math.radians(self.heading))
        self.isAlive = True
        self.hasLaser = False
        
    
    def addTankHeading(self,degree):
        self.heading = self.heading + degree
    
    def addTankX(self,num):
        if ((num>0 and self.x+num<=app.width-25)
            or (num<0 and self.x+num>=20)):
            self.x += num
    
    def addTankY(self,n):
        if ((n>0 and self.y+n<=app.height-25)
            or (n<0 and self.y+n>=20)):
            self.y += n

    def driveTank(self,app,key): #wasd for tank0 and ijkl for tank1
        if self.isAlive:
            self.width = app.width
            self.height = app.height
            #the values that are stored in tankBox should be the coordinates of:
            #the x,y coordinates of each corner of the box, and the center of the tankBox, for the purpose of reset
            tempTankBox = self.getTankBox(app)
            if not self.isColliding(app,tempTankBox):
                self.prevTankBox = tempTankBox
            turnedDegree = 0
            if self.index == 0:
                if 'w' in key and self.y>15 and self.x>15 : #appwidth is 800
                    self.addTankY(self.speed*self.rotateY)
                    self.addTankX(-self.speed*self.rotateX)
                if 'a' in key:
                    self.addTankHeading(-self.turnSpeed)
                    turnedDegree += -self.speed
                if 's' in key and self.y>15 and self.x>15 :
                    self.addTankY(-self.speed*self.rotateY)
                    self.addTankX(self.speed*self.rotateX)
                if 'd' in key:
                    self.addTankHeading(self.turnSpeed)
                    turnedDegree+= self.turnSpeed
            else:
                if 'y' in key and self.y>15 and self.x>15 : #appwidth is 800
                    self.addTankY(self.speed*self.rotateY)
                    self.addTankX(-self.speed*self.rotateX)
                if 'g' in key:
                    self.addTankHeading(-self.turnSpeed)
                    turnedDegree += -self.speed
                if 'h' in key and self.y>15 and self.x>15 :
                    self.addTankY(-self.speed*self.rotateY)
                    self.addTankX(self.speed*self.rotateX)
                if 'j' in key:
                    self.addTankHeading(self.turnSpeed)
                    turnedDegree+= self.turnSpeed
            if self.heading%360 == 0 and self.heading != 0:
                self.heading = 0
            currTankBox = self.getTankBox(app)
            if self.isColliding(app,currTankBox):
                self.x = self.prevTankBox[4][0]
                self.y = self.prevTankBox[4][1]
            self.rotateX = math.sin(math.radians(self.heading))
            self.rotateY = math.cos(math.radians(self.heading))
    
    def getTankBox(self,app):
        corner = [(self.wid/2,self.hei/2),
                  (self.wid/2,-self.hei/2),
                  (-self.wid/2,self.hei/2),
                  (-self.wid/2,-self.hei/2)]
        corners = []
        for i in range(len(corner)):
            x = self.x + (corner[i][0]*self.rotateY-corner[i][1]*self.rotateX)
            y = self.y + (corner[i][0]*self.rotateX+corner[i][1]*self.rotateY)
            corners.append((x,y))
        corners.append((self.x,self.y))
        corners.append(self.heading)
        # (x1,y1),(x2,y2),(x3,y3),(x4,y4) = corners
        # centerX, centerY = (x1+x2+x3+x4)/4,(y1+y2+y3+y4)/4
        # corners.append((centerX,centerY))
        return corners
    

    def isColliding(self,app,tankBox):
        (tankX1,tankY1),(tankX2,tankY2),(tankX3,tankY3),(tankX4,tankY4) = tankBox[0],tankBox[1],tankBox[2],tankBox[3]
        for line1,line2 in app.collisionList:
            line1X = min(line1[0],line1[1])
            line2X = max(line1[0],line1[1])
            line1Y = min(line2[0],line2[1])
            line2Y = max(line2[0],line2[1])
            if line1X == line2X and line1Y<=self.y<=line2Y and abs(self.x-line1X)<=self.collisionTolerance:
                return True
            elif line1Y == line2Y and line1X<=self.x<=line2X and abs(self.y-line1Y)<=self.collisionTolerance:
                return True
        return False



    def hasIntersection(self,tank1,tank2,wall1,wall2):
        A,B,C,D = tank1,tank2,wall1,wall2
        ACD = self.isCounterClockWise(A,C,D)
        BCD = self.isCounterClockWise(B,C,D)
        ABC = self.isCounterClockWise(A,B,C)
        ABD = self.isCounterClockWise(A,B,D)
        return ACD != BCD and ABC != ABD  #if all of these are satisfied, there is an intersection between the two line segments
    
    def isCounterClockWise(self,A,B,C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0]) #check if the points are counter-clockwise

    def getTurretPosition(self,x,y):
        #y = mx+b
        xDiff = x-self.x
        yDiff = y-self.y
        self.turretHeading = math.atan2(yDiff, xDiff)
        x1,y1 = self.x+self.turretLen*math.cos(self.turretHeading),self.y+self.turretLen*math.sin(self.turretHeading)
        return x1,y1

    def startTank(self):
        pass
    
    def __repr__(self):
        return f'Tank, position({self.x},{self.y}),heading angle ({self.heading})'

def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5