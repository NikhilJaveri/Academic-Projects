import numpy as np
#from PIL import Image
##import os
import sys
#from math import *
#from MyImageLib import *

#from numbapro import uint8, uint32, void
#from numbapro import guvectorize, cuda
#from numba import jit

import cv2
import time
import pyaudio
import wave
#from numba.npyufunc.decorators import guvectorize

# file_name = 'C:\Users\Nikhil\Desktop\Nikhil\USCEE\Spring_2016\CSCI 576\Project\Alin_Day1_002\Alin_Day1_002.rgb'
# image = np.fromfile(file_name, dtype ='uint8')

#@guvectorize([void(uint32, uint32, uint32, uint32, uint8[:,:])], '()->(m,n)')
#@jit
# def readImagePlane(row,col,level,offset):
#     global image

#     final = np.zeros(shape = (row,col), dtype = np.uint8)

#     i = 0

#     for m in range(row):
#         for n in range(col):
#             final[m,n] = image[level*row*col*3 + i + offset]
#             i = i + 1

#     return final

def main():

    #####################3Audio##############333
    # length of data to read.
    chunk = 1600

    # open the file for reading.
    wf = wave.open('C:\Users\Nikhil\Desktop\Nikhil\USCEE\Spring_2016\CSCI 576\Project\Alin_Day1_002\Alin_Day1_002.wav', 'rb')

    # create an audio object
    p = pyaudio.PyAudio()

    # open stream based on the wave object which has been input.
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    # read data (based on the chunk size)
    #data = wf.readframes(chunk)

    # play stream (looping from beginning of file to the end)

    ######################Video################
    frames, col, row = 13500, 480, 270

    # print("Starting the code")

    # #file_name = 'C:\Users\Nikhil\Desktop\Nikhil\USCEE\Spring_2016\CSCI 576\Project\Alin_Day1_002\Alin_Day1_002.rgb'

    file_name = 'C:\Users\Nikhil\Desktop\Nikhil\USCEE\Spring_2016\CSCI 576\Project\Alin_Day1_002\Alin_Day1_002.rgb'

    image = np.fromfile(file_name, dtype ='uint8')
    print image.shape
    #print("The number of frames is> " + str(number_of_frames))
    image= np.reshape(image,(13500,270,480))

    # # make a 3D array of a video

    # global image

    # #image = np.fromfile(file_name, dtype ='uint8')

    # print('File has been read')

    # # Reading all the channels
    # Red_plane = np.zeros(shape=(frames,row,col),dtype = np.uint8)
    # Green_plane = np.zeros(shape=(frames,row,col),dtype = np.uint8)
    # Blue_plane = np.zeros(shape=(frames,row,col),dtype = np.uint8)

    # multiplier = row*col*3

    # Intermediate_image = np.zeros(shape=(row,col,3),dtype = np.uint8)

    # print('Starting the reading process')

    # cv2.startWindowThread()

    # #for k in range(frames):
    # #    i = 0
    # #    for m in range(row):
    # #            for n in range(col):
    # #                    Red_plane[k][m][n] = image[k*multiplier + i]
    # #                    Green_plane[k][m][n] = image[k*multiplier + i+row*col]
    # #                    Blue_plane[k][m][n] = image[k*multiplier + i+2*row*col]
    # #                    i =i+1
    # #    print k
    # #print('Starting the displaying process')

    # final = np.zeros(shape = (row,col), dtype = np.uint8)

    # for k in range(frames):
       
    #     Red_plane[k,:,:] = readImagePlane(row,col,k,0)
    #     Green_plane[k,:,:] = readImagePlane(row,col,k,row*col)
    #     Blue_plane[k,:,:] = readImagePlane(row,col,k,2*row*col)
        
    #     print k

    Display_image = np.zeros(shape = (row,col,3), dtype = np.uint8)

    cv2.namedWindow('Video', cv2.WINDOW_AUTOSIZE)

    #avg = 0
    flag = 0

    wf.setpos(0)
    data = wf.readframes(chunk)

    i = 0

    while(i < frames):
        #start = time.time()
        Display_image = np.dstack((image[i+2][:][:],image[i+1][:][:],image[i][:][:]))
        #now = time.time() - start
        #avg = avg + now
        cv2.imshow('Video', Display_image)
        stream.write(data)
        data = wf.readframes(chunk)

        #time.sleep(0.060800)
        q = cv2.waitKey(1)
    
        if (q == ord('s')):
            break
        elif(q == ord('p')):
            while(cv2.waitKey(1) != ord('p')):

                if (cv2.waitKey(1) == ord('s')):
                    flag = 1
                    break
                else:
                    pass
        elif(q == ord('r')):
            while(cv2.waitKey(1) != ord('r')):
                i -= 3
                Display_image = np.dstack((image[i+2][:][:],image[i+1][:][:],image[i][:][:]))
                cv2.imshow('Video', Display_image)
            wf.setpos(chunk*(i/3))
        elif(q == ord('f')):
            while(cv2.waitKey(1) != ord('f')):
                i += 3
                Display_image = np.dstack((image[i+2][:][:],image[i+1][:][:],image[i][:][:]))
                cv2.imshow('Video', Display_image)
            wf.setpos(chunk*(i/3))
        else:
            pass

        if(flag == 1):
            break

        i += 3

    #avg = avg/15

    #print("The time is ",str(avg))


    # cleanup stuff.
    stream.close()    
    p.terminate()   
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    sys.exit(int(main() or 0))