import matplotlib.pyplot as plt
import numpy as np
from readData import oneTrack
from stabbing import stabbing_path
from datetime import datetime
import time
import os
import csv

balls = []


print('parsingSingleTrack')
track=oneTrack()
for i in range(10):
    track[i] = 10000*track[i]
    balls.append([track[i], 1])
print(track[1])


N=int(100 * np.log(len(balls)))
seed = 12345

start_time = time.time()
curve, sampleArray = stabbing_path(balls,N,seed)
running_time= round(time.time() - start_time,4)


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

fig, ax = plt.subplots()
ax.plot(curve[:,0], curve[:,1], color = 'black')
xs =[]
ys=[]
for i in range(10):
        xs.append(track[i][0])
        ys.append(track[i][1])
ax.plot(xs,ys, color = 'red')

fig.savefig(path+'/plot.pdf')  


keys = ['Input lattitude','Input longitude', 'Input size', 'Output lattitude','Output longitude', 'Output size', 'running time (secs)','seed']
values = [xs, ys, len(track)-1,curve[:,0],curve[:,1],len(curve)-1,running_time,seed]
dict_data = dict(zip(keys, values))


csv_columns = ['Input lattitude','Input longitude', 'Input size', 'Output lattitude','Output longitude', 'Output size', 'running time (secs)','seed']
csv_file = path+'/results.csv'
with open(csv_file, 'w') as f:
    for key in dict_data.keys():
        f.write("%s, %s\n" % (key, dict_data[key]))