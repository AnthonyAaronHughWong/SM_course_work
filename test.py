import pdb
from numpy import array


paramses = [[(-10.546849183086746, [[ 7.38354114]], 565.57309805845068), (-10.576477482243165, [[ 7.62103462]], 479.42690194154858)], [(-13.576522973528256, [[ 13.91879451]], 473.07544250353891), (-13.464244404677721, [[ 16.06230521]], 372.9245574964612)]]


paramses = [[(-10.546849183086746, array([[ 7.38354114]]), 565.57309805845068), (-10.576477482243165, array([[ 7.62103462]]), 479.42690194154858)], [(-13.576522973528256, array([[ 13.91879451]]), 473.07544250353891), (-13.464244404677721, array([[ 16.06230521]]), 372.9245574964612)]]

def density(params):
    print(params)
#    if len(params) == 3:
    pdb.set_trace()
    for param in params:
#        pdb.set_trace()
        try:
            center, deviation, weight = param
        except TypeError:
            pdb.set_trace()
    return 1

max(enumerate(paramses), key= lambda x: density(x[1]))
