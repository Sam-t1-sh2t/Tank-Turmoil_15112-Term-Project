from cmu_graphics import *
from tank import Tank
from cannon import Cannon
from laser import Laser
from mazeGen import Cell
from clusterCannon import clusterCannon
import os, pathlib
import math
import copy
import random
def onAppStart(app):
    resetAll(app)
    print(app.collisionList)

def resetAll(app):
    app.tanks = []
    app.mapRows = 6
    app.mapCols = 6
    app.cannonVelocity = 7 #default velocity
    app.tankSpeed = 4
    app.mapLeft = 10
    app.mapTop = 10
    app.cellWidth = 120
    app.cellHeight = 120
    app.width, app.height = app.cellWidth*app.mapCols+20, app.cellHeight* app.mapRows+20
    app.stepsPerSecond = 60
    app.tankTurnSpeed = 5
    app.mapPowerUp = 0
    app.steps = 0
    app.powerUpSteps = 0
    app.spreadNum = 8
    app.gameMode = 'multi'
    setupTank(app)
    app.optionButton = [((app.width/2)-100,(app.height/2)-60),
                        ((app.width/2)+100,(app.height/2)-60),
                        ((app.width/2)-100,(app.height/2)+60),
                        ((app.width/2)+100,(app.height/2)+60)]
    reset(app)
    for row in range(len(app.map)):
        for col in range(len(app.map[0])):
            cell = app.map[row][col]
            print(row,col,cell.top,cell.left,cell.right,cell.bottom)

def reset(app):
    app.paused = False
    app.gameOver = False
    app.stepsLeft = app.stepsPerSecond*3
    app.map = []
    setUpMap(app)
    app.wallLocation = []
    setUpAim(app)
    app.collisionList = []
    setupCollision(app)
    app.existingWeapons = []
    app.gameSettlement = False
    app.mapPowerUp = 0
    app.steps = 0
    app.powerUpSteps = 0
    for i in range(len(app.tanks)):
        app.tanks[i].tankReset(app,i)


def setupTank(app):
    if app.gameMode == 'multi':
        for i in range(2):
            app.tanks.append(Tank(app,i,app.tankSpeed,app.tankTurnSpeed))


def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

def setupCollision(app):
    for row in app.map:
        for cell in row:
            if cell.top:
                app.collisionList.append(((cell.x,cell.x+app.cellWidth),(cell.y,cell.y))) 
            if cell.left:
                app.collisionList.append(((cell.x,cell.x),(cell.y,cell.y+app.cellHeight)))
            if cell.right:
                app.collisionList.append(((cell.x+app.cellWidth,cell.x+app.cellWidth),(cell.y,cell.y+app.cellHeight)))
            if cell.bottom:
                app.collisionList.append(((cell.x,cell.x+app.cellWidth),(cell.y+app.cellHeight,cell.y+app.cellHeight)))
            

    
    

def setUpAim(app): #set up the aiming system for solo mode. the variables have to be instantiated for both modes anyways
    app.cursorX = 50
    app.cursorY = 50
    app.lineX,app.lineY = app.tanks[0].getTurretPosition(app.cursorX,app.cursorY)


def setUpMap(app):  #get the idea of the algoritm from this video: https://www.youtube.com/watch?v=Ez7U6jU0q5k maze generator using Depth-first search
                    #the code I wrote is totally original. The video used pygame instead
    app.map = []
    for row in range(app.mapRows):
        rowList = []
        for col in range(app.mapCols):
            rowList.append(Cell(app.cellWidth*col+app.mapLeft,app.cellHeight*row+app.mapTop,app.cellHeight))
        app.map.append(rowList)
    setUpMaze(app)

def setUpMaze(app):
    checkList = []
    for row in range(len(app.map)):
        rowList = []
        for col in range(len(app.map[0])):
            rowList.append(False)
        checkList.append(rowList)
    setupHelper(app.map,checkList,0,0)


