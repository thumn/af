import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import sys

class Mesh:

    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.view = gl.GLViewWidget()
        self.view.show()
        vertices = []
        faces = []
        for row in range(32):
            for col in range(32):
                vertices.append([col, row])
        for i in range(32):
            for j in range(i+1, 32):
                for k in range(j+1, 32):
                    faces.append([i, j, k])
        vertices = np.array(vertices)
        faces = np.array(faces)
        colors = np.array([
            [1, 0, 0, 0.5],
            [0, 1, 0, 0.5],
            [0, 0, 1, 0.5]
        ])
        self.mesh = gl.GLMeshItem(vertexes=vertices, faces=faces, faceColors=colors)
        self.mesh.setGLOptions("additive")
        self.view.addItem(self.mesh)
        self.view.setWindowTitle('Meshy')

    def run(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
	           QtGui.QApplication.instance().exec_()

def generate_grid():
        vert = []
        for j in range(32):
            for i in range(32):
                v = [i/32, j/32, 0]
                vert.append(v)
        vert = np.array(vert)
        return vert

if __name__ == '__main__':
    m = Mesh()
    m.run()
