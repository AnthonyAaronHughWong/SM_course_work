import math
from _collections_abc import Set as _Set, Sequence as _Sequence

#we only do minimal check here
def distance(x, y):

#    if isinstance(x, _Set):
#            x = tuple(x)
#            y = tuple(y)


#    if isinstance(x, _Sequence):
    try:
        sum = 0
        for p in  zip(x,y):
            v1, v2 = p
            sum += (v1 - v2) ** 2
            return sum ** 0.5
    except TypeError:
    #    else:
        return abs(x - y)
        
        
def gausspdf(s, mean, sig):        
    return math.exp( - (s - mean)**2/(sig*2)) / math.sqrt( sig)
    
if __name__ == '__main__':

    print("testing function distance")
    x = (1,2,4)
    y = (0,3,4)
    d = distance(x,y)
    print("distance of " + str(x) + " and " + str(y) + " is: " + str(d))



def classifier(sample, paramses, density):
    """classfier a sample based on a model"""
    try:
        return max(range(len(paramses)), key= lambda x: density(sample, paramses[x]))
    except ValueError:
        pdb.set_trace()


def statTrueRate(samples, paramses, classifier, result):
    true = 0
    for sample in samples:
        inx = classifier(sample, paramses)
        if inx == result:
            true += 1
    return true