def setupHelper(map,checkList,currRow,currCol):
    if not any(False in row for row in checkList):
        return map
    else:
        direction = [(-1,0),(1,0),(0,-1),(0,1)]
        if not map[currRow][currCol].visited:
            map[currRow][currCol].visited = True
            checkList[currRow][currCol] = True
        moveable = remainingNeighbors(map,currRow,currCol,direction)
        for dRow,dCol in moveable:
            nextRow, nextCol = currRow + dRow, currCol + dCol
            if not map[nextRow][nextCol].visited:
                cancelWall(map,currRow,currCol,dCol,dRow)
                setupHelper(map,checkList,currRow+dRow,currCol+dCol)


def remainingNeighbors(map,row,col,direction):
    newList = []
    for dRow,dCol in direction:
        if 0<=row+dRow<len(map) and 0<=col+dCol<len(map[0]) and not map[row+dRow][col+dCol].visited:
            newList.append((dRow,dCol))
    random.shuffle(newList)
    return newList


def cancelWall(map,row,col,dCol,dRow):
    if dCol == -1:
        map[row][col].left = False
        map[row][col-1].right = False
    elif dCol == 1:
        map[row][col].right = False
        map[row][col+1].left = False
    elif dRow == -1:
        map[row][col].top = False
        map[row-1][col].bottom = False
    elif dRow == 1:
        map[row][col].bottom = False
        map[row+1][col].top = False

############################################################
# Start Screen
############################################################
def start_redrawAll(app):
    TL,TR,BL,BR = app.optionButton
    drawLabel('Welcome to Tank Turmoil!',app.width/2,150,size = 30,bold = True)
    drawLabel('Press any key to start!',app.width/2,250,size = 20)
    drawLabel('Left click on the options to adjust them',app.width/2,app.height/2+app.cellHeight*1.5,size = 20)
    drawPolygon(TL[0],TL[1],TR[0],TR[1],BR[0],BR[1],BL[0],BL[1],fill = None,border = 'black',borderWidth=2)
    drawLabel('Options',app.width/2,app.height/2,size = 16)


def start_onKeyPress(app,key):
    setActiveScreen('instructions')

def start_onMousePress(app,mouseX,mouseY):
    if not selectsOptions(app,mouseX,mouseY):
        setActiveScreen('instructions')
    else:
        setActiveScreen('options')

def selectsOptions(app,x,y):
    TL,TR,BL,BR = app.optionButton
    if TL[0]<=x<=BR[0] and TL[1]<=y<=BR[1]:
        return True
    return False

############################################################
# Instructions Screen
############################################################
def instructions_redrawAll(app):
    drawLabel("Player 1: use 'w' 's' to move forward/backward, ",app.width/2,app.height/9,size = 18)
    drawLabel("use 'a', 'd' to turn left/right (clockwise/counterclockwise)",app.width/2,app.height/9*2,size = 18)
    drawLabel("Left click to fire, press 'q' to make the cluster cannons 'explode'  you'll see hehehe :)",app.width/2,app.height/9*3,size = 18)
    drawLabel("Player 2: use 'y' 'h' to move forward/backward, use 'g', 'j' to turn left/right",app.width/2,app.height/9*4,size = 18)
    drawLabel("Press 'space' to fire, press 'l' (L) to make the cluster explode",app.width/2,app.height/9*5,size = 18)
    drawLabel('Press any key to continue',app.width/2,app.height/9*6,size = 18)
    drawLabel("Press 'b' to go back",app.width/2,app.height/9*7,size = 18)
    drawLabel("Have Fun!!!!!!",app.width/2,app.height/9*8,size = 30)


def instructions_onKeyPress(app,key):
    if key!='b':
        setActiveScreen('game')
    else:
        setActiveScreen('start')




