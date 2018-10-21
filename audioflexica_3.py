import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import sys

class Mesh:


    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.view = gl.GLViewWidget()
        self.view.show()

        #creates a 32x32 grid
        verts = []
        for row in range(32):
            for col in range(32):
                verts.append([col, row, 0])

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
            colors.append([1, 0, 0, 1])
            colors.append([0, 1, 0, 1])
            colors.append([0, 0, 1, 1])
        colors.append([1, 0, 0, 1])

        colors = np.array(colors)
        self.mesh = gl.GLMeshItem(vertexes = verts, faces = faces, faceColors = colors)
        self.mesh.setGLOptions("additive")
        self.view.addItem(self.mesh)
        self.view.setWindowTitle('Mesh')

    def run(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

if __name__ == '__main__':
    meesh = Mesh()
    meesh.run()
