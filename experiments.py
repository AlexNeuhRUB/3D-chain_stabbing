import matplotlib.pyplot as plt
import numpy as np
import readData as rd
from stabbing import stabbing_path
from datetime import datetime
import time
import os
import json

radius = 1
tracks,ids=rd.parseTracks()


current_time = datetime.now()
timestamp = current_time.timestamp()
date_time = datetime.fromtimestamp(timestamp)
str_date_time = date_time.strftime("%d-%m-%Y_%H_%M_%S")

for tr in [0,1,9]:
    path = "stabbing/Track"+str(ids[tr])+'_'+ str_date_time
    d = {"Track ID":[], "radius":[], "epsilon":[], "Input size":[], "Output size":[], "running time (secs)":[],"Input lattitude":[],"Input longitude":[], "Output lattitude":[],"Output longitude":[]}
# Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The new directory is created!")
    for epsilon in [.3,.4,.5]:
        os.makedirs(path +'/eps'+str(epsilon))
        tr_exp = ids[tr]
        for k in range(10):
            track = tracks[tr].copy()
            balls = []
            m= len(track)
            for i in range(m):
                track[i] = 10000*track[i]
                balls.append([track[i], radius])
            
            print('Experiment '+str(k)+' starting')
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
                
            fig.savefig(path+'/eps'+str(epsilon)+'/exp_'+str(k)+'.svg')  
            fig.clear()
            plt.close()
            d["Track ID"].append(str(tr_exp))
            d["radius"].append(str(radius))
            d["epsilon"].append(str(epsilon))
            d["Input size"].append(len(track)-1)
            d["Output size"].append(len(curve)-1)
            d["running time (secs)"].append(running_time)
            d["Input lattitude"].append(xs)
            d["Input longitude"].append(ys)
            d["Output lattitude"].append(curve[:,0].tolist())
            d["Output longitude"].append(curve[:,1].tolist())
        print('Experiment '+str(k)+' finished')


    with open(path+'/results.json', 'w') as fp:
        json.dump(d,fp, indent=4)
    d = {"Track ID":[], "radius":[], "epsilon":[], "Input size":[], "Output size":[], "running time (secs)":[],"Input lattitude":[],"Input longitude":[], "Output lattitude":[],"Output longitude":[]}
   
