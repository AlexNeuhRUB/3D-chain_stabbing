# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 14:37:15 2022
@author: Alex
"""

import matplotlib.pyplot as plt

from readData import oneTrack
from stabbing import stabbing_path


balls = []


print('parsingSingleTrack')
track=oneTrack()
for i in range(len(track)):
    track[i] = 10000*track[i]
    balls.append([track[i], 1])
print(track[1])


curve, sampleArray = stabbing_path(balls)

fig, ax = plt.subplots()
ax.plot(curve[:,0], curve[:,1], color = 'black')
xs =[]
ys=[]
for i in range(len(track)):
        xs.append(track[i][0])
        ys.append(track[i][1])
ax.plot(xs,ys, color = 'red')

plt.show()

