#!env python3
import kmeans as km
import numpy as np
from  mylib import gausspdf
import mylib as mylib
import gmm as gmm
import pdb
import functools






def density_gmm(sample, params):
    """density for gauss mixture model"""
    pdf = 0
    for param in params:
            center, deviation, weight = param
            pdf += weight*gausspdf(sample, center, deviation)
            #multivariate_normal(mean = center, cov = deviation).pdf(sample)
    return pdf

def density_gmm_m(samples, params):
    """density for gauss mixture model, but a multiply of several independent gmm"""
    pdf = 1
    for param, sample  in zip(params, samples):
        pdf *= density_gmm(sample, param)
    return pdf


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

    
    #for i in range(n_classes):
    #    train = trains[i]
    #    paramses[i] = gmm.gmm(k, train, 4)
    #
    #print(paramses)

    classifier = functools.partial(mylib.classifier, density = density_gmm_m)
    def dotest(k, max_iter):
        
        print('Model Number is ' + str(k))
        input("Press Enter to Continue: ")
        for i in range(n_classes):
            train = trains[i]
            d = np.shape(train)[1]
            dparams = [None]*d
            for j in range(d):
                dparams[j] = gmm.gmm(k,[x[j] for x in train], max_iter)
            paramses[i] = dparams
        for i, params in enumerate(paramses):
            print("Class " + str(i))
            for j, param in enumerate(params):
                print("    Dimension " + str(j))
                for l, m in enumerate(param):
                    print('            Model ' + str(l))
                    print(m)

        
        input('Params calculated, Press Enter to stat true rate: ')
        testlen = len(testA) + len(testB)    
        rate1 = mylib.statTrueRate(testA, paramses, classifier,  0 ) / testlen
        rate2 = mylib.statTrueRate(testB, paramses, classifier,  1 ) / testlen
        print(rate1 + rate2)


    input('Files loaded, Press Enter to Continue: ')
    for k in ks:        
        dotest(k, max_iter=4)
    
#    classifier()
