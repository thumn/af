import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import sys

class Mesh:
    def __init__(self): # pass in self, and the app & view attributes
        self.app = QtGui.QApplication(sys.argv) # the window titl this be the GUI for our project, allowing us to see all of the visuals
        self.view = gl.GLViewWidget() # this is going to be the view widget that we need to be able to add meshes
        self.view.show() # shows the view widget
        self.view.setWindowTitle('Mesh') #sets the window title to whatever we want

        vertices = [] # vertices is an np array of [x, y, z] coordinates
        for row in range(32): # row corresponds to the y value
            for col in range(32): # col corresponds to the x value
                vertices.append([col, row, 0])

        faces = [] # faces is an np array of [vertex1, vertex2, vertex3] using indices from the vertices np array
        for n in range(31): # row
            for k in range(31): # column
# first point of FIRST triangle; to the right of the first; directly below the first
                faces.append([n * 32 + k, n * 32 + k + 1, (n + 1) * 32 + k ])
# first point of SECOND triangle (same as last point of first triangle); to the right of the first; at the top (same as second position of first triangle)
                faces.append([(n + 1) * 32 + k, (n + 1) * 32 + k + 1, n * 32 + k + 1])

        colors = []
        for i in range(341):
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


    def run(self): # this function actually executes our Mesh instance and enables the GUI to run!
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

if __name__ == '__main__': # checks to see the Main function
 object = Mesh() # creates instance of your Mesh class by putting it on an object
 object.run() # object actually runs when calling run function
