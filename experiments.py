import matplotlib.pyplot as plt
import numpy as np
import readData as rd
from stabbing import stabbing_path
from datetime import datetime
import time
import os
import json

radius = .1
epsilon=.5
tracks,ids=rd.parseTracks()

for k in range(100):
    print('Experiment '+str(k)+' starting')
    current_time = datetime.now()
    timestamp = current_time.timestamp()
    date_time = datetime.fromtimestamp(timestamp)
    str_date_time = date_time.strftime("%d-%m-%Y_%H_%M_%S")
    path = "stabbing/" + str_date_time
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:

        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The new directory is created!")
    for l in [0,1,9]:
        directory = path+'/Track'+str(ids[l])
        if not isExist:
            os.makedirs(directory)
        track = tracks[l]
        balls = []
        m= len(track)
        for i in range(m):
            track[i] = 10000*track[i]
            balls.append([track[i], radius])
        
    
        start_time = time.process_time()
        curve, sampleArray = stabbing_path(balls,epsilon)
        running_time = round(time.process_time() - start_time,4)
    
        fig, ax = plt.subplots()
        ax.plot(curve[:,0], curve[:,1], color = 'black')
        xs =[]
        ys=[]
        for i in range(m):
            xs.append(track[i][0])
            ys.append(track[i][1])
        ax.plot(xs,ys, color = 'red')
    
        fig.savefig(directory+'/plot_for_track'+str(ids[l])+'.svg')  
        fig.clear()
        plt.close()
        
        keys = ['Track ID', 'radius', 'epsilon', 'Input size', 'Output size', 'running time (secs)','Input lattitude','Input longitude', 'Output lattitude','Output longitude']
        values = [str(ids[l]),  str(radius), str(epsilon),len(track)-1,len(curve)-1,running_time, xs, ys, curve[:,0].tolist(),curve[:,1].tolist()]
        dict_data = dict(zip(keys, values))

        with open(directory+'/result_track'+str(ids[l])+'.json', 'w') as fp:
            json.dump(dict_data,fp, indent=4)
        print('Experiment '+str(k)+' finished')