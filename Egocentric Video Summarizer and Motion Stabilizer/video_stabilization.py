import numpy as np
import cv2
from math import *
import time
import sys
import matplotlib.pyplot as plt
import pyaudio
import wave

def main():

    # Read the file and rehshape to form a video
    
    # length of data to read.
    chunk = int(wf.getframerate())/15

    # open the file for reading.
    wf = wave.open('C:\Users\Nikhil\Desktop\Nikhil\USCEE\Spring_2016\CSCI 576\Project\Alin_Day1_003\Alin_Day1_003.wav', 'rb')

    # create an audio object
    p = pyaudio.PyAudio()

    # open stream based on the wave object which has been input.
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
    
    sampling_freq = wf.getframerate()

    print(int(sampling_freq))

    # read data (based on the chunk size)
    #data = wf.readframes(chunk)

    # play stream (looping from beginning of file to the end)

    ######################Video################
    frames, col, row = 13500, 480, 270

    # print("Starting the code")

    # #file_name = 'C:\Users\Nikhil\Desktop\Nikhil\USCEE\Spring_2016\CSCI 576\Project\Alin_Day1_002\Alin_Day1_002.rgb'

    file_name = 'C:\Users\Nikhil\Desktop\Nikhil\USCEE\Spring_2016\CSCI 576\Project\Alin_Day1_003\Alin_Day1_003.rgb'

    image = np.fromfile(file_name, dtype ='uint8')
    print image.shape
    #print("The number of frames is> " + str(number_of_frames))
    image= np.reshape(image,(frames,270,480))
    
    # Video Stabilization

    smoothing_radius = 500
    horizontal_border_crop = 20

    previous_frame = np.dstack((image[2][:][:],image[1][:][:],image[0][:][:]))

    previous_gray = cv2.cvtColor(previous_frame,cv2.COLOR_BGR2GRAY)

    # Parameters for lucas kanade optical flow

    feature_params = dict( maxCorners = 200, qualityLevel = 0.03, minDistance = 7, blockSize = 7 )

    lk_params = dict( winSize  = (15,15),maxLevel = 2,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    # previous_corners = cv2.goodFeaturesToTrack(previous_gray, 200, 0.01, 30)

    previous_to_current_transform = [[] for i in range(3)]

    for i in range(3,frames,3):

        current_frame = np.dstack((image[i+2][:][:],image[i+1][:][:],image[i][:][:]))

        current_gray = cv2.cvtColor(current_frame,cv2.COLOR_BGR2GRAY)

        # p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        previous_corners = cv2.goodFeaturesToTrack(previous_gray, 200, 0.1, 10)

        current_corners, status, err = cv2.calcOpticalFlowPyrLK(previous_gray, current_gray, previous_corners, None, **lk_params)

        #if (np.sum(status) > 0):
        #    previous_corners2 = previous_corners
        #    current_corners2 = current_corners

        current_corners2 = []
        previous_corners2 = []

        # Remove bad corners
        for k in range(len(status)):
            if(status[k]):
                previous_corners2.append(previous_corners[k])
                current_corners2.append(current_corners[k])
        
        current_corners2 = np.array(current_corners2)
        previous_corners2 = np.array(previous_corners2)

        if ((not current_corners2.tolist()) | (not previous_corners2.tolist())):
            current_corners2 = valid_current_corners
            previous_corners2 = valid_prev_corners

        valid_prev_corners = previous_corners2
        valid_current_corners = current_corners2

        #previous_corners = current_corners2.reshape(-1,1,2)

        # Translation and Rotation
        transform = cv2.estimateRigidTransform(previous_corners2, current_corners2, False)

        if (transform is None):
            transform = previous_transform
        
        previous_transform = transform

        dx = transform[0,2]
        dy = transform[1,2]
        da = atan(transform[1,0]/transform[0,0])

        previous_to_current_transform[0].append(dx)
        previous_to_current_transform[1].append(dy)
        previous_to_current_transform[2].append(da)

        previous_frame = current_frame
        previous_gray = current_gray

        # Print the optical flow params to keep track

        print("Frame: " + str(i/3) + " has optical flow: " + str(len(previous_corners2)))

    # Accumulate tranformations to get motion trajectory

    print("Accumulation starting")

    x, y, a = 0, 0, 0

    trajectory = [[] for i in range(3)]

    for i in range(len(previous_to_current_transform[0])):

        x += previous_to_current_transform[0][i]
        y += previous_to_current_transform[1][i]
        a += previous_to_current_transform[2][i]

        trajectory[0].append(x)
        trajectory[1].append(y)
        trajectory[2].append(a)

        # Print to keep track
        #print("Frame: " + str(i) + " x:  " + str(x) + " y: " + str(y) + " a: " + str(a))

    # Smooth out the transition

    smoothened_trajectory = [[] for i in range(3)]

    print("Smoothening starting")

    for i in range(len(previous_to_current_transform[0])):

        sum_x, sum_y, sum_a, count = 0.0, 0.0, 0.0, 0

        for j in range(-smoothing_radius, smoothing_radius + 1):
            if((i+j > 0) & (i+j < len(previous_to_current_transform[0]))):
                sum_x += trajectory[0][i+j]
                sum_y += trajectory[1][i+j]
                sum_a += trajectory[2][i+j]

                count += 1

        avg_x, avg_y, avg_a = (sum_x/count), (sum_y/count), (sum_a/count)

        smoothened_trajectory[0].append(avg_x)
        smoothened_trajectory[1].append(avg_y)
        smoothened_trajectory[2].append(avg_a)

        print("frame: " + str(i))

    # Generate new transform

    print("Transformation starting")

    new_transform = [[] for i in range(3)]

    x, y, a = 0.0, 0.0, 0.0

    for i in range(len(previous_to_current_transform[0])):

        x += previous_to_current_transform[0][i]
        y += previous_to_current_transform[1][i]
        a += previous_to_current_transform[2][i]

        # Get the difference between the target and the current

        diff_x = smoothened_trajectory[0][i] - x
        diff_y = smoothened_trajectory[1][i] - y
        diff_a = smoothened_trajectory[2][i] - a

        # Correct the shift

        dx = previous_to_current_transform[0][i] + diff_x
        dy = previous_to_current_transform[1][i] + diff_y
        da = previous_to_current_transform[2][i] +  diff_a

        # Save the shifts

        new_transform[0].append(dx)
        new_transform[1].append(dy)
        new_transform[2].append(da)
        

    # Plot the x values for debug

    original_a = np.array(trajectory[2])
    smooth_a = np.array(smoothened_trajectory[2])

    plt.plot(original_a)
    plt.hold('True')
    plt.plot(smooth_a)
    plt.show()

    # Apply the new tranform to the video

    print("Writing frames to buffer")

    vert_border = horizontal_border_crop * (row / col)

    T = np.zeros(shape = (2,3))

    final_video = np.zeros(shape = (frames, row, (col*2)), dtype = np.uint8)
    canvas = np.zeros(shape = (3,row, col*2), dtype = np.uint8);

    for i in range(0, frames - 3, 3):

        T[0,0] = cos(0.07*new_transform[2][i/3])
        T[0,1] = -sin(0.07*new_transform[2][i/3])
        T[1,0] = sin(0.07*new_transform[2][i/3])
        T[1,1] = cos(0.07*new_transform[2][i/3])

        T[0,2] = 0.1*new_transform[0][i/3]
        T[1,2] = 0.1*new_transform[1][i/3]

        old_frame = np.dstack((image[i+2][:][:],image[i+1][:][:],image[i][:][:]))

        if (i == 0):
            new_frame = old_frame

        new_frame = cv2.warpAffine(old_frame, T, (col, row), dst = new_frame, flags = cv2.INTER_LANCZOS4 | cv2.WARP_INVERSE_MAP)

        # Now draw the original and stablised side by side for coolness

        Display_image = np.dstack((image[i+2][:][:],image[i+1][:][:],image[i][:][:]))

        # difference = cv2.absdiff(new_frame, Display_image)

        canvas[0,:,0:col] = Display_image[:,:,2]
        canvas[1,:,0:col] = Display_image[:,:,1]
        canvas[2,:,0:col] = Display_image[:,:,0]

        canvas[0,:,col:col*2] = np.uint8(new_frame[:,:,2])
        canvas[1,:,col:col*2] = np.uint8(new_frame[:,:,1])
        canvas[2,:,col:col*2] = np.uint8(new_frame[:,:,0])

        #canvas[0,:,col*2:col*3] = np.uint8(difference[:,:,2])
        #canvas[1,:,col*2:col*3] = np.uint8(difference[:,:,1])
        #canvas[2,:,col*2:col*3] = np.uint8(difference[:,:,0])

        # new_frame = new_frame[vert_border:new_frame.shape[0] - vert_border+1, horizontal_border_crop: new_frame.shape[1] - horizontal_border_crop+1,:]

        # Write frames into buffer final_video

        final_video[i,:,:] = canvas[0,:,:]
        final_video[i+1,:,:] = canvas[1,:,:]
        final_video[i+2,:,:] = canvas[2,:,:]

        #for x in range(row):
        #    for y in range(col):
        #        final_video[i,x,y] = new_frame[x,y,0]
        #        final_video[i+1,x,y] = new_frame[x,y,1]
        #        final_video[i+2,x,y] = new_frame[x,y,2]

        print(i/3)

    # Play the stabilized video along with the original video for reference

    cv2.namedWindow('Original Video --- Stabilized Video', cv2.WINDOW_AUTOSIZE)
    #cv2.namedWindow('Stabilized Video', cv2.WINDOW_AUTOSIZE)
    # cv2.namedWindow('Difference Video', cv2.WINDOW_AUTOSIZE)

    wf.setpos(0)
    data = wf.readframes(chunk)

    i = 0

    flag = 0

    print("Gona show now")

    while(i < frames):

        Display_image = np.dstack((final_video[i+2][:][:],final_video[i+1][:][:],final_video[i][:][:]))
        #Stabilized_image = np.dstack((final_video[i+2][:][:],final_video[i+1][:][:],final_video[i][:][:]))
       #  difference = cv2.absdiff(Stabilized_image, Display_image)

        cv2.imshow('Original Video --- Stabilized Video', Display_image)
        #cv2.imshow('Stabilized Video', Stabilized_image)
        # cv2.imshow('Difference Video', difference)

        stream.write(data)
        data = wf.readframes(chunk)

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
                Display_image = np.dstack((final_video[i+2][:][:],final_video[i+1][:][:],final_video[i][:][:]))
                # Stabilized_image = np.dstack((final_video[i+2][:][:],final_video[i+1][:][:],final_video[i][:][:]))
                # difference = cv2.absdiff(Stabilized_image, Display_image)
                cv2.imshow('Original Video --- Stabilized Video', Display_image)
                # cv2.imshow('Stabilized Video', Stabilized_image)
                # cv2.imshow('Difference Video', difference)
            wf.setpos(chunk*(i/3))
        elif(q == ord('f')):
            while(cv2.waitKey(1) != ord('f')):
                i += 3
                Display_image = np.dstack((final_video[i+2][:][:],final_video[i+1][:][:],final_video[i][:][:]))
                # Stabilized_image = np.dstack((final_video[i+2][:][:],final_video[i+1][:][:],final_video[i][:][:]))
                # difference = cv2.absdiff(Stabilized_image, Display_image)
                cv2.imshow('Original Video --- Stabilized Video', Display_image)
                # cv2.imshow('Stabilized Video', Stabilized_image)
                # cv2.imshow('Difference Video', difference)
            wf.setpos(chunk*(i/3))
        else:
            pass

        if(flag == 1):
            break

        i += 3

    cv2.destroyAllWindows()

if __name__ == "__main__":
    sys.exit(int(main() or 0))