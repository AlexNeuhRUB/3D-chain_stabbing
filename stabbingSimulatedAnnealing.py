# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 14:37:15 2022

@author: Alex
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from ballSampling import rejection_sampling

#function test data starts here
N=100
r1 = 1
c1 = np.array((0,0,0))
r2 = 1
c2 = np.array((0,1,0))
r3 = 1
c3 = np.array((0,2,0))
r4 = 1
c4 = np.array((0,3,0))
r5 = 1
c5 = np.array((0,4,0))

sampleBall1 = rejection_sampling(3,r1,c1,N)
sampleBall2 = rejection_sampling(3,r2,c2,N)
sampleBall3 = rejection_sampling(3,r3,c3,N)
sampleBall4 = rejection_sampling(3,r4,c4,N)
sampleBall5 = rejection_sampling(3,r5,c5,N)

sampleArray = np.array([sampleBall1,sampleBall2,sampleBall3,sampleBall4,sampleBall5])
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
        curve.append(sampleArray[i][y[i]])
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

    res = optimize.dual_annealing(f, bounds=list(zip(listZip,[len(x)-0.001 for x in samples])))

    xf = res['x']
    curveList = []
    for i in range(len(sampleArray)):
        curveList.append(sampleArray[i][int(xf[i])])
    return(np.array(curveList))


def isStabbable(balls):
    return(len(balls)<=3)


def twoApproximation(balls):#see guibas
    start = 0;
    stabber=[]
    for i in range(len(balls)):
        if not isStabbable(balls[start:i:1]):
            temp=computeStabber(balls[start:i:1])
            for j in range(len(temp)):
                stabber.append(temp[j])
            start = i
    return np.array(stabber)
        
#curve = computeStabber(sampleArray)

curve = twoApproximation(sampleArray)
print(curve)

#plot starts here
fig, ax = plt.subplots(1, 1, subplot_kw={'projection':'3d', 'aspect':'auto'})
for i in range(len(sampleArray)):
    ax.scatter(sampleArray[i][:,0], sampleArray[i][:,1], sampleArray[i][:,2], s=10, c='r', zorder=10)
ax.plot(curve[:,0], curve[:,1], curve[:,2], color = 'black')