############################################################
# Options Screen
############################################################
def options_onScreenActivate(app):
    app.optionsBoard = []
    app.optionsText = [['Cannon Velocity','Refresh Rate','Tank Velocity','Turn Degrees','Rate this game:'],
                       ['++','++','++','++','++'],
                       [],
                       ['--','--','--','--','--']]
    app.appRate = 0
    app.boardLeft = 100
    app.boardTop = 100
    app.boardRows = 4
    app.boardCols = 5
    app.boardWid = app.width-app.boardLeft*2
    app.boardHei = app.height-app.boardTop*2
    app.optionsCellWid = app.boardWid/app.boardCols
    app.optionsCellHei = app.boardHei/app.boardRows
    app.count = 0
    instantiateBoard(app)

def instantiateBoard(app):
    color = ['red','yellow','green','cyan','blue','purple','orange']
    for row in range(app.boardRows):
        rowList = []
        for col in range(app.boardCols):
            if row == 0:
                selectedColor = random.choice(color)
                rowList.append(selectedColor)
                color.remove(selectedColor)
            else:
                rowList.append(None)
        app.optionsBoard.append(rowList)


# def options_onMouseDrag(app,mouseX,mouseY):
#     print(app.count)
#     row,col = getRowCol(app,mouseX,mouseY)
#     if (row,col)!= (None,None):
#         app.count+=1
#         if app.count>=60:
#             if row == 1:
#                 if col == 0:
#                     if app.cannonVelocity<15-10:
#                         app.cannonVelocity+=10
#                     else:app.cannonVelocity = 15
#                 elif col == 1:
#                     if app.stepsPerSecond<70-10:
#                         app.stepsPerSecond+=10
#                     else: app.stepsPerSecond = 70
#                 elif col == 2:
#                     if app.tankSpeed<10:
#                         app.tankSpeed=10
#                 elif col == 3:
#                     if app.appRate == 'TAT':
#                         app.appRate = -100
#                     elif app.appRate<300-10:
#                         app.appRate += 10
#                     else:
#                         app.appRate = 'Infinite!!!'
#             elif row == 3:
#                 if col == 0:
#                     if app.cannonVelocity>1+10:
#                         app.cannonVelocity-=10
#                     else: app.cannonVelocity = 1
#                 elif col == 1:
#                     if app.stepsPerSecond>20+10:
#                         app.stepsPerSecond-=10
#                     else:app.stepsPerSecond = 20
#                 elif col == 2:
#                     if app.tankSpeed>1+10:
#                         app.tankSpeed-=10
#                     else: app.tankSpeed = 1
#                 elif col == 3:
#                     if app.appRate == 'Infinite!!!':
#                         app.appRate = 300
#                     elif app.appRate>-100+10:
#                         app.appRate -= 10
#                     else:
#                         app.appRate = 'TAT'
#             app.count = 0
            
# def options_onMouseRelease(app,mouseX,mouseY):
#     app.count = 0

def options_onMousePress(app,mouseX,mouseY):
    #switchCells(app,mouseX,mouseY)
    row,col = getRowCol(app,mouseX,mouseY)
    if (row,col)!= (None,None):
        if row == 1:
            if col == 0:
                if app.cannonVelocity<15:
                    app.cannonVelocity+=1
            elif col == 1:
                if app.stepsPerSecond<70:
                    app.stepsPerSecond+=1
            elif col == 2:
                if app.tankSpeed<10:
                    app.tankSpeed+=1
            elif col == 3:
                if app.tankTurnSpeed<20:
                    app.tankTurnSpeed+=1
            elif col == 4:
                if app.appRate == 'TAT':
                    app.appRate = -100
                elif app.appRate<300:
                    app.appRate += 1
                else:
                    app.appRate = 'Infinite!!!'
                
        elif row == 3:
            if col == 0:
                if app.cannonVelocity>1:
                    app.cannonVelocity-=1
            elif col == 1:
                if app.stepsPerSecond>20:
                    app.stepsPerSecond-=1
            elif col == 2:
                if app.tankSpeed>1:
                    app.tankSpeed-=1
            elif col == 3:
                if app.tankTurnSpeed>1:
                    app.tankTurnSpeed-=1
            elif col == 4:
                if app.appRate == 'Infinite!!!':
                    app.appRate = 300
                elif app.appRate>-100:
                    app.appRate -= 1
                else:
                    app.appRate = 'TAT'

