from threading import Thread
import time
import math
import serial # import Serial Library
from Queue import Queue
import pyaudio
import wave
import numpy as np
from NSLib import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

# Common data shared between threads
qObject = Queue()
flag = Queue()

# Serial objects for IMU
ser = serial.Serial('/dev/ttyACM0', 38400, timeout=1)
ax = ay = az = 0.0
yaw_mode = False

def resize((width, height)):
    if height==0:
        height=1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def drawText(position, textString):     
    font = pygame.font.SysFont ("Courier", 18, True)
    textSurface = font.render(textString, True, (255,255,255,255), (0,0,0,255))     
    textData = pygame.image.tostring(textSurface, "RGBA", True)     
    glRasterPos3d(*position)     
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def draw():
    global rquad
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	
    
    glLoadIdentity()
    glTranslatef(0,0.0,-7.0)

    osd_text = "pitch: " + str("{0:.2f}".format(ay)) + ", roll: " + str("{0:.2f}".format(ax))

    if yaw_mode:
        osd_line = osd_text + ", yaw: " + str("{0:.2f}".format(az))
    else:
        osd_line = osd_text

    drawText((-2,-2, 2), osd_line)

    # the way I'm holding the IMU board, X and Y axis are switched 
    # with respect to the OpenGL coordinate system
    if yaw_mode:                             # experimental
        glRotatef(az, 0.0, 1.0, 0.0)  # Yaw,   rotate around y-axis
    else:
        glRotatef(0.0, 0.0, 1.0, 0.0)
    glRotatef(ay ,1.0,0.0,0.0)        # Pitch, rotate around x-axis
    glRotatef(-1*ax ,0.0,0.0,1.0)     # Roll,  rotate around z-axis

    glBegin(GL_QUADS)	
    glColor3f(0.0,1.0,0.0)
    glVertex3f( 1.0, 0.2,-1.0)
    glVertex3f(-1.0, 0.2,-1.0)		
    glVertex3f(-1.0, 0.2, 1.0)		
    glVertex3f( 1.0, 0.2, 1.0)		

    glColor3f(1.0,0.5,0.0)	
    glVertex3f( 1.0,-0.2, 1.0)
    glVertex3f(-1.0,-0.2, 1.0)		
    glVertex3f(-1.0,-0.2,-1.0)		
    glVertex3f( 1.0,-0.2,-1.0)		

    glColor3f(1.0,0.0,0.0)		
    glVertex3f( 1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)		
    glVertex3f(-1.0,-0.2, 1.0)		
    glVertex3f( 1.0,-0.2, 1.0)		

    glColor3f(1.0,1.0,0.0)	
    glVertex3f( 1.0,-0.2,-1.0)
    glVertex3f(-1.0,-0.2,-1.0)
    glVertex3f(-1.0, 0.2,-1.0)		
    glVertex3f( 1.0, 0.2,-1.0)		

    glColor3f(0.0,0.0,1.0)	
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2,-1.0)		
    glVertex3f(-1.0,-0.2,-1.0)		
    glVertex3f(-1.0,-0.2, 1.0)		

    glColor3f(1.0,0.0,1.0)	
    glVertex3f( 1.0, 0.2,-1.0)
    glVertex3f( 1.0, 0.2, 1.0)
    glVertex3f( 1.0,-0.2, 1.0)		
    glVertex3f( 1.0,-0.2,-1.0)		
    glEnd()	
         
def read_data():
    global ax, ay, az
    ax = ay = az = 0.0
    line_done = 0

    # request data by sending a dot
    ser.write(".")
    #while not line_done:
    line = ser.readline() 
    angles = line.split(", ")
    if len(angles) == 3:    
        ax = float(angles[0])
        ay = float(angles[1])
        az = -float(angles[2])
        # line_done = 1
        if(az > 110):
            az = 80 - (az-110)
            ax = 180 + ax
        elif(az < -110):
            az = -80 + (-110 - az)
            ax = 180 + ax
        elif((az > 80) & (az < 110)):
            az = 79
            # ax = 0
        elif ((az > -110) & (az < -80)):
            az = -79
            # ax = 0

