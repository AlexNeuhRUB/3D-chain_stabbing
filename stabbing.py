import numpy as np
import math
from scipy import optimize
from ballSampling import rejection_sampling

#def angle(vec1, vec2):
#    angle = np.arccos(np.dot((vec2/np.linalg.norm(vec2)),vec1 / (np.linalg.norm(vec1))))
#    print('vec1',vec1)
    #print angleDegrees, vertexType
    
#    return angle

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def f(x, *args):
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

def computeStabber(sampleArray):
    samples = []
    for i in range(len(sampleArray)):
        samples.append(sampleArray[i])

    listZip = [0]*len(sampleArray)

    print('StartOptimizing')
    res = optimize.dual_annealing(f, args=(sampleArray,), bounds=list(zip(listZip,[len(x)-0.001 for x in samples])))

    xf = res['x']
    curveList = []
    for i in range(len(sampleArray)):
        curveList.append(sampleArray[i][int(xf[i])])
    return(np.array(curveList))

def outerTangents(r1,c1,r2,c2):
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

def convertCoordinates(p1,p2,p3):
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

def swapIfBigger(r1,c1,r2,c2):
    if(r1 < r2):
        rTmp = r2
        cTmp = c2
        r2 = r1
        c2 = c1
        r1 = rTmp
        c1 = cTmp
    return c1, r1, c2, r2

def checkContainment(c1,r1,c2,r2,p):
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

def pruneSamples(balls, samples):
    n = len(balls)
    if n < 3:
        return samples
    else:
        for j in range(1, n-1):
            for i in range(j):
                for k in range(j+1, n):
                    c1 = balls[i][0]
                    r1 = balls[i][1]
                    c2 = balls[k][0]
                    r2 = balls[k][1]
                    print('before Pruning sample inside Ball',j)
                    print('i',i)
                    print('k',k)
                    points = np.array([p for p in samples[j] if checkContainment(c1, r1, c2, r2, p)])
                    samples[j] = points
                    print('after sample inside Ball',j)

    return samples

def isStabbable(balls, samples):
    n = len(balls)
    if n < 3:
        return True
    else:
        for j in range(1, n):
            for i in range(j):
                for k in range(j+1, n):
                    c1 = balls[i][0]
                    r1 = balls[i][1]
                    c2 = balls[k][0]
                    r2 = balls[k][1]
                    print('before Containmentcheck sample inside Ball',j)
                    points = [p for p in samples[j] if checkContainment(c1, r1, c2, r2, p)]
                    print('after Containmentcheck sample inside Ball',j)
                    if len(points) == 0:
                        return False
        return True

def isStabbableTrue(balls, samples):
    n = len(balls)
    if n < 3:
        return True
    else:
        for j in range(1, n):
            for i in range(j):
                c1 = balls[i][0]
                r1 = balls[i][1]
                c2 = balls[n-1][0]
                r2 = balls[n-1][1]
                #print('before Containmentcheck sample inside Ball',j)
                points = [p for p in samples[j] if checkContainment(c1, r1, c2, r2, p)]
                #print('after Containmentcheck sample inside Ball',j)
                if len(points) == 0:
                    return False
        return True

def stabbing_path(balls, n_samples):
    samples = list()
    for i in range(len(balls)):
        samples.append(rejection_sampling(3, balls[i][1], balls[i][0], n_samples))
    start = 0;
    end = 0;
    allStabbable= True
    stabbable = True
    print('StartTesting')
    while end < len(balls):
        print(stabbable)
        if stabbable:
            print('EndTesting')
            end += 1
            #print(end)
            stabbable = isStabbableTrue(balls[start:end:1], samples[start:end:1])
            if end==len(balls)-1:
                print('start',start)
                print('end',end)
                samples[start:end:1] = pruneSamples(balls[start:end:1], samples[start:end:1])
        else:
            allStabbable = False
            print('EndTesting')
            print('StartPruning')
            samples[start:end-1:1] = pruneSamples(balls[start:end-1:1], samples[start:end-1:1])
            print('EndPruning')
            start = end
            stabbable = True
    print('EndTesting')
    
    return computeStabber(samples), samples
