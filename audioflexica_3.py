import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import sys

class Mesh:


    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.view = gl.GLViewWidget()
        self.view.show()


        verts = np.array([
        [0, 0, 0],
        [2, 0, 0],
        [1, 2, 0],
        [1, 1, 1],
        ])





        faces = np.array([
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
        [1, 2, 3]
        ])
        colors = np.array([
        [.7, 0, 0, 1],
        [.2, .2, .5, 1]


        ])

        self.mesh = gl.GLMeshItem(vertexes = verts, faces = faces, faceColors = colors)
        self.mesh.setGLOptions("additive")
        self.view.addItem(self.mesh)
        self.view.setWindowTitle('Mesh')

    def run(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

if __name__ == '__main__':
    asdf = Mesh()
    asdf.run()
