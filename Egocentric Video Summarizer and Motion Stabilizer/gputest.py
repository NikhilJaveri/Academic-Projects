#import numpy as np
#from numbapro import vectorize
#import sys
#import time

#@vectorize(['float32(float32, float32)',
#            'float64(float64, float64)'], identity=1)
#def sum(a, b):
#    return a + b

#@vectorize
#def sum(a, b):
#    return a + b

#@vectorize(identity=1)
#def mul(a, b):
#    return a * b

#def main():

#    start = time.time()

#    a = np.ones(shape = (10000,10000))*3
#    b = np.ones(shape = (10000,10000))*2

#    c = mul(a,b)

#    d = sum(a,b)

#    #print(str(c) + "...." + str(d))
#    print("Time taken is " + str(time.time() - start))

#if __name__ == "__main__":
#    sys.exit(int(main() or 0))