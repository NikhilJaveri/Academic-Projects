#import pyaudio
#import wave
#import time

## length of data to read.
#chunk = 1600

## open the file for reading.
#wf = wave.open('C:\Users\Nikhil\Desktop\Nikhil\USCEE\Spring_2016\CSCI 576\Project\Alin_Day1_002\Alin_Day1_002.wav', 'rb')

## create an audio object
#p = pyaudio.PyAudio()

## open stream based on the wave object which has been input.
#stream = p.open(format =
#                p.get_format_from_width(wf.getsampwidth()),
#                channels = wf.getnchannels(),
#                rate = wf.getframerate(),
#                output = True)

## read data (based on the chunk size)
#data = wf.readframes(chunk)

## play stream (looping from beginning of file to the end)
#while data != '':
#    start = time.time()
#    # writing to the stream is what *actually* plays the sound.
#    stream.write(data)
#    data = wf.readframes(chunk)
#    print(time.time()-start)

## cleanup stuff.
#stream.close()    
#p.terminate()
