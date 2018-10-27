import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
from opensimplex import OpenSimplex
import pyqtgraph.opengl as gl
import sys
import pyaudio
import struct


class Mesh:


    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.view = gl.GLViewWidget()
        self.view.show()
        self.noise = OpenSimplex()
        self.offSet = 0
        self.RATE = 44100
        self.CHUNK = 1024
        self.audioData = None
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
                                  format = pyaudio.paInt16,
                                  channels = 1, rate = self.RATE,
                                  input = True, output = True,
                                  frames_per_buffer = self.CHUNK
                                  )


        #creates a 32x32 grid
        verts = []
        for row in range(32):
            for col in range(32):
                verts.append([row, col, 0])

        #assigns triangular faces
        faces = []
        for i in range(31): #row
            for j in range(31): #column
                faces.append([
                i * 32 + j, #first point of triangle
                i * 32 + j + 1, #point to right of the first
                (i + 1) * 32 + j #point directly below the first
                ])
                faces.append([
                (i + 1) * 32 + j, #first point of second triangle (same as last point of first)
                (i + 1) * 32 + j + 1, #point to the right of the first
                i * 32 + j + 1 #point at the top of the second triangle (same as 2nd position of first)
                ])

        verts = np.array(verts)
        faces = np.array(faces)

        colors = []
        for i in range(1024):
            colors.append([1, 0, 0, 1])
            colors.append([0, 1, 0, 1])
            colors.append([0, 0, 1, 1])

        colors = np.array(colors)
        self.mesh = gl.GLMeshItem(vertexes = verts, faces = faces, vertexColors = colors)
        self.mesh.setGLOptions("additive")
        self.view.addItem(self.mesh)
        self.view.setWindowTitle('Mesh')



    def run(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def update(self):
        self.audioData = self.stream.read(self.CHUNK, exception_on_overflow = False)
        self.audioData = struct.unpack(str(2 * self.CHUNK) + 'B', self.audioData)
        self.audioData = np.array(self.audioData, dtype = 'b')[::2] + 128
        self.audioData = np.array(self.audioData, dtype = 'int32') - 128
        self.audioData = self.audioData * 0.04
        self.audioData = self.audioData.reshape(32, 32)

        verts = []
        for row in range(32):
            for col in range(32):
                verts.append([row, col,
                 #self.audioData[row][col] *
                  self.noise.noise2d(x= row + self.offSet, y= col + self.offSet)])

        faces = []
        for i in range(31): #row
            for j in range(31): #column
                faces.append([
                i * 32 + j, #first point of triangle
                i * 32 + j + 1, #point to right of the first
                (i + 1) * 32 + j #point directly below the first
                ])
                faces.append([
                (i + 1) * 32 + j, #first point of second triangle (same as last point of first)
                (i + 1) * 32 + j + 1, #point to the right of the first
                i * 32 + j + 1 #point at the top of the second triangle (same as 2nd position of first)
                ])
        verts = np.array(verts)
        faces = np.array(faces)
        colors = []
        for i in range(1024):
            colors.append([1, 0, 0, 1])
            colors.append([0, 1, 0, 1])
            colors.append([0, 0, 1, 1])

        colors = np.array(colors)

        self.mesh.setMeshData(vertexes = verts, faces = faces, vertexColors = colors, drawEdges = True)
        self.offSet -= 0.01

        print(self.audioData)



    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(10)
        self.run()
        self.update()



if __name__ == '__main__':
    meesh = Mesh()
    meesh.animation()
