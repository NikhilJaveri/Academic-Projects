# Finding corners

import numpy as np
import cv2
from math import *
import time
import sys

import pyaudio
import wave

def main():

    # Read the file and rehshape to form a video
    
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
    image= np.reshape(image,(frames,270,480))

    # Track corners

    # params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 100,
                           qualityLevel = 0.3,
                           minDistance = 7,
                           blockSize = 7 )

    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                      maxLevel = 2,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    # Create some random colors
    color = np.random.randint(0,255,(100,3))

    # Take first frame and find corners in it
    previous_frame = np.dstack((image[2][:][:],image[1][:][:],image[0][:][:]))

    previous_gray = cv2.cvtColor(previous_frame,cv2.COLOR_BGR2GRAY)

    p0 = cv2.goodFeaturesToTrack(previous_gray, mask = None, **feature_params)

    # Create a mask image for drawing purposes
    mask = np.zeros_like(previous_frame)

    cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE) 

    for i in range(3,frames,3):

        current_frame = np.dstack((image[i+2][:][:],image[i+1][:][:],image[i][:][:]))

        current_gray = cv2.cvtColor(current_frame,cv2.COLOR_BGR2GRAY)

        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(previous_gray, current_gray, p0, None, **lk_params)

        # Select good points
        good_new = p1
        good_old = p0

        # draw the tracks
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            #mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
            #current_frame = cv2.circle(current_frame,(a,b),5,color[i].tolist(),-1)

            cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
            cv2.circle(current_frame,(a,b),5,color[i].tolist(),-1)
        img = cv2.add(current_frame,mask)

        cv2.imshow('frame',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        # Now update the previous frame and previous points
        previous_gray = current_gray.copy()
        p0 = good_new.reshape(-1,1,2)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    sys.exit(int(main() or 0))