def getRowCol(app,x,y):
    for col in range(len(app.optionsBoard[0])):
        for row in range(len(app.optionsBoard)):
            if (app.boardLeft+app.optionsCellWid*col<=x<=app.boardLeft+app.optionsCellWid*(col+1) and
                app.boardTop+app.optionsCellHei*row<=y<=app.boardTop+app.optionsCellHei*(row+1)):
                return row,col
    return None,None

def switchCells(app,x,y):
    for row in range(app.boardRows):
        for col in range(app.boardCols):
            x0 = app.boardLeft+app.optionsCellWid*col
            x1 = app.boardLeft+app.optionsCellWid*(col+1)
            y0 = app.boardTop+app.optionsCellHei*row
            y1 = app.boardTop+app.optionsCellHei*(row+1)
            if x0<=x<=x1 and y0<=y<=y1 and app.optionsBoard[row][col] == None:
                color = None
                for i in range(app.boardRows):
                    if app.optionsBoard[i][col]!=None:
                        color = app.optionsBoard[i][col]
                    app.optionsBoard[i][col] = None
                # setGameSetting(app,row,col)
                app.optionsBoard[row][col] = color

 
### gamemode(solo or multi);mapsize(row);mapsize(col);game AI difficulty

# game mode,weapons, game AI difficulty
#add app to init function to control the features of tank and weapons

def options_redrawAll(app):
    drawLabel("press 'b' to go back to start page",app.width/2,30,size = 14,bold = True)
    drawLabel("press 'r' to get default settings",app.width/2,55,size = 14,bold = True)
    drawBoard(app)

def drawBoard(app):
    for row in (range(app.boardRows)):
        for col in range(app.boardCols):
            drawRect(app.boardLeft+app.optionsCellWid*col,app.boardTop+app.optionsCellHei*row,app.optionsCellWid,app.optionsCellHei,fill = app.optionsBoard[row][col],border = 'black')
            if row!=2:
                drawLabel(app.optionsText[row][col],app.boardLeft+app.optionsCellWid*(col+0.5),app.boardTop+app.optionsCellHei*(row+0.5),size = 14,bold = True)
            else:
                if col == 0:
                    drawLabel(app.cannonVelocity,app.boardLeft+app.optionsCellWid*(col+0.5),app.boardTop+app.optionsCellHei*(row+0.5),size = 25,bold = True)
                elif col == 1:
                    drawLabel(app.stepsPerSecond,app.boardLeft+app.optionsCellWid*(col+0.5),app.boardTop+app.optionsCellHei*(row+0.5),size = 25,bold = True)
                elif col == 2:    
                    drawLabel(app.tankSpeed,app.boardLeft+app.optionsCellWid*(col+0.5),app.boardTop+app.optionsCellHei*(row+0.5),size = 25,bold = True)
                elif col == 3:
                    drawLabel(app.tankTurnSpeed,app.boardLeft+app.optionsCellWid*(col+0.5),app.boardTop+app.optionsCellHei*(row+0.5),size = 25,bold = True)
                elif col == 4:
                    drawLabel(app.appRate,app.boardLeft+app.optionsCellWid*(col+0.5),app.boardTop+app.optionsCellHei*(row+0.5),size = 25,bold = True)
                


def options_onKeyPress(app,key):
    if key == 'b':
        for tank in app.tanks:
            tank.speed = app.tankSpeed
        setActiveScreen('start')
    if key == 'r':
        resetAll(app)


############################################################
# Game Screen
############################################################

def game_redrawAll(app):
    drawMap(app)
    drawTank(app)
    drawWeapon(app)
    drawSettlement(app)

