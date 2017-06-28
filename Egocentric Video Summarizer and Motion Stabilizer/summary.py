import numpy as np
import sys
from math import *

import matplotlib.pyplot as plt


import cv2
import time
import pyaudio
import wave



def main():

    #####################3Audio##############333
    # length of data to read.
    chunk = 1600

    # open the file for reading.
    wf = wave.open('F:\Fall 2015\Course Material\Spring 2016\CSCI 576\Project\Alin_Day1_002\Alin_Day1_002.wav', 'rb')

    # create an audio object
    p = pyaudio.PyAudio()

    # open stream based on the wave object which has been input.
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    # read data (based on the chunk size)
    data = wf.readframes(chunk)

    # play stream (looping from beginning of file to the end)

    ######################Video################
    frames, col, row = 13500, 480, 270

    # print("Starting the code")

    # #file_name = 'C:\Users\Nikhil\Desktop\Nikhil\USCEE\Spring_2016\CSCI 576\Project\Alin_Day1_002\Alin_Day1_002.rgb'

    file_name = 'F:\Fall 2015\Course Material\Spring 2016\CSCI 576\Project\Alin_Day1_002\Alin_Day1_002.rgb'
    file_name1 = 'F:\Fall 2015\Course Material\Spring 2016\CSCI 576\Project\Alin_Day1_002\Xyz.rgb'
    image = np.fromfile(file_name, dtype ='uint8')
    testimage=np.fromfile(file_name1, dtype ='uint8')
    #print testimage.shape
    #print("The number of frames is> " + str(number_of_frames))
    image= np.reshape(image,(13500,270,480))
    testimage1=np.reshape(testimage,(3,720,1280))

    stack = np.dstack((testimage1[2][:][:],testimage1[1][:][:],testimage1[0][:][:]))

    testimage = cv2.resize(stack, (col,row))

 

    Display_image = np.zeros(shape = (row,col,3), dtype = np.uint8)

    #cv2.namedWindow('Video', cv2.WINDOW_AUTOSIZE)

    frame1 = np.zeros(shape = (row,col,3), dtype = np.uint8)
    frame2 = np.zeros(shape = (row,col,3), dtype = np.uint8)


    
    final_entropy = np.zeros(shape = (4500,1), dtype = np.float64)
    flag = 0
    tot_sum=row*col
    #test_frame=np.dstack((testimage[2][:][:],testimage[1][:][:],testimage[0][:][:]))
    for i in range(0,frames,3):
        frame1=np.dstack((image[i+2][:][:],image[i+1][:][:],image[i][:][:]))
        frame1gray = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
        # frame2=np.dstack((image[i+5][:][:],image[i+4][:][:],image[i+3][:][:]))
        # frame2gray = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

        framediff = cv2.absdiff(testimage,frame1)
        hist = cv2.calcHist([framediff],[0],None,[256],[0,256])
        probs = hist/tot_sum
        #print probs.shape
        sum_entropy = 0

        for j in range(255):
            if probs[j]==0:
                pass
            else:
                sum_entropy = sum_entropy + probs[j]*log(probs[j],2)

        final_entropy[i/3] = abs(sum_entropy)

    
    #print final_entropy.shape
    #new_entropy=np.zeros(shape = (4498,1), dtype = np.float64)
    #for i in range(4498):
    #    new_entropy[i] = abs(final_entropy[i+1]-final_entropy[i]) 

    #plt.stem(tot_frames[2:4500:2],new_entropy[0:4497:2]/max(final_entropy))
    #plt.hold('True')
    # plt.plot(final_entropy/max(final_entropy))

    # plt.show()
    section = np.zeros(shape=(900,270,480), dtype=np.uint8)
    index = np.argmin(final_entropy)
    if index < 150 or index > 4349:
        pass
    else:
        section = image[((index-150)*3):((index+150)*3)][:][:]

    cv2.namedWindow('Video', cv2.WINDOW_AUTOSIZE)

    

    for i in range(0,900,3):
        #start = time.time()
        Display_image = np.dstack((section[i+2][:][:],section[i+1][:][:],section[i][:][:]))
        #now = time.time() - start
        #avg = avg + now
        cv2.imshow('Video', Display_image)
        time.sleep(0.06)

        #time.sleep(0.060800)
        q = cv2.waitKey(1)
    
        if (q == ord('s')):
            break;
        elif(q == ord('p')):
            while(cv2.waitKey(1) != ord('p')):

                if (cv2.waitKey(1) == ord('s')):
                    flag = 1
                    break
                else:
                    pass
        else:
            pass

        if(flag == 1):
            break




if __name__ == "__main__":
    sys.exit(int(main() or 0))
