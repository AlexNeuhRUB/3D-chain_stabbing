# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 14:37:15 2022

@author: Alex
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from readData import oneTrack
from stabbing import *


n_samples = 500
balls = []


#print('parsingSingleTrack')
#track=oneTrack()
#for i in range(10):
#    balls.append([track[i], 1])
#print(track[1])

r1 = .5
c1 = np.array((0,0,0))
r2 = .5
c2 = np.array((1,1,0))
r3 = .5
c3 = np.array((2,0,0))
r4 = 1
c4 = np.array((3,0,0))
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


balls = [[c1,r1],[c2,r2],[c3,r3],[c4,r4]]#,[c5,r5],[c6,r6],[c6,r6],[c7,r7],[c8,r8],[c9,r9]]


#function test data ends here

        
#curve = computeStabber(sampleArray)

curve, sampleArray = stabbing_path(balls, n_samples)
#print(curve)


#c1,c2,p = convertCoordinates(np.array((0,0,1)),np.array((2,1,1)),np.array((0,1,1)))
#t1,t2 = outerTangents(.5,c1,1.5,c2)

fig, ax = plt.subplots()


c = list()

for i in range(len(balls)):
    c.append(plt.Circle((balls[i][0][0],balls[i][0][1]), balls[i][1]))
    ax.add_patch(c[i])

#plt.xlim(-2, 5)
#plt.ylim(-2, 5)
#ax.plot(p[0],p[1], 'o', color = 'g')
#t1xs=[t1[0][0],t1[1][0]]
#t1ys=[t1[0][1],t1[1][1]]
#ax.plot(t1xs,t1ys, color='black')
#t2xs=[t2[0][0],t2[1][0]]
#t2ys=[t2[0][1],t2[1][1]]
#ax.plot(t2xs,t2ys, color='black')

for i in range(len(sampleArray)):
    ax.scatter(sampleArray[i][:,0], sampleArray[i][:,1])
ax.plot(curve[:,0], curve[:,1], color = 'black')
#ax.set_aspect('equal', adjustable='datalim')
ax.plot()
plt.show()
#plot starts here
#fig = plt.figure()
#ax = Axes3D(fig)
#ax.set_xlim3d(-10.942, -10.938)
#ax.set_ylim3d(-37.063, -37.0575)
#ax.set_zlim3d(.99, 1.01)
#xs=[]
#ys=[]
#zs=[]
#xxs=[]
#yys=[]
#zzs=[]

#for i in range(30):
#    for j in range(len(samples[i])):
#        xs.append(samples[i][j][0])
#        ys.append(samples[i][j][1])
#        zs.append(samples[i][j][2])
        
#for i in range(len(sampleArray)):
#    ax.scatter(xs,ys,zs,  c='r')
#for i in range(len(track[i])):
#        xxs.append(track[i][0])
#        yys.append(track[i][1])
#        zzs.append(track[i][2])
#ax.plot(xxs,yys,zzs, color = 'blue')
ax.plot(curve[:,0], curve[:,1], color = 'black')
