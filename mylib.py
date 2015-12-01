
#we only do minimal check here
def distance(x, y):
    sum = 0
    if type(x) == tuple:        
	    for p in  zip(x,y):
	        v1, v2 = p
	        sum += (v1 - v2) ** 2
	    return sum ** 0.5
    else:
            return abs(x - y)
        
        

if __name__ == '__main__':

    print("testing function distance")
    x = (1,2,4)
    y = (0,3,4)
    d = distance(x,y)
    print("distance of " + str(x) + " and " + str(y) + " is: " + str(d))
