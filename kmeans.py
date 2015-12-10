#! /usr/bin/python3
import random
import numpy as np
import mylib as mylib
import functools
import collections
import timeit

def nearst( sample, initials, distance=mylib.distance):

    """find nearst center and return a tuple of the index and the center"""
    return min(enumerate(initials),key=lambda x : distance( x[1], sample ))

def cluster(samples, initials, nearst= functools.partial(nearst, distance = mylib.distance)):
    """cluster around every initials
    this may be used after kmeans to group points
    I use linked list to collect samples
    """
    # number of clusters are not large, so I used list
    samples_cluster = [collections.deque() for _ in initials]
    for sample in samples:        
        inx, center = nearst(sample, initials)
        samples_cluster[inx].append( sample)

    return samples_cluster

def kmeans_iter(samples,  initials, nearst= functools.partial(nearst, distance = mylib.distance),
           add=np.add, div = np.divide, zeros_like = np.zeros_like):
    
    """
    perform 1 kmeans clustering iteration
    needed:          
    initial guesses  
    distance function
    I have a delimma here: whether to store samples of each cluster or not
    if I do, more time and space are required
    if I don't, I'll need to get it at the last iter
    vector sum of samples within every cluster
    """
    
    sum_samples = zeros_like(initials)
    #number of samples within very cluster
    num_samples = np.zeros(len(sum_samples))
    #find nearest center
    for sample in samples:        
        inx, center = nearst(sample, initials)
        sum_samples[inx] = add(sum_samples[inx], sample)
        num_samples[inx] += 1
        
    return map(div, sum_samples, num_samples)

def kmeans_init(k, samples):

    """randomly init kmeans"""
    return random.sample(list(samples), k)


def kmeans(k, samples, max_iter=6, nearst= functools.partial(nearst, distance = mylib.distance),
           add=np.add, div = np.divide, zeros_like = np.zeros_like):

    """wrapper of kmeans"""
    
    initials = kmeans_init(k, samples)
    for _ in range(max_iter):
        centers = kmeans_iter(samples, initials, nearst, add, div, zeros_like)
        # it seems there's no better way than list
        centers = list(centers)
        if np.allclose(centers, initials):            
            return centers
        initials = centers
        
    return initials


samples=[[1,2],[3,5],[60,65]]
initials=[[-1,-8],[1,1]]
trainA = np.loadtxt('trainA.txt')
trainB = np.loadtxt('trainB.txt')
testA = np.loadtxt('testA.txt')
testB = np.loadtxt('testB.txt')
if __name__ == '__main__':

    print (nearst( samples[0],initials, mylib.distance))
    print (kmeans(2,trainA))
    print (kmeans(2,trainB))
    t=timeit.Timer('kmeans(6, trainA, 20)',
                   'from kmeans import kmeans, trainA')
    print(t.timeit(1))
    