def drawSettlement(app):
    if app.gameSettlement:
        drawRect(app.mapLeft+app.cellWidth,app.mapTop+app.cellHeight,
                 app.cellWidth*(app.mapCols-2),app.cellHeight*(app.mapRows-2),
                 fill = 'lightGreen',border = 'white',borderWidth = 5)
        drawLabel('Game Over!',app.width/2,app.height/2-app.cellHeight,size = 40, bold = True)
        drawLabel(f'Player one: {app.tanks[0].scores}',app.width/2-app.cellWidth,app.height/2,size = 30,bold = True)
        drawLabel(f'Player two: {app.tanks[1].scores}',app.width/2+app.cellWidth,app.height/2,size = 30,bold = True)
        drawLabel('Press r to play another round',app.width/2,app.height/2+app.cellHeight,size=30,bold = True)
        drawLabel('Press b to go back to starting page (resets everything)',app.width/2,app.height/2+app.cellHeight*1.5,size = 20,bold = True)


def drawWeapon(app):
    if app.existingWeapons!=[]:
        for weapon in app.existingWeapons:
            if isinstance(weapon,Cannon):
                if weapon.draw:
                    drawCannon(weapon)
            elif isinstance(weapon,Laser):
                if weapon.draw:
                    drawLaser(weapon)
            elif isinstance(weapon,clusterCannon):
                if weapon.draw:
                    drawBigCannon(weapon)
                    

def drawBigCannon(weapon):
    drawCircle(weapon.x,weapon.y,weapon.size,fill = 'black')

def drawLaser(weapon):
    for segment in weapon.segments:
        point1, point2 = segment[0],segment[1]
        x0,y0 = point1[0],point1[1]
        x1,y1 = point2[0],point2[1]
        drawLine(x0,y0,x1,y1,lineWidth = weapon.laserWidth,fill = weapon.color)


def drawCannon(cannon):
    drawCircle(cannon.x,cannon.y,cannon.size,fill = 'black')


def drawAim(app):
    drawCircle(app.cursorX,app.cursorY,15,fill = None, border = 'black')
    drawLine(app.cursorX-20,app.cursorY,app.cursorX+20,app.cursorY,dashes=(10, 20))
    drawLine(app.cursorX,app.cursorY-20,app.cursorX,app.cursorY+20,dashes=(10, 20))


def drawTank(app):
    if app.gameMode == 'multi':
        for tank in app.tanks:
            if tank.isAlive:
                drawRect(tank.x,tank.y,tank.wid,tank.hei,fill = tank.color,align = 'center',rotateAngle = tank.heading)
                drawRect(tank.x-25*tank.rotateX,tank.y+25*tank.rotateY,tank.wid,tank.hei-50,fill = 'green',align = 'center',rotateAngle = tank.heading)
                drawCircle(tank.x,tank.y,10,fill = 'black')
                drawLine(tank.x,tank.y,tank.x-tank.turretLen*tank.rotateX,tank.y+tank.turretLen*tank.rotateY,lineWidth=5)
            else:
                drawLabel('BOOM!',tank.x,tank.y,size = 16)
    elif app.gameMode == 'solo':
        for tank in app.tanks:
            if tank.isAlive:
                drawRect(tank.x,tank.y,tank.wid,tank.hei,fill = tank.color,align = 'center',rotateAngle = tank.heading)
                drawRect(tank.x-25*tank.rotateX,tank.y+25*tank.rotateY,tank.wid,tank.hei-50,fill = 'green',align = 'center',rotateAngle = tank.heading)
                drawCircle(tank.x,tank.y,10,fill = 'black')        
                drawLine(tank.x,tank.y,app.lineX,app.lineY,lineWidth = 5) #this is the tank's turret
            else: 
                drawLabel('BOOM!',tank.x,tank.y,size = 16)
            if tank.index == 0:
                drawLine(tank.x,tank.y,app.cursorX,app.cursorY,dashes=(10, 6)) #this is the 辅助线 for aiming
                drawAim(app)