def sound():

	# length of data to read.
	chunk = 1600

	# open the file for reading.
	wf = wave.open('skyfall.wav', 'rb')

	# create an audio object
	p = pyaudio.PyAudio()

	# open stream based on the wave object which has been input.
	stream = p.open(format =
	               p.get_format_from_width(wf.getsampwidth()),
	               channels = wf.getnchannels(),
	               rate = wf.getframerate(),
	               output = True)


	normalizer = pow(2.0,15)

	# print "This is the chunk size: " + str(wf.getsampwidth())
	# read data (based on the chunk size)
	data = wf.readframes(chunk)

	data = np.fromstring(wf.readframes(chunk), np.int16)
	data = data.astype(np.float64)/normalizer
	previousStereo = np.reshape(data, (-1, wf.getnchannels()))

	ogsize = data.shape

	samplingFrequency = wf.getframerate()

	print "runtime: " + str(float(wf.getnframes())/samplingFrequency)
	# play stream (looping from beginning of file to the end)

	# theta = -80
	# phi = -45

	while ((len(data) > 0) or (not(flag.get()))):
	   # writing to the stream is what *actually* plays the sound.
	   stream.write(data)

	   data = np.fromstring(wf.readframes(chunk), np.int16)

	   data = data.astype(np.float64)/normalizer
	   # print np.max(data)

	   stereo = np.reshape(data, (-1, wf.getnchannels()))
	   # print stereo.dtype

	   # Get the data from the sensor
	   data = qObject.get()
	   # print "I can see data, they are: " + str(data)
	   qObject.task_done()

	   theta = data[2]
	   phi = data[0]#*math.cos(theta*np.pi/180) + data[1]*abs(math.sin(theta*np.pi/180))

	   stereo = ITD(0.215, theta*(np.pi/180), phi*(np.pi/180), previousStereo, stereo, samplingFrequency, chunk)

	   previousStereo = stereo

	   stereo = CrossTalk(stereo, 0.99, theta*(np.pi/180), phi*(np.pi/180))

	   stereo, next_overlap = CIPIC_HRTF(stereo/3, theta, phi)

	   stereo[0:(previous_overlap.shape)[0]+1,:] = stereo[0:(previous_overlap.shape)[0]+1,:] + previous_overlap

	   previous_overlap = next_overlap

	   # stereo = RIR(stereo)

	   # print np.max(stereo)

	   data = np.reshape(stereo, ogsize)

	   # print np.max(data)

	   # data = data*normalizer

	   data = (data.astype(np.int16)).tostring()

	   # data = wf.readframes(chunk)

	   # phi += 2
	   # theta += 2

	   # print theta

	# cleanup stuff.
	stream.close()    
	p.terminate()

def main():

	soundscape = Thread(target = sound)

	# passd.daemon = True

	soundscape.start()
	
	global yaw_mode

	video_flags = OPENGL|DOUBLEBUF

	pygame.init()
	screen = pygame.display.set_mode((640,480), video_flags)
	pygame.display.set_caption("Press Esc to quit, z toggles yaw mode")
	resize((640,480))
	init()
	frames = 0
	ticks = pygame.time.get_ticks()
	while 1:
	    event = pygame.event.poll()
	    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
	    	flag.put(True)
	        break       
	    if event.type == KEYDOWN and event.key == K_z:
	        yaw_mode = not yaw_mode
	        ser.write("z")
	    read_data()
	    draw()
	    # print az

	    qObject.put([ax,ay,az])
	    flag.put(False)
	    qObject.join()
	  
	    pygame.display.flip()
	    frames = frames+1

	print "fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks))
	ser.close()
	flag.put(True)


if __name__ == '__main__':
	main()

