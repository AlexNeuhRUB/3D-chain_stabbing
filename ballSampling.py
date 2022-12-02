import numpy as np

def rejection_sampling(dim, radius, center, N):
    points = []
    for i in range(N):
        while True:
            p = np.random.uniform(low=0.0, high=1.0, size=dim) * 2 - 1
        
            if np.linalg.norm(p) <= 1:
                break
        p *= radius
        p += center
        points.append(p)
    return np.array(points)
