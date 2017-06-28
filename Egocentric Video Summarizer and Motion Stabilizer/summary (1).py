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
    # data = wf.readframes(chunk)
    

    # play stream (looping from beginning of file to the end)

    ######################Video################
    frames, col, row = 13500, 480, 270

    # print("Starting the code")

    # #file_name = 'C:\Users\Nikhil\Desktop\Nikhil\USCEE\Spring_2016\CSCI 576\Project\Alin_Day1_002\Alin_Day1_002.rgb'

    file_name = 'C:\Users\Nikhil\Desktop\Nikhil\USCEE\Spring_2016\CSCI 576\Project\Alin_Day1_002\Alin_Day1_002.rgb'
    # file_name1 = 'F:\Fall 2015\Course Material\Spring 2016\CSCI 576\Project\Alin_Day1_002\Xyz2.rgb'
    image = np.fromfile(file_name, dtype ='uint8')
    # testimage=np.fromfile(file_name1, dtype ='uint8')
    
    image= np.reshape(image,(13500,270,480))
    # testimage1=np.reshape(testimage,(3,720,1280))

    # stack = np.dstack((testimage1[2][:][:],testimage1[1][:][:],testimage1[0][:][:]))

    # testimage = cv2.resize(stack, (col,row))

 

    Display_image = np.zeros(shape = (row,col,3), dtype = np.uint8)

    

    frame1 = np.zeros(shape = (row,col,3), dtype = np.uint8)
    frame2 = np.zeros(shape = (row,col,3), dtype = np.uint8)


    
    final_entropy = np.zeros(shape = (4500,1), dtype = np.float64)
    cdf_final = np.zeros(shape = (4500,1), dtype = np.float64)
    flag = 0
    tot_sum=row*col
    #test_frame=np.dstack((testimage[2][:][:],testimage[1][:][:],testimage[0][:][:]))
    for i in range(0,frames-3,3):
        frame1=np.dstack((image[i+2][:][:],image[i+1][:][:],image[i][:][:]))
        frame1gray = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
        frame2=np.dstack((image[i+5][:][:],image[i+4][:][:],image[i+3][:][:]))
        frame2gray = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

        framediff = cv2.absdiff(frame2gray,frame1gray)
        hist = cv2.calcHist([framediff],[0],None,[256],[0,256])
        probs = hist/tot_sum
        
        sum_entropy = 0

        for j in range(255):
            if probs[j]==0:
                pass
            else:
                sum_entropy = sum_entropy + probs[j]*log(probs[j],2)

        final_entropy[i/3] = abs(sum_entropy)
    
    a=[]
    final_entropy= final_entropy/max(final_entropy)
    mean_full = np.mean(final_entropy)
    print np.mean(final_entropy)

    new_final_entropy = final_entropy-mean_full

    max_final_entropy = max(new_final_entropy)

    # Find Non Zero Sections

    x1 = 0
    x2 = 1
    
    segment_array_x1 = []
    segment_array_x2 = []

    i = 0

    while (i < 4500):

        if(new_final_entropy[i] > 0):
            x1 = i

            while(new_final_entropy[i] > 0):
                i = i + 1

            x2 = i
            
            segment_array_x1.append(x1)
            segment_array_x2.append(x2)

            x1 = x2
            x2 = x2 + 1

        else:

            i = i + 1

    #print(segment_array_x1)
    #print(segment_array_x2)

    #print(max(np.array(segment_array_x2) - np.array(segment_array_x1)))

    # Sort and find the section lengths according to priority

    x1_array = np.array(segment_array_x1)
    x2_array = np.array(segment_array_x2)

    segment_difference = x2_array - x1_array

    sorted_segments = np.argsort(segment_difference)

    # print(sorted_segments)

    max_index = max(sorted_segments)

    summary_length = 0

    summary_section_x1 = []
    summary_section_x2 = []

    i = 0

    while (summary_length < 150*15):

        index = sorted_segments[max_index - i]

        summary_section_x1.append(x1_array[index])
        summary_section_x2.append(x2_array[index])

        summary_length += sorted_segments[i]

        i += 1


    # Refine the structure of the summary by clubbing sub videos that are very close

    #for i in len(summary_section_x1):



    #print(summary_section_x1)
    #print(summary_section_x2)
    #print(np.array(summary_section_x2) - np.array(summary_section_x1))

    print("Summary Length: " + str(summary_length/15))

    index_to_play = np.argsort(summary_section_x1)

    vote = raw_input("Video is ready. Play?")

    i = 0

    start = time.time()
    while(i < len(summary_section_x1)):

        wf.setpos(chunk*summary_section_x1[index_to_play[i]])
        data = wf.readframes(chunk)

        for k in range(summary_section_x1[index_to_play[i]], summary_section_x2[index_to_play[i]]):
            Display_image = np.dstack((image[3*k+2][:][:],image[3*k+1][:][:],image[3*k][:][:]))
            cv2.imshow('Video', Display_image)
            
            stream.write(data)
            data = wf.readframes(chunk)

            time.sleep(0.014800)
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

        i += 1

    print("video length: " + str(time.time() - start))

    cv2.destroyAllWindows()
        
    #=======================================================================
    #print ind

    #new_final_entropy[new_final_entropy < 0] =0
    #ind=[]

    #k = 0
    #while (k < 4500):
    #    if ((new_final_entropy[k]==0) & (np.sum(new_final_entropy[k:k+10])==0)):
    #        #print new_final_entropy[i]
    #        ind.append(k)
    #        k=k+10
    #    else:
    #        #print new_final_entropy[i]
    #        pass
    #    k = k + 1

    #print ind
    #plt.plot(new_final_entropy)
    #plt.show()

    #for i in range(0,4499,50):
    #    mean_segment = np.mean(final_entropy[i:i+50])
    #    if mean_segment > mean_full:
    #        a.append(i)
    #    else:
    #        final_entropy[i:i+50]=0



    #plt.stem(final_entropy)
    #plt.show()
        