def drawMap(app):
    for row in app.map:
        for cell in row:
            if cell.top:
                drawLine(cell.x,cell.y,cell.x+app.cellWidth,cell.y,lineWidth = 20)
            if cell.left:
                drawLine(cell.x,cell.y,cell.x,cell.y+app.cellHeight,lineWidth = 20)
            if cell.right:
                drawLine(cell.x+app.cellWidth,cell.y,cell.x+app.cellWidth,cell.y+app.cellHeight,lineWidth = 20)
            if cell.bottom:
                drawLine(cell.x,cell.y+app.cellHeight,cell.x+app.cellWidth,cell.y+app.cellHeight,lineWidth = 20)
            if cell.visited:
                drawRect(cell.x,cell.y,app.cellWidth,app.cellHeight,fill = 'cyan')
            if cell.specialWeapon != None:
                drawRect(cell.x+app.cellWidth/4,cell.y+app.cellWidth/4,app.cellWidth/2,app.cellHeight/2,fill = 'pink',rotateAngle = 45)
                drawLabel(f'{cell.specialWeapon}!',cell.x+app.cellWidth/2,cell.y+app.cellHeight/2,size = 14)

def game_onMouseMove(app,mouseX,mouseY):
    app.cursorX,app.cursorY = mouseX,mouseY

def game_onKeyPress(app,key):
    if 'p' == key:
        app.paused = not app.paused
    if 'r' == key and (app.gameSettlement or app.paused):
        reset(app)
    if 'b' == key:
        setActiveScreen('start')
        resetAll(app)
    if 'space' == key:
        addWeapon(app,1)
    if 'q' == key:
        clusterExplodes(app,0)
    if 'l' == key:
        clusterExplodes(app,1)

def clusterExplodes(app,tankIndex):
    for weapon in app.existingWeapons:
        if isinstance(weapon,clusterCannon) and weapon.draw == True and weapon.owner == tankIndex:
            weapon.clusterExplode(app)


def game_onMousePress(app,mouseX,mouseY):
    addWeapon(app,0)

def addWeapon(app,tankIndex):
    tank = app.tanks[tankIndex]
    if not app.paused and not app.gameSettlement and tank.isAlive:
        if app.gameMode == 'multi':
            if tank.weaponType == 'cannon':
                weapon = Cannon(app,tank.x-(tank.turretLen+3)*tank.rotateX,tank.y+(tank.turretLen+3)*tank.rotateY,tank.heading,app.cannonVelocity)
            elif tank.weaponType == 'laser':
                weapon = Laser(app,tank.x-(tank.turretLen+3)*tank.rotateX,tank.y+(tank.turretLen+3)*tank.rotateY,tank.heading)
                tank.weaponType = 'cannon'
            elif tank.weaponType == 'clusterCannon':
                weapon = clusterCannon(app,tank.x-(tank.turretLen+3)*tank.rotateX,tank.y+(tank.turretLen+3)*tank.rotateY,tank.heading,app.cannonVelocity,tankIndex)
                tank.weaponType = 'cannon'
        app.existingWeapons.append(weapon)

def game_onKeyHold(app,key):
    if not app.paused and not app.gameSettlement:
        for tank in app.tanks: #if this doesn't work, switch to hardcode. call the methods for the tanks one by one
            tank.driveTank(app,key)
            # print(tank.x,tank.y)

def game_onStep(app):
    if not app.paused:
        if not app.gameOver:
            takeStep(app)
        else: 
            app.stepsLeft -= 1
            takeStep(app)
            if app.stepsLeft == 0:
                app.gameSettlement = True
                for tank in app.tanks:
                    if tank.isAlive:
                        tank.scores+=1

