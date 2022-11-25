# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 14:37:15 2022

@author: Alex
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import optimize
from ballSampling import rejection_sampling
from readData import oneTrack

print('parsingSingleTrack')        
track=oneTrack()
balls=[]
samples=[]
print('StartSampling')
for i in range(len(track)):
    balls.append([track[i],1])
    samples.append(rejection_sampling(3,1,track[i],30))
#function test data starts here
#N=100000
#r1 = 1
#c1 = np.array((0,0,0))
#r2 = 1
#c2 = np.array((0,1,1))
#r3 = 1
#c3 = np.array((3,2,0))
#r4 = 1
#c4 = np.array((3,3,2))
#r5 = 1
#c5 = np.array((0,4,1))
#r6 = 1
#c6 = np.array((1,4,1))
#r7 = 1
#c7 = np.array((5,4,1))
#r8 = 1
#c8 = np.array((2,2,5))
#r9 = 1
#c9 = np.array((4,1,4))
#r10 = 1
#c10 = np.array((2,1,1))


#ballArray=[[c1,r1],[c2,r2],[c3,r3],[c4,r4],[c5,r5],[c6,r6],[c6,r6],[c7,r7],[c8,r8],[c9,r9]]
#sampleBall1 = rejection_sampling(3,r1,c1,N)
#sampleBall2 = rejection_sampling(3,r2,c2,N)
#sampleBall3 = rejection_sampling(3,r3,c3,N)
#sampleBall4 = rejection_sampling(3,r4,c4,N)
#sampleBall5 = rejection_sampling(3,r5,c5,N)
#sampleBall6 = rejection_sampling(3,r6,c6,N)
#sampleBall7 = rejection_sampling(3,r7,c7,N)
#sampleBall8 = rejection_sampling(3,r8,c8,N)
#sampleBall9 = rejection_sampling(3,r9,c9,N)

#sampleArray = [sampleBall1,sampleBall2,sampleBall3,sampleBall4,sampleBall5,sampleBall6,sampleBall7,sampleBall8,sampleBall9]
print('EndSampling')
#function test data ends here

