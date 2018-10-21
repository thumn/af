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
                vertices.append([col, row, 0])
        for i in range(31): # row
            for k in range(31): # offset
                faces.append([i * 32 + k, i * 32 + k + 1, (i + 1) * 32 + k])
                faces.append([i * 32 + k + 1, (i + 1) * 32 + k + 1, (i + 1) * 32 + k])
        vertices = np.array(vertices)
        faces = np.array(faces)
        colors = []
        for i in range(341):
            colors.append([1, 0, 0, 0.5])
            colors.append([0, 1, 0, 0.5])
            colors.append([0, 0, 1, 0.5])
        colors.append([1, 0, 0, 0.5])
        colors = np.array(colors)
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