def takeStep(app):
    app.steps += 1
    app.powerUpSteps+=1
    if app.powerUpSteps%app.stepsPerSecond*10 == 0 and app.powerUpSteps!=0 and app.mapPowerUp<1:
        randX = random.randint(0,len(app.map[0])-1)
        randY = random.randint(0,len(app.map)-1)
        app.map[randX][randY].powerUp()
        app.mapPowerUp += 1
    app.lineX, app.lineY = app.tanks[0].getTurretPosition(app.cursorX,app.cursorY)
    if app.existingWeapons != []:
        for i in range(len(app.existingWeapons)):
            weapon = app.existingWeapons[i]
            if isinstance(weapon,Cannon) and weapon.draw:
                weapon.moveCannon(app)
                # if hit(app,weapon):
                #     weapon.draw = False
                if weapon.steps>5*app.stepsPerSecond:
                    weapon.draw = False
                    weapon.dx = 0
                    weapon.dy = 0
            if isinstance(weapon,Laser) and weapon.draw:
                if app.steps%10 == 0 and app.steps != 0:
                    weapon.draw = False
            if isinstance(weapon,clusterCannon) and weapon.draw:
                weapon.moveCluster(app)
                if weapon.steps>5*app.stepsPerSecond and weapon.draw:
                    weapon.draw = False
                    weapon.dx = 0
                    weapon.dy = 0
                    weapon.clusterExplode(app)

            targetHit(app,weapon)
    count = 0
    for tank in app.tanks:
        if tank.isAlive:
            count += 1
            checkPowerUpCell(tank,app)

    if count<=1:
        app.gameOver = True
        
def checkPowerUpCell(tank,app):
    row,col = getMapRowCol(app,tank.x,tank.y)
    cell = app.map[row][col]
    if cell.specialWeapon != None:
        tank.weaponType = cell.specialWeapon
        cell.specialWeapon = None
        app.mapPowerUp -= 1

def getMapRowCol(app,x,y):
    for col in range(len(app.map[0])):
        for row in range(len(app.map)):
            if (app.mapLeft+app.cellWidth*col<=x<=app.mapLeft+app.cellWidth*(col+1) and
                app.mapTop+app.cellHeight*row<=y<=app.mapTop+app.cellHeight*(row+1)):
                return row,col
    return None,None

def targetHit(app,weapon):   #get mathematical support from gpt. the code is written by myself
    if weapon.draw:
        for tank in app.tanks:
            if tank.isAlive:
                tankBox = tank.getTankBox(app)
                vertex1,vertex2,vertex3,vertex4 = tankBox[1],tankBox[0],tankBox[2],tankBox[3]
                if isinstance(weapon,Cannon) or isinstance(weapon,clusterCannon):
                    crossProductList = []
                    crossProductList.append(crossProduct(vertex1,vertex2,weapon.x,weapon.y))
                    crossProductList.append(crossProduct(vertex2,vertex3,weapon.x,weapon.y))
                    crossProductList.append(crossProduct(vertex3,vertex4,weapon.x,weapon.y))
                    crossProductList.append(crossProduct(vertex4,vertex1,weapon.x,weapon.y))
                    if not (max(crossProductList)>0 and min(crossProductList)<0):
                        tank.isAlive = False
                elif isinstance(weapon,Laser):
                    result = []
                    for x,y in weapon.pointCollisionL:
                        crossProductList = []
                        crossProductList.append(crossProduct(vertex1,vertex2,x,y))
                        crossProductList.append(crossProduct(vertex2,vertex3,x,y))
                        crossProductList.append(crossProduct(vertex3,vertex4,x,y))
                        crossProductList.append(crossProduct(vertex4,vertex1,x,y))
                        if not (max(crossProductList)>0 and min(crossProductList)<0):
                            result.append(False)
                        else: result.append(True)
                    if any(bol == False for bol in result):
                        tank.isAlive = False


            
def crossProduct(p1,p2,px,py):
    vectp2p1 = (p2[0]-p1[0],p2[1]-p1[1])
    vectp1p = (px-p1[0],py-p1[1])
    return vectp2p1[0]*vectp1p[1]-vectp2p1[1]*vectp1p[0]  

def main():
    runAppWithScreens(initialScreen = 'start')
main()
