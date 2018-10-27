import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import sys
from opensimplex import OpenSimplex
import pyaudio # this is how we'll receive data from our mics!
import struct # this is how we'll unpack the data and use it on our visualizer

class Mesh:
    def __init__(self): # pass in self, and the app & view attributes
        self.app = QtGui.QApplication(sys.argv) # the window titl this be the GUI for our project, allowing us to see all of the visuals
        self.view = gl.GLViewWidget() # this is going to be the view widget that we need to be able to add meshes
        self.view.show() # shows the view widget
        self.view.setWindowTitle('Mesh') #sets the window title to whatever we want
        self.noise = OpenSimplex()
        self.offSet = 0 # change the noise value as we loop through the animation
        self.RATE = 44100 # standard refresh rate for videos
        self.CHUNK = 1024 # standard chunk size for data; this is why our grid is 32 x 32
        self.audioData = None # this will keep track of the audio data we read
        self.p = pyaudio.PyAudio() # instance of a pyaudio class
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True, output=True, frames_per_buffer=self.CHUNK) # this is how we read audio data

        vertices = [] # vertices is an np array of [x, y, z] coordinates
        for row in range(32): # row corresponds to the y value
            for col in range(32): # col corresponds to the x value
                vertices.append([col, row, self.noise.noise2d(x= row, y=col)]) # add noise to the z coord to create a random terrain

        faces = [] # faces is an np array of [vertex1, vertex2, vertex3] using indices from the vertices np array
        for n in range(31): # row
            for k in range(31): # column
                # first point of FIRST triangle; to the right of the first; directly below the first
                faces.append([n * 32 + k, n * 32 + k + 1, (n + 1) * 32 + k ])
                # first point of SECOND triangle (same as last point of first triangle); to the right of the first; at the top (same as second position of first triangle)
                faces.append([(n + 1) * 32 + k, (n + 1) * 32 + k + 1, n * 32 + k + 1])

        colors = []
        for i in range(341): #ratio between 0 to 1 ...divide by length of row
            colors.append([1, 0, 0, 0.6])
            colors.append([0, 1, 0, 0.6])
            colors.append([0, 0, 1, 0.6])
        colors.append([1, 0, 0, 0.6])

        v = np.array(vertices)
        f = np.array(faces)
        c = np.array(colors)

        self.mesh = gl.GLMeshItem(vertexes=v, faces=f, faceColors=c)
        self.mesh.setGLOptions("additive")
        self.view.addItem(self.mesh)
        self.view.setWindowTitle('me$h')

    def update(self):
        self.audioData = self.stream.read(self.CHUNK, exception_on_overflow = False) # this reads incoming audiodata self.CHUNK bytes at a time
        # important to set exception_on_overflow in line above to False in order to prevent program from crashing
        audio_obj = struct.unpack(str(2 * self.CHUNK) + 'B', self.audioData)
        audio_obj = np.array(audio_obj, dtype = 'b')[::2] + 128
        audio_obj = np.array(audio_obj, dtype = 'int32') - 128
        audio_obj = audio_obj * 0.04
        audio_obj = audio_obj.reshape(32, 32)


        vertices = [] # vertices is an np array of [x, y, z] coordinates
        for row in range(32): # row corresponds to the y value
            for col in range(32): # col corresponds to the x value
                vertices.append([col, row, audio_obj[row][col] * self.noise.noise2d(x= row + self.offSet, y=col + self.offSet)])

        self.offSet -= 0.1 # each time the update function gets called, self.offSet decrements by 0.1

        faces = [] # faces is an np array of [vertex1, vertex2, vertex3] using indices from the vertices np array
        for n in range(31): # row
            for k in range(31): # column
        # first point of FIRST triangle; to the right of the first; directly below the first
                faces.append([n * 32 + k, n * 32 + k + 1, (n + 1) * 32 + k ])
        # first point of SECOND triangle (same as last point of first triangle); to the right of the first; at the top (same as second position of first triangle)
                faces.append([(n + 1) * 32 + k, (n + 1) * 32 + k + 1, n * 32 + k + 1])

        colors = []
        for i in range(341): #ratio between 0 to 1 ...divide by length of row
            colors.append([1, 0, 0, 0.6])
            colors.append([0, 1, 0, 0.6])
            colors.append([0, 0, 1, 0.6])
        colors.append([1, 0, 0, 0.6])

        v = np.array(vertices)
        f = np.array(faces)
        c = np.array(colors)

        self.mesh.setMeshData(vertexes=v, faces=f, vertexColors=c, drawEdges=True)

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(10)
        self.run() # call the start function to kick off animation
        self.update() # call the update function to kick off animation

    def run(self): # this function actually executes our Mesh instance and enables the GUI to run!
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

if __name__ == '__main__': # checks to see the Main function
 object = Mesh() # creates instance of your Mesh class by putting it on an object
 object.animation() # object actually runs when calling run function