def angle(vec1, vec2, acute=True):
    angle = np.arccos(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    if (acute == True):
        return angle
    else:
        return 2 * np.pi - angle

def f(x):#muss den max Winkel berechnen
    y = [int(xs) for xs in x]
    #curveOld = [sampleArray[0][y[0]], sampleArray[1][y[1]], sampleArray[2][y[2]],sampleArray[3][y[3]]]
    curve=[]
    vectors=[]
    tmp=[]
    for i in range(len(y)):
        curve.append(samples[i][y[i]])
    for i in range(len(y)-1):
        vectors.append(curve[i+1]-curve[i])
    for i in range(len(vectors)-1):
        tmp.append(-angle(vectors[i],vectors[i+1]))
    return min(tmp)

def computeStabber(sampleArray):
    samples = []
    for i in range(len(sampleArray)):
        samples.append(sampleArray[i])
        
    listZip = [0]*len(sampleArray)

    print('StartOptimizing')
    res = optimize.dual_annealing(f, bounds=list(zip(listZip,[len(x)-0.001 for x in samples])))

    xf = res['x']
    curveList = []
    for i in range(len(sampleArray)):
        curveList.append(sampleArray[i][int(xf[i])])
    return(np.array(curveList))

def outerTangents(r1,c1,r2,c2):
    angle1 = math.atan2(c2[1]-c1[1],c2[0]-c1[0])
    angle2 = math.acos((r1-r2)/np.linalg.norm(c1-c2))
    
    t1StartX=c1[0]+math.cos(angle1+angle2)*r1
    t1StartY=c1[1]+math.sin(angle1+angle2)*r1
    t1EndX=c2[0]+math.cos(angle1+angle2)*r2
    t1EndY=c2[1]+math.sin(angle1+angle2)*r2
    
    t2StartX=c1[0]+np.cos(angle1-angle2)*r1
    t2StartY=c1[1]+np.sin(angle1-angle2)*r1
    t2EndX=c2[0]+np.cos(angle1-angle2)*r2
    t2EndY=c2[1]+np.sin(angle1-angle2)*r2
    
    
    t1 = [[t1StartX,t1StartY],[t1EndX,t1EndY]]
    t2 = [[t2StartX,t2StartY],[t2EndX,t2EndY]]
    return t1,t2



def convertCoordinates(p1,p2,p3):#p1 should be center of ball 1, since we project it on 0,0 and p2 to be on x axis

    u=p2-p1
    v=p3-p1
    
    u=u/np.linalg.norm(u)
    v=v/np.linalg.norm(v)
    
    
    #project p1 to [0,0], hence move p2,p3 accordingly
    p2_x = np.dot(u,p2-p1)
    p2_y = np.dot(v,p2-p1)
    
    p3_x = np.dot(u,p3-p1)
    p3_y = np.dot(v,p3-p1)
    
    #rotate projected points
    alpha = np.arctan2(p2_y,p2_x)
    p2_xx = p2_x * np.cos(alpha) + p2_y * np.sin(alpha)
    p2_yy = -p2_x * np.sin(alpha) + p2_y * np.cos(alpha)
    p3_xx = p3_x * np.cos(alpha) + p3_y * np.sin(alpha)
    p3_yy = -p3_x * np.sin(alpha) + p3_y * np.cos(alpha)
    
    return np.array((0,0)),np.array((round(p2_xx,4),round(p2_yy,4))),np.array((round(p3_xx,4),round(p3_yy,4)))

def swapIfBigger(r1,c1,r2,c2):
    if(r1 < r2):
        rTmp=r2
        cTmp=c2
        r2=r1
        c2=c1
        r1=rTmp
        c1=cTmp
    return c1,r1,c2,r2

def checkContainment(c1,r1,c2,r2,p):
    p1,p2,p3 = convertCoordinates(c1,c2,p)
    t1,t2 = outerTangents(r1, p1, r2, p2)
    t1A = t1[0]
    t1B=t1[1]
    t2A = t2[0]
    t2B=t2[1]
    
    if((np.linalg.norm(p-c1)<r1) or (np.linalg.norm(p-c2)<r2)):
        return True
    else:
        sign1 = (p[0]-t1A[0])*(t1B[1]-t1A[1])-(p[1]-t1A[1])*(t1B[0]-t1A[0])
        sign2 = (p[0]-t2A[0])*(t2B[1]-t2A[1])-(p[1]-t2A[1])*(t2B[0]-t2A[0])
        if((sign1 >= 0 and sign2 <=0) and (np.linalg.norm(np.array((p[0],0))-p1)<=np.linalg.norm(p1-p2)) and (np.linalg.norm(np.array((p[0],0))-p2)<=np.linalg.norm(p1-p2))):
            return True
        return False
    
def pruneSamples(balls,samples):
    n = len(balls)
    if n<3:
        return samples
    else:
        for j in range(1,n-1):
            for i in range(j):
                for k in range(j+1,n):
                    c1 = balls[i][0]
                    r1 = balls[i][1]
                    c2 = balls[k][0]
                    r2 = balls[k][1]
                    print('before Pruning sample inside Ball',j)
                    samples[j] = np.array([p for p in samples[j] if checkContainment(c1, r1, c2, r2, p)])
                    print('after sample inside Ball',j)
                    
    return samples

def isStabbable(balls, samples):
    n = len(balls)
    if n<3:
        return True
    else:
        for j in range(1,n):
            for i in range(j):
                for k in range(j+1,n):
                    c1 = balls[i][0]
                    r1 = balls[i][1]
                    c2 = balls[k][0]
                    r2 = balls[k][1]
                    #print('before Containmentcheck sample inside Ball',j)
                    points = [p for p in samples[j] if checkContainment(c1, r1, c2, r2, p)]
                    #print('after Containmentcheck sample inside Ball',j)
                    if len(points) == 0:
                        return False
        return True
    
def isStabbableTrue(balls, samples):
    n = len(balls)
    if n<3:
        return True
    else:
        for j in range(1,n):
            for i in range(j):
                c1 = balls[i][0]
                r1 = balls[i][1]
                c2 = balls[n-1][0]
                r2 = balls[n-1][1]
                #print('before Containmentcheck sample inside Ball',j)
                points = [p for p in samples[j] if checkContainment(c1, r1, c2, r2, p)]
                #print('after Containmentcheck sample inside Ball',j)
                if len(points) == 0:
                    return False
        return True
    
def twoApproximation(balls, samples):#see guibas
    start = 0;
    end=0;
    lastTestPassed = True
    print('StartTesting')
    while end < len(balls):
        
        if lastTestPassed:
            #print('EndTesting')
            end+=1
            print(end)
            lastTestPassed = isStabbableTrue(balls[start:end:1], samples[start:end:1])
        else:
            #print('EndTesting')
            print('StartPruning')
            samples[start:end-1:1] = pruneSamples(balls[start:end-1:1], samples[start:end-1:1])
            print('EndPruning')
            start = end
            lastTestPassed=True
    print('EndTesting') 
    return computeStabber(samples),samples
        
#curve = computeStabber(sampleArray)

curve,sampleArray = twoApproximation(balls,samples)
#print(curve)


#c1,c2,p = convertCoordinates(np.array((0,0,1)),np.array((2,1,1)),np.array((0,1,1)))
#t1,t2 = outerTangents(.5,c1,1.5,c2)


#c1= plt.Circle((c1[0],c1[1]), .5, color = 'r')
#c2= plt.Circle((c2[0],c2[1]), 1.5, color = 'b')
#fig, ax = plt.subplots()
#plt.xlim(-2, 5)
#plt.ylim(-2, 5)
#ax.plot(p[0],p[1], 'o', color = 'g')
#t1xs=[t1[0][0],t1[1][0]]
#t1ys=[t1[0][1],t1[1][1]]
#ax.plot(t1xs,t1ys, color='black')
#t2xs=[t2[0][0],t2[1][0]]
#t2ys=[t2[0][1],t2[1][1]]
#ax.plot(t2xs,t2ys, color='black')
#ax.add_patch(c1)
#ax.add_patch(c2)
#ax.set_aspect('equal', adjustable='datalim')
#ax.plot()
#plt.show()
#plot starts here
fig, ax = plt.subplots(1, 1, subplot_kw={'projection':'3d'})
xs=[]
ys=[]
zs=[]
for i in range(len(sampleArray)):
    for j in range(len(sampleArray[i])):
        xs.append(sampleArray[i][j][0])
        ys.append(sampleArray[i][j][1])
        zs.append(sampleArray[i][j][2])
        
for i in range(len(sampleArray)):
    ax.scatter(xs,ys,zs, s=10, c='r', zorder=10)
ax.plot(curve[:,0], curve[:,1], curve[:,2], color = 'black')