import pandas as pd
import numpy as np


def parseTracks():
    tracks=[]
    temptrack=[]
    data = pd.read_csv("go_track_trackspoints.csv")
    temptrack.append(np.array((data.loc[0,'latitude'], data.loc[0,'longitude'],1)))
    for i in range(1,len(data)):
        if data.loc[i,'track_id'] == data.loc[i-1,'track_id']:
            temptrack.append(np.array((data.loc[i,'latitude'], data.loc[i,'longitude'],1)))
        else:
            tracks.append(temptrack)
            temptrack=[]
            temptrack.append(np.array((data.loc[i,'latitude'], data.loc[i,'longitude'],1)))
    return tracks

def oneTrack():
    temptrack=[]
    data = pd.read_csv("go_track_trackspoints.csv")
    temptrack.append(np.array((data.loc[0,'latitude'], data.loc[0,'longitude'],1)))
    print(len(temptrack))
    for i in range(1,len(data)):
        if data.loc[i,'track_id'] == data.loc[i-1,'track_id']:
            temptrack.append(np.array((data.loc[i,'latitude'], data.loc[i,'longitude'],1)))
        else:
            break
    return temptrack
