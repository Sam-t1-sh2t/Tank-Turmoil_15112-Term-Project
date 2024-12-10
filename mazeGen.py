from cmu_graphics import *
import random
import math
class Cell:
    def __init__(self,x,y,sideLen):
        self.top = True
        self.left = True
        self.right = True
        self.bottom = True
        self.x = x
        self.y = y
        self.sideLen = sideLen
        self.visited = False
        self.specialWeapon = None
        self.powerUpList = ['laser','clusterCannon']
    
    def powerUp(self):
        self.specialWeapon = random.choice(self.powerUpList)
        print(self.specialWeapon)

    def __repr__(self):
        return f'Cell at position ({self.x},{self.y})'
    
    def getCellX(self):
        return self.x
    
    def getCellY(self):
        return self.y
    
        