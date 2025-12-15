from cmu_graphics import *
import math
class Segment:
    def __init__(self,x0,y0,x1,y1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.slope = (self.y1-self.y0)/(self.x1-self/x0)
        self.len = distance(x0,y0,x1,y1)
    
    