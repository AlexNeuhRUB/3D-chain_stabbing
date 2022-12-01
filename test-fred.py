import Fred as fred
import numpy as np
import pandas as pd

curve1d = fred.Curve([1., 2.]) # Curve stores a polygonal curve with 
                                         # at least two points of at least one 
                                         # and equal number of dimensions

curve2d1 = fred.Curve([[1., 0.], [2., 1.], [3., 0.]]) # any number of dimensions and points works
curve2d2 = fred.Curve([[1., -1.], [2., -2.], [3., -1.]], "optional name, e.g. displayed in plot") 

print(curve2d1)

fred.plot_curve(curve2d1, curve2d2)
fred.plot_curve(curve2d2, fred.minimum_error_simplification(curve2d2, 2))

print("distance is {}".format(fred.continuous_frechet(curve2d1, curve2d2).value))

print("download HUGE curves") 

import requests, zipfile, io             # you can use all libraries 
                                         # that work with numpy to read data into fred
                                         
re = requests.get("https://archive.ics.uci.edu/ml/machine-learning-databases/00447/data.zip", stream=True)
zf = zipfile.ZipFile(io.BytesIO(re.content))

ps1 = fred.Curve(pd.read_csv(zf.open('PS1.txt'), delimiter="\t", header=None).values[:50], "PS1")
ps2 = fred.Curve(pd.read_csv(zf.open('PS2.txt'), delimiter="\t", header=None).values[:50], "PS2")
ps3 = fred.Curve(pd.read_csv(zf.open('PS3.txt'), delimiter="\t", header=None).values[:50], "PS3")
ps4 = fred.Curve(pd.read_csv(zf.open('PS4.txt'), delimiter="\t", header=None).values[:50], "PS4")
ps5 = fred.Curve(pd.read_csv(zf.open('PS5.txt'), delimiter="\t", header=None).values[:50], "PS5")
ps6 = fred.Curve(pd.read_csv(zf.open('PS6.txt'), delimiter="\t", header=None).values[:50], "PS6")

curves = fred.Curves() # for clustering or if you want to apply dimension reduction
                       # you need to encapsulate your curves in a Curves object
              
curves.add(ps1)
curves.add(ps2)
curves.add(ps3)
curves.add(ps4)
curves.add(ps5)
curves.add(ps6)

fred.plot_curve(curves)

curves = fred.dimension_reduction(curves, 0.95) # fred is pretty fast but with high dimensional data
                                                # a dimension reduction massively improves running-time
                                                # even for smaller values of epsilon
                                                
fred.plot_curve(curves)
                                  
# Oneshot clustering - if you already know the value of k
                                  
clustering = fred.discrete_klcenter(2, 10, curves) # fast but coarse
          
clustering = fred.discrete_klmedian(2, 10, curves) # slow but better results

print("clustering cost is {}".format(clustering.value))

for i, center in enumerate(clustering):
    print("center {} is {}".format(i, center))

fred.plot_curve(clustering)

# Multiple clustering calls - if you need to find a suitable value for k
                            
for k in range(2, 6):
    
    clustering = fred.discrete_klcenter(k, 10, curves, consecutive_call=True)
    print("clustering cost is {}".format(clustering.value))
            
    clustering = fred.discrete_klmedian(k, 10, curves, consecutive_call=True)
    print("clustering cost is {}".format(clustering.value))

clustering.compute_assignment(curves, consecutive_call=True) # use consecutive_call = False when computing assignment for curves other
                                                             # than those used for computing the clustering

for i in range(0, len(clustering)):
    for j in range(0, clustering.assignment.count(i)):
        print("{} was assigned to center {}".format(curves[clustering.assignment.get(i,j)].name, clustering[i].name))