#! env python3
import kmeans as km
import numpy as np
import mylib as mylib
import gmm as gmm
from scipy.stats import multivariate_normal
import pdb

def classifier(sample, params, density= lambda s,c,d: multivariate_normal(mean = c, cov = d).pdf(s)
):
    """classfier a sample based on gmm model"""
    
    for i in range(k):
        density(sample, params[i][0], params[i][1])


if __name__ == '__main__':

