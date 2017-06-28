#import pyximport
#import numpy as np
#import time
#import math

#setup_args = {}

#setup_args = {'options': {'build_ext': {'compiler' : 'mingw32'}}}

#pyximport.install(setup_args = setup_args)

#from cpytest import sincof

#start = time.time()
#a = sincof(5.000)
#print(str(time.time() - start))

#t2 = time.time()
#b = math.sin(5.000)/5.000
#print(str(time.time() - t2))