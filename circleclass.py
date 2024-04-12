import p5
from p5 import setup, draw, colorMode, strokeWeight, size, background, background, Vector, stroke, circle, run
import numpy as np

class circleObject():

    #Circles need a location and curvature/radius
    def __init__(self, x, y, k, generation):
        self.x = x
        self.y = y
        self.k = k
        self.r =np.abs(1 / self.k)
        self.generation = generation

    #Show the circle on the display
    def display(self):
        colorMode('HSB')
        stroke(150 + self.generation * 10, 200, 200)
        strokeWeight(3)
        p5.no_fill()
        p5.circle(self.x, self.y, np.abs(1 / self.k)*2)

class imNumber():

    #Custom imaginary number class just for doing simple arithmetic
    def __init__(self, re, im):
        self.re = re
        self.im = im

    def imAdd(self, other):
        return imNumber(self.re + other.re, self.im + other.im)
    
    def imSub(self, other):
        return imNumber(self.re - other.re, self.im - other.im)
    
    def imScale(self, value):
        return imNumber(self.re * value, self.im * value)
    
    def imMult(self, other):
        return imNumber(self.re*other.re - self.im*other.im, self.re*other.im + other.re*self.im)
    
    def imRoot(self):
        mag = np.sqrt(self.re**2 + self.im**2)
        angle = np.arctan2(self.im, self.re)

        mag = np.sqrt(mag)
        angle = angle / 2
        return(imNumber(mag * np.cos(angle), mag * np.sin(angle)))
    
