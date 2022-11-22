# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 09:59:26 2022

@author: Alex
"""
import numpy as np


def normalized_gaussian(dim, radius, center, N): # muller
    X = np.random.randn(dim, N)
    norm = np.linalg.norm(X, axis=0)

    r = np.random.rand(N)**(1/dim)*radius
    return X*r / norm + center


def rejection_sampling(dim, radius, center, N):
    points = []

    for i in range(N):
        while True:
            p = np.random.rand(dim) * 2 - 1
        
            if np.linalg.norm(p) < 1:
                break
        p *= radius
        p+=center
        points.append(p)
    return points  