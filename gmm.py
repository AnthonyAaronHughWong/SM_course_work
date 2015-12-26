#! env python3
import kmeans as km
import numpy as np
from  mylib import gausspdf
import functools
import pdb


def gmm_init(k, samples):
    """
    init a gauss mixture model for all samples
    using kmeans algorithm
    weights don't sum up to 1
    """
    centers = km.kmeans(k, samples)
    clusters =  km.cluster(samples, centers)

    #params is a list of (mean, sigma, weight)
#    shapec = np.shape(centers[0])
    shapes = np.shape(np.outer(samples[0], samples[0]))

    #params = [[np.zeros_like(centers[0]), np.zeros(shapes), 0]]*k
    params = [None]*k
    for i in range(k):
        cluster, center = clusters[i], centers[i]
        num_samples = len(cluster)
        deviation = np.zeros(shapes)
        for sample in cluster:
            diff = sample - center
            deviation += np.outer(diff, diff)
        deviation /= len(cluster)
        params[i] = [center, deviation, num_samples]
    return params
    
#@profile
def gmm_iter(samples, params#, density= lambda s,c,d: multivariate_normal(mean = c, cov = d).pdf(s)
            ):
    """
    run one gmm iter
    return params in the same format
    density: give a probability given a sample and a param

    I'll do best to make it work on arrays
    """
    n_sam = len(samples)
    k = len(params)

    #density = [multivariate_normal(mean = c, cov = d).pdf for c,d,_ in params  ]
    density = [functools.partial(gausspdf, mean = c, sig = d) for c,d,_ in params]
    #tmp variable (per sample)
    sum_resp = [0] * k
    sum_resp_sample = [samples[0]*0]*k
    sum_resp_deviation = [samples[0] ** 2 *0]*k  #[np.outer(samples[0], samples[0])*0]*k

    t = [None]* k
    
    for sample in samples:
        #get responsibilities
        for i in range(k):
            t[i] = density[i](sample)
            t[i] *=  params[i][2]
        t = np.true_divide(t, sum(t))
        #t should contain responsibilities now        
        
        #get these things for every cluster
        #we'll use them to calculate params_en
#        pdb.set_trace()
        for i in range(k):
           sum_resp[i] += t[i]
           sum_resp_sample[i] +=  t[i] * sample
           diff = sample - params[i][0]
           sum_resp_deviation[i] += t[i] * diff ** 2 #np.outer(diff,diff)

    #new params for every one
    for i in range(k):
        center = sum_resp_sample[i] / sum_resp[i]
        deviation = sum_resp_deviation[i] / sum_resp[i]
        weight = sum_resp[i]
        params[i] = [center, deviation, weight]

    return params

def gmm(k, samples, max_iter=5):
    """
    gmm algorithm
    weight sum up to 1
    """
    params = gmm_init(k, samples)
    for i in range(max_iter):
        gmm_iter(samples, params)

    weight = 0
    for param in params:
        weight += param[2]

    for i in range(len(params)):
        params[i][2] /= weight
    return params

#    return [[param[0], param[1], np.divide(param[2],weight)] for param in params]

if __name__ == '__main__':
    trainA = list(np.loadtxt('trainA.txt'))
    trainB = list(np.loadtxt('trainB.txt'))
    testA = list(np.loadtxt('testA.txt'))
    testB = list(np.loadtxt('testB.txt'))
    trains = (trainA, trainB)
    tests = (testA, testB)    
    ks = (2, 4, 6)

    
    n_classes = len(trains)
    paramses = [None]*n_classes


    
    def dotest(k, func,  max_iter):
        
        print('Model Number is ' + str(k))
        input("Press Enter to Continue: ")        
        for i in range(n_classes):
            train = trains[i]
            d = np.shape(train)[1]
            dparams = [None]*d
            for j in range(d):
                dparams[j] = func(k,[x[j] for x in train], max_iter)
            paramses[i] = dparams
        for i, params in enumerate(paramses):
            print("Class " + str(i))
            for j, param in enumerate(params):
                print("    Dimension " + str(j))
                for l, m in enumerate(param):
                    print('            Model ' + str(l))
                    print(m)


    dotest(2, gmm, 1)
