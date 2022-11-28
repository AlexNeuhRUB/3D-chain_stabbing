import numpy as np
import math
from scipy import optimize
from ballSampling import rejection_sampling

def angle(vec1, vec2):
    angle = np.arccos(np.dot(vec1 / (np.linalg.norm(vec1)), (vec2/np.linalg.norm(vec2))))
    return angle

def f(x, *args):
    if len(x) < 3:
        return -np.pi
    samples = args[0]
    y = [int(xs) for xs in x]
    curve = list()
    vectors = list()
    tmp = list()
    for i in range(len(y)):
        curve.append(samples[i][y[i]])
    for i in range(len(y)-1):
        vectors.append(curve[i+1]-curve[i])
    for i in range(len(vectors)-1):
        tmp.append(-angle(vectors[i],vectors[i+1]))
    return min(tmp)

def computeStabber(samples, start, end):

    n = end - start

    listZip = [0] * n

    res = optimize.dual_annealing(f, args=(samples,), bounds=list(zip(listZip,[len(samples[i])-0.001 for i in range(start, end)])))

    xf = res['x']
    curveList = []
    for i in range(start, end):
        curveList.append(samples[i][int(xf[i-start])])
    return(np.array(curveList))

def outerTangents(r1, c1, r2, c2):
    angle1 = math.atan2(c2[1] - c1[1], c2[0] - c1[0])
    angle2 = math.acos((r1-r2) / np.linalg.norm(c1 - c2))

    t1StartX = c1[0] + math.cos(angle1 + angle2) * r1
    t1StartY = c1[1] + math.sin(angle1 + angle2) * r1
    t1EndX = c2[0] + math.cos(angle1 + angle2) * r2
    t1EndY = c2[1] + math.sin(angle1 + angle2) * r2

    t2StartX = c1[0] + np.cos(angle1 - angle2) * r1
    t2StartY = c1[1] + np.sin(angle1 - angle2) * r1
    t2EndX = c2[0] + np.cos(angle1 - angle2) * r2
    t2EndY = c2[1] + np.sin(angle1 - angle2) * r2


    t1 = [[t1StartX, t1StartY], [t1EndX, t1EndY]]
    t2 = [[t2StartX, t2StartY], [t2EndX, t2EndY]]
    return t1,t2

def convertCoordinates(p1, p2, p3):
    """p1 should be center of ball 1, since we project it on 0,0 and p2 to be on x axis"""

    u = p2 - p1
    v = p3 - p1

    u = u / np.linalg.norm(u)
    v = v / np.linalg.norm(v)


    #project p1 to [0,0], hence move p2,p3 accordingly
    p2_x = np.dot(u, p2 - p1)
    p2_y = np.dot(v, p2 - p1)

    p3_x = np.dot(u, p3 - p1)
    p3_y = np.dot(v, p3 - p1)

    #rotate projected points
    alpha = np.arctan2(p2_y, p2_x)
    p2_xx = p2_x * np.cos(alpha) + p2_y * np.sin(alpha)
    p2_yy = -p2_x * np.sin(alpha) + p2_y * np.cos(alpha)
    p3_xx = p3_x * np.cos(alpha) + p3_y * np.sin(alpha)
    p3_yy = -p3_x * np.sin(alpha) + p3_y * np.cos(alpha)

    return np.array((0,0)), np.array((round(p2_xx,4),round(p2_yy,4))), np.array((round(p3_xx,4), round(p3_yy,4)))

def swapIfBigger(r1, c1, r2, c2):
    if(r1 < r2):
        rTmp = r2
        cTmp = c2
        r2 = r1
        c2 = c1
        r1 = rTmp
        c1 = cTmp
    return c1, r1, c2, r2

def checkContainment(c1, r1, c2, r2, p):
    p1,p2,p3 = convertCoordinates(c1, c2, p)
    t1,t2 = outerTangents(r1, p1, r2, p2)
    t1A = t1[0]
    t1B = t1[1]
    t2A = t2[0]
    t2B = t2[1]

    if((np.linalg.norm(p-c1) <= r1) or (np.linalg.norm(p-c2) <= r2)):
        return True
    else:
        sign1 = (p[0] - t1A[0]) * (t1B[1] - t1A[1]) - (p[1] - t1A[1]) * (t1B[0] - t1A[0])
        sign2 = (p[0] - t2A[0]) * (t2B[1] - t2A[1]) - (p[1] - t2A[1]) * (t2B[0] - t2A[0])
        if((sign1 >= 0 and sign2 <=0)
           and (np.linalg.norm(np.array((p[0],0)) - p1) <= np.linalg.norm(p1 - p2))
           and (np.linalg.norm(np.array((p[0], 0)) - p2) <= np.linalg.norm(p1 - p2))):
            return True
        return False

def pruneSamples(balls, samples, start, end):
    n = end - start
    if n < 3:
        return samples
    else:
        for j in range(start + 1, end-1):
            for i in range(start, j):
                for k in range(j+1, end):
                    c1 = balls[i][0]
                    r1 = balls[i][1]
                    c2 = balls[k][0]
                    r2 = balls[k][1]
                    samples[j] = np.array([p for p in samples[j] if checkContainment(c1, r1, c2, r2, p)])

    return samples

def isStabbable(balls, samples, start, end):
    n = end - start
    if n < 3:
        return True
    else:
        for j in range(start+1, end):
            for i in range(start, j):
                for k in range(j+1, end):
                    c1 = balls[i][0]
                    r1 = balls[i][1]
                    c2 = balls[k][0]
                    r2 = balls[k][1]
                    points = [p for p in samples[j] if checkContainment(c1, r1, c2, r2, p)]
                    if len(points) == 0:
                        return False
        return True

def isStabbableTrue(balls, samples, start, end):
    n = end - start
    if n < 3:
        return True
    else:
        for j in range(start + 1, end):
            for i in range(start, j):
                c1 = balls[i][0]
                r1 = balls[i][1]
                c2 = balls[end-1][0]
                r2 = balls[end-1][1]
                points = [p for p in samples[j] if checkContainment(c1, r1, c2, r2, p)]
                if len(points) == 0:
                    return False
        return True

def stabbing_path(balls, n_samples):
    samples = list()
    segments = list()
    for i in range(len(balls)):
        samples.append(rejection_sampling(3, balls[i][1], balls[i][0], n_samples))
    start = 0;
    end = 0;
    stabbable = True
    while end < len(balls):
        if stabbable:
            end += 1
            stabbable = isStabbableTrue(balls, samples, start, end)
            print(start, end, stabbable)
        else:
            samples = pruneSamples(balls, samples, start, end-1)
            segments.append(computeStabber(samples, start, end-1))
            start = end
            stabbable = True
    if not stabbable:
        samples = pruneSamples(balls, samples, start, end-1)
    #print('EndTesting')
    return np.concatenate(segments), samples
