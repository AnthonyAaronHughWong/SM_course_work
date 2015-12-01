import kmeans as km
import numpy as np

trainA = np.loadtxt('trainA.txt')
trainB = np.loadtxt('trainB.txt')
testA = np.loadtxt('testA.txt')
testB = np.loadtxt('testB.txt')






def gmm_init(k, samples):
    """
    init a gauss mixture model for all samples
    using kmeans algorithm
    """
    centers = km.kmeans(k, samples)
    clusters =  km.cluster(samples, centers)
    return clusters
    




if __name__ == '__main__':
    km.kmeans(2, trainA[:,0])