#==============================================================================
    #cdf_final[0]=final_entropy[0]
    #for i in range(1,4499):
    #    cdf_final[i]=final_entropy[i]+cdf_final[i-1]
#     
#==============================================================================
    # new_entropy=np.zeros(shape = (4498,1), dtype = np.float64)
    # for i in range(4498):
    #    new_entropy[i] = abs(final_entropy[i+1]-final_entropy[i]) 

    #plt.plot(cdf_final)
    #plt.show()
    # plt.hold('True')
    # plt.plot(final_entropy/max(final_entropy))

    #==============================================================================
    #x1 = 0
    #x2 = 1
 
    #segment_array_x1 = np.zeros(shape = (1,1), dtype = np.int)
    #segment_array_x2 = np.zeros(shape = (1,1), dtype = np.int)
 
    #some_threshold = 6
    #i = 0
    #while (i < 4500):
    #    current_slope = (cdf_final[x2] - cdf_final[x1])
 
    #    if (current_slope > some_threshold):
 
    #        # x1 = i
    #        # x2 = i+1
    #        new_slope = current_slope
 
    #        while (new_slope > some_threshold):

    #            x2 = x2 + 1
    #            x3 = x2 - 1
    #            new_slope = (cdf_final[x2] - cdf_final[x3])
 
    #            i = i + 1
 
    #            if (x2 > 4499):
    #                break
 
    #        np.append(segment_array_x1, x1)
    #        np.append(segment_array_x2, x2)
 
    #        print("Video is fast changing from " + str(x1) + " to " + str(x2))
 
    #        x1 = x2
    #        x2 = x2 + 1
 
    #    else:
    #        x1 = x1 + 1
    #        x2 = x2 + 1
    #        i = i + 1
 
    #    if (x2 > 4498):
    #        break
# 
#     previous_slope = (cdf_final[1] - cdf_final[0])/(x2-x1)
#     for i in range(1,4499):
#         current_slope = (cdf_final[i+1] - cdf_final[0])/(1+i)
#==============================================================================



    
#==============================================================================
#     section = np.zeros(shape=(900,270,480), dtype=np.uint8)
#     index = np.argmin(final_entropy)
#     mean = np.mean(final_entropy/max(final_entropy))
#     print mean
#     if index < 150 or index > 4349:
#         pass
#     else:
#         section = image[((index-150)*3):((index+150)*3)][:][:]
# 
#     cv2.namedWindow('Video', cv2.WINDOW_AUTOSIZE)
# 
#==============================================================================
    

#==============================================================================
#     for i in range(0,900,3):
#         #start = time.time()
#         Display_image = np.dstack((section[i+2][:][:],section[i+1][:][:],section[i][:][:]))
#         #now = time.time() - start
#         #avg = avg + now
#         cv2.imshow('Video', Display_image)
#         time.sleep(0.06)
# 
#         #time.sleep(0.060800)
#         q = cv2.waitKey(1)
#     
#         if (q == ord('s')):
#             break;
#         elif(q == ord('p')):
#             while(cv2.waitKey(1) != ord('p')):
# 
#                 if (cv2.waitKey(1) == ord('s')):
#                     flag = 1
#                     break
#                 else:
#                     pass
#         else:
#             pass
# 
#         if(flag == 1):
#             break
#==============================================================================




if __name__ == "__main__":
    sys.exit(int(main() or 0))
