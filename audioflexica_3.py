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
                verts.append([row, col,self.noise.noise2d(x= row, y=col)])

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
        for i in range(341):
            colors.append([1, 0, 0, 0.5])
            colors.append([0, 1, 0, 0.5])
            colors.append([0, 0, 1, 0.5])
            colors.append([1, 0, 0, 0.5])

        colors = np.array(colors)
        self.mesh = gl.GLMeshItem(vertexes = verts, faces = faces, vertexColors = colors)
        self.mesh.setGLOptions("additive")
        self.view.addItem(self.mesh)
        self.view.setWindowTitle('me$h')



    def update(self):
        self.audioData = self.stream.read(self.CHUNK, exception_on_overflow = False)
        a = struct.unpack(str(2 * self.CHUNK) + 'B', self.audioData)
        a = np.array(a, dtype = 'b')[::2] + 128
        a = np.array(a, dtype = 'int32') - 128
        a = a * 0.04
        a = a.reshape(32, 32)

        verts = []
        for row in range(32):
            for col in range(32):
                verts.append([row, col,
                 a[row][col] * self.noise.noise2d(x= row + self.offSet, y= col + self.offSet)])

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

        colors = []
        for i in range(341):
            colors.append([1, 0, 0, 0.5])
            colors.append([0, 1, 0, 0.5])
            colors.append([0, 0, 1, 0.5])
            colors.append([1, 0, 0, 0.5])

        verts = np.array(verts)
        faces = np.array(faces)
        colors = np.array(colors)

        self.mesh.setMeshData(vertexes = verts, faces = faces, faceColors = colors, drawEdges = True)
        self.offSet -= 0.01

        print(a)



    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(10)
        self.run()
        self.update()

    def run(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()



if __name__ == '__main__':
    meesh = Mesh()
    meesh.animation()
