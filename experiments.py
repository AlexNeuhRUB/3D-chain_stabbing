import matplotlib.pyplot as plt
import numpy as np
import readData as rd
from stabbing import stabbing_path
from datetime import datetime
import time
import os
import json


tracks=rd.parseTracks()
current_time = datetime.now()
timestamp = current_time.timestamp()
date_time = datetime.fromtimestamp(timestamp)
str_date_time = date_time.strftime("%d-%m-%Y_%H_%M_%S")
path = "Experiment_" + str_date_time
# Check whether the specified path exists or not
isExist = os.path.exists(path)
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs(path)
   print("The new directory is created!")


for l in range(len(tracks)):
    track = tracks[l]
    balls = []
    m= len(track)
    for i in range(m):
        track[i] = 10000*track[i]
        balls.append([track[i], 1])


    start_time = time.process_time()
    curve, sampleArray = stabbing_path(balls)
    running_time = round(time.process_time() - start_time,4)

    fig, ax = plt.subplots()
    ax.plot(curve[:,0], curve[:,1], color = 'black')
    xs =[]
    ys=[]
    for i in range(m):
        xs.append(track[i][0])
        ys.append(track[i][1])
    ax.plot(xs,ys, color = 'red')

    fig.savefig(path+'/plot_track'+str(l+1)+'.svg')  
    fig.clear()

    keys = ['Input lattitude','Input longitude', 'Input size', 'Output lattitude','Output longitude', 'Output size', 'running time (secs)']
    values = [xs, ys, len(track)-1,curve[:,0].tolist(),curve[:,1].tolist(),len(curve)-1,running_time]
    dict_data = dict(zip(keys, values))

    with open(path+'/result_track'+str(l+1)+'.json', 'w') as fp:
        json.dump(dict_data,fp, indent=4)
