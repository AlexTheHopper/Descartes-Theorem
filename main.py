import p5
from p5 import setup, draw, size, background, background, Vector, stroke, circle, run
from circleclass import circleObject, imNumber
import numpy as np
import time
import math
import random

#Descartes' Theorem#
#Alexander Hopper#
#Created: 12/4/24
#Last Updates: 12/4/24

#This .py begins with three circles and over iterations, finds extra mutually tangential circles to each triplet of already existing circles.
#This makes use of Descartes' Theorem: https://en.wikipedia.org/wiki/Descartes%27_theorem
#Knowing the three curvatures, one can find the curvature of the fourth.
#Then knowing the four curvatures and the locations of the three circles on a complex plane, one can find locations of potential fourth circles.


#Size of the display, pixels
width = 1000
height = 1000
#Size of the larger circle, pixels
mainSize = 500

#Standard == True starts with set symmetrical triplet
#Standard == False starts with semi-random triplet
standard = False

#Finds the curvature of the fourth circle (k4), given three other tangential circles
def getFourthK(c1, c2, c3):
    sum = c1.k + c2.k + c3.k
    root = 2 * np.sqrt(np.abs(c1.k*c2.k + c2.k*c3.k + c1.k*c3.k))
    return [sum + root, sum - root]

#Finds the location of a fourth circle tangential to 3 other tangential circles from complex coordinates
#Takes in 3 circles and one [k1, k2] curvatures
#Returns four circle objects that *should be* tangential to the three input circles with curvature of k4
def getFourthCircles(c1, c2, c3, k4, g):
    comp1 = imNumber(c1.x,c1.y)
    c1k = comp1.imScale(c1.k)
    comp2 = imNumber(c2.x,c2.y)
    c2k = comp2.imScale(c2.k)
    comp3 = imNumber(c3.x,c3.y)
    c3k = comp3.imScale(c3.k)

    #Add c1k1, c2k2 and c3k3
    sum = c1k.imAdd(c2k.imAdd(c3k))

    #Add pairs of cnkn*cmkm
    underRoot = c1k.imMult(c2k).imAdd(c2k.imMult(c3k)).imAdd(c1k.imMult(c3k))
    root = underRoot.imRoot().imScale(2)

    resultPlus = (sum.imAdd(root))
    resultMinus = (sum.imSub(root))
    #Return the four potential circle objects to be added
   
    return ([
        circleObject(resultPlus.imScale(1/k4[0]).re,resultPlus.imScale(1/k4[0]).im,k4[0], g),
        circleObject(resultMinus.imScale(1/k4[0]).re,resultMinus.imScale(1/k4[0]).im,k4[0], g),
        circleObject(resultPlus.imScale(1/k4[1]).re,resultPlus.imScale(1/k4[1]).im,k4[1], g),
        circleObject(resultMinus.imScale(1/k4[1]).re,resultMinus.imScale(1/k4[1]).im,k4[1], g)
    ])

#Ensures any new circle is valid:
def checkCircle(new, allCircles, newTriplet):
    e = 1
    minD = 2
    #If circles are getting too small, dont add:
    if new.r < e:
        return False
    
    #Check to see if the circle is in the same spot as another:
    for c in allCircles:
        if math.dist([new.x,new.y],[c.x,c.y]) < minD:
            return False
        
    #Ensure it is actually tangential to all three
    for c in newTriplet:
        dist = math.dist([new.x,new.y],[c.x,c.y])
        rNew = new.r
        rOld = c.r

        #If both distances dont match(i.e. not tangential to one of the triplet circles), return false and dont add the circle.
        case1 = np.abs(dist - (rNew + rOld)) < e
        case2 = dist - np.abs(rNew - rOld) < e
        if not case1 and not case2:
            return False

    #If it passes the tests, add the circle.
    return True

#Just for aligning initial circles in random mode
def rotate2DVector(V,angle):
    return([V[0]*np.cos(angle) - V[1]*np.sin(angle),V[0]*np.sin(angle) + V[1]*np.cos(angle)])

#Prepares the canvas and adds the initial triplet of circles
def setup():
    global allCircles, queue, width, height, mainSize
    size(width, height)
    if standard:
        start1 = circleObject(width/2, height/2, -1/mainSize, 0)
        start2 = circleObject(width/2 + mainSize/2, height/2, 1/(mainSize/2), 0)
        start3 = circleObject(width/2 - mainSize/2, height/2, 1/(mainSize/2), 0)
    else:
        #This is very ugly *but works* :/
        #Large circle is always the same
        start1 = circleObject(width/2, height/2, -1/mainSize, 0)

        #Second circle is put on a random side with a semirandom size using a rotated vector as its position.
        angle = random.randrange(0,50)
        r2 = random.randrange(20, round(start1.r / 2))
        vec = [0,start1.r - r2]
        vec = rotate2DVector(vec, angle)
        start2 = circleObject(500+vec[0],500+vec[1],1/r2, 0)
        
        #The third circle also uses this rotated vector
        r3 = start1.r - r2
        mag = np.sqrt(vec[0]**2+vec[1]**2)
        vec = vec / mag
        vec = vec * (r3 - start1.r)
        start3 = circleObject(500+vec[0],500+vec[1],1/r3, 0)

    allCircles = [start1,start2,start3]
    queue = [[start1,start2,start3]]

#Iterates this function to draw new circles
generation = 1
def draw():
    global allCircles, queue, generation
    background(255)
    

    #Actually display circles
    for c in allCircles:
        c.display()

    #Delay so you can actually see the progress.
    time.sleep(1)

    #Each iteration produces a new list of NEW triplets to check next iteration.
    newQueue = []
    for triplet in queue:
        #find k values, k is of form [k0,k1]
        newK = getFourthK(triplet[0], triplet[1], triplet[2])
       
        #find 4 potential circles
        newCircles = getFourthCircles(triplet[0], triplet[1], triplet[2], newK, generation)
       
        #add them to the whole list if valid
        for newCircle in newCircles:
            if checkCircle(newCircle, allCircles, triplet):
                allCircles.append(newCircle)
       
                #add new triplets to queue which all incude one new circle and two old circles.
                newQueue.append([newCircle, triplet[0], triplet[1]])
                newQueue.append([newCircle, triplet[0], triplet[2]])
                newQueue.append([newCircle, triplet[1], triplet[2]])


    queue = newQueue[:]
    generation += 1
   


run()