import math, random
import matplotlib as plt
import numpy as np


class Ball:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, xmove, ymove):
        self.x = self.x + xmove
        self.y = self.y + ymove

    def display(self):
        print(f"({self.x},{self.y})")



    
xcoord = 0
ycoord = 0

ball1 = Ball(xcoord,ycoord)
ball1.display()


ball1.move(10,20)

ball1.display()