# This is a sound library that contains functions to alleviate the processing of 3D/Natural Sound rendering

import numpy as np
from math import *
import scipy.io as sio
import scipy.io.wavfile
from astropy.convolution import convolve
import scipy.signal as sig


# Returns the Amplitude of a percieved sound source parameterized by its location in space in Polar co-ordinates
# Model for Inter Aural Level Difference (ILD)
def ILD(theta, phi):
	
	amplitude = np.array([((1 - 0.5*sin(theta))*cos(phi)), ((1 + 0.5*sin(theta))*cos(phi))])

	return amplitude

# Returns a stereo sample that is mutated for sound localization
# Model for Inter Aural Time Difference (ITD)
def ITD(distanceBetweenEars, theta, phi, previousSample, currentSample, samplingFrequency, sampleSize):

	# Assuming the speed of sound as 340 m/s

	# if (theta > 2*pi):
	# 	while (theta > 2*pi):
	# 		theta -= 2*pi

	# if ((phi > pi/2) & ()):

	deltaTheta = (distanceBetweenEars*sin(theta))/340
	deltaPhi = (distanceBetweenEars*cos(phi))/340

	bigDelta = sqrt(pow(deltaTheta,2) + pow(deltaPhi,2))

	noOfSamplesToShift = abs(bigDelta*samplingFrequency)

	if ((theta >= 0) & (theta < pi/2)):

		currentSample[noOfSamplesToShift:,1] = currentSample[0:(sampleSize - noOfSamplesToShift+1),1]
		currentSample[0:noOfSamplesToShift,1] = previousSample[(sampleSize - noOfSamplesToShift+1) : sampleSize,1]

	elif ((theta > -pi/2) & (theta < 0)):
		currentSample[noOfSamplesToShift:,0] = currentSample[0:(sampleSize - noOfSamplesToShift+1),0]
		currentSample[0:noOfSamplesToShift,0] = previousSample[(sampleSize - noOfSamplesToShift+1) : sampleSize,0]

	# elif ((theta == 0) | (theta == pi)):
	# 	pass

	# currentSample[:,0] = currentSample[:,0]*(ILD(theta, phi)[0])
	# currentSample[:,1] = currentSample[:,1]*(ILD(theta, phi)[1])

	return currentSample#/np.max(currentSample)

# Returns a stereo sample that is mutated by the sound Crosstalk in the real world
# Model for Crosstalk

def CrossTalk(stereo, alpha, theta, phi):

        # Should go with ITD for low freq and ILD for Med-High freq. Test!
	stereo[:,0] = stereo[:,0]*ILD(theta, phi)[0] + alpha*stereo[:,1]*ILD(theta, phi)[0]
	stereo[:,1] = stereo[:,1]*ILD(theta, phi)[1] + alpha*stereo[:,0]*ILD(theta, phi)[1]

	return stereo/(1+alpha)

# Returns a stereo sample that is mutated by the RIR in the real world
# Model for Room Impulse Response (Reverb)

rate, reverb = sio.wavfile.read('/home/nikhil/Desktop/Nikhil/EE_522_Project/Natural Sound Processing/Python Code/reverb.wav')

def RIR(stereo):
	stereo[:,0] = np.convolve(stereo[:,0], reverb[:,0], 'same') # Right Channel
	stereo[:,1] = np.convolve(stereo[:,1], reverb[:,1], 'same') # Left Channel

	return stereo/65536


# Returns a stereo sample that is mutated by the CIPIC HRTF database for sound localization

azAngles = np.array([-80, -65, -55, -45, -40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 55, 65, 80])
elAngles = np.round(-45 + 5.625*np.arange(50))
HRTF = sio.loadmat('/home/nikhil/Desktop/Nikhil/EE_522_Project/CIPIC/completedata.mat')
HRTF = HRTF['completedata']

# HRTF = HRTF

# newHRTF = np.zeros(shape = (2,25,HRTF.shape[2], HRTF.shape[3] + 1), dtype = np.float16)

# newHRTF[:,:,:,1:] = HRTF

def CIPIC_HRTF(stereo, theta, phi):

	# return the indexes of theta and phi values which correspond to the CIPIC HRTF indexes

	az = 0
	el = 0

	for i in range(len(azAngles)-1):
		if (azAngles[i] <= theta < azAngles[i+1]):
			if (theta < ((azAngles[i] + azAngles[i+1])/2)):
				az = i
				break
			elif (theta > ((azAngles[i] + azAngles[i+1])/2)):
				az = i+1
				break 

	for j in range(len(elAngles)-1):
		if (elAngles[j] <= phi < elAngles[j+1]):
			if (phi < ((elAngles[j] + elAngles[j+1])/2)):
				el = j
				break
			elif (phi > ((elAngles[j] + elAngles[j+1])/2)):
				el = j+1
				break

	# print [az,el]

	# Use these angles to retireve the HRTFs from the database and convolve with signal

	[stereo_row, stereo_col] = stereo.shape

	stereo[:,0] = np.convolve(stereo[:,0], HRTF[0,az,el,:], 'full') # Right Channel
	stereo[:,1] = np.convolve(stereo[:,1], HRTF[1,az,el,:], 'full') # Left Channel

	next_overlap = stereo[stereo_row:,stereo_col]
	stereo = stereo[0:stereo_row,stereo_col]

	# stereo[:,0] = convolve(stereo[:,0], newHRTF[1,az,el,:], boundary = 'extend', normalize_kernel = True) # Right Channel
	# stereo[:,1] = convolve(stereo[:,1], newHRTF[0,az,el,:], boundary = 'extend', normalize_kernel = True) # Left Channel

	# stereo[:,0] = np.fft.ifft(np.fft.fft(stereo[:,0])*np.fft.fft(HRTF[0,az,el,:]))
	# stereo[:,1] = np.fft.ifft(np.fft.fft(stereo[:,1])*np.fft.fft(HRTF[1,az,el,:]))

	# print np.max(HRTF[0,23,16,:])
	#print stereo[:,0].shape

	return stereo, next_overlap

########################################################################################################################

# Space for IMU functions


