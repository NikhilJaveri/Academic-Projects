# Create a data structure to hold the CIPIC HRIR/HRTF database readings for a single person so it can be modelled and used int eh real time virtual soundscaping project.

import numpy as np
import scipy.io as sio
import scipy.io.wavfile
import wave

folderpath = '/home/nikhil/Desktop/Nikhil/EE_522_Project/CIPIC/wav_database/subject33/'

rate, reverb = sio.wavfile.read('/home/nikhil/Desktop/Nikhil/EE_522_Project/Natural Sound Processing/Python Code/reverb.wav')



k = 0

completeright = np.zeros(shape = (25, 50, 200), dtype = np.float)
completeleft = np.zeros(shape = (25, 50, 200), dtype = np.float)

for i in range(-80,85,5):

	if ((abs(i) == 50) or (abs(i) == 60) or (abs(i) == 70) or (abs(i) == 75)):
		continue;

	if (i < 0):
		pathstringleft = folderpath + 'neg' + str(abs(i)) + 'azleft.wav'
		pathstringright = folderpath + 'neg' + str(abs(i)) + 'azright.wav'

		rate, dataleft = sio.wavfile.read(pathstringleft)
		rate, dataright = sio.wavfile.read(pathstringright)

		# print dataleft

		completeright[k,:,:] = dataright
		completeleft[k,:,:] = dataleft

		# for j in range(50):

		# 	completeright[k,j,:] = np.convolve(dataright[j,:], reverb[:,0], 'same')
		# 	completeleft[k,j,:] = np.convolve(dataleft[j,:], reverb[:,1], 'same')


	elif (i >= 0):
		pathstringright = folderpath + str(i) + 'azright.wav'
		pathstringleft = folderpath + str(i) + 'azleft.wav'

		rate, dataleft = sio.wavfile.read(pathstringleft)
		rate, dataright = sio.wavfile.read(pathstringright)

		completeright[k,:,:] = dataright
		completeleft[k,:,:] = dataleft

		# for j in range(50):

		# 	completeright[k,j,:] = np.convolve(dataright[j,:], reverb[:,0], 'same')
		# 	completeleft[k,j,:] = np.convolve(dataleft[j,:], reverb[:,1], 'same')

	k = k+1

	print pathstringright + "---" + str(k)

# print wfright.getsampwidth()
# print wfright.getnchannels()

completedata = np.array([completeleft, completeright])

sio.savemat('completedata.mat', {'completedata':completedata})