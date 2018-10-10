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


        # To make a 1024 grid, first create a 32 by 32 grid, and then create 10-24 faces
            # try using a nested for loop? first for loop for the horizontal rows/vertices & second for loop for the vertical rows/vertices
            # use an offset, everytime you move through it, you increase it (iteration / counter method)

            # use a nested for loop in terms of x & y coordinates
        vertices = []
        for row in range(32): # row corresponds to the y value
            for col in range(32): # col corresponds to the x value
                vertices.append((col, row))

        faces = []
            for n in range(32):
                for i in range(n+1, 32):
                    #for k in range(j+1, 32)
                    faces.append((n, i))

        v = np.array(vertices)
        f = np.array(faces)


        #v = np.array([
         #  [0, 0, 0],
          # [2, 0, 0],
           #[1, 2, 0],
           #[1, 1, 1],
        # ])

        #f = np.array([
         #  [0, 1, 2],
          # [0, 1, 3],
           #[0, 2, 3],
           #[1, 2, 3],
        #])

        c = np.array([
        [1,0,0,0.5],
        [0,1,0,0.5],
        [0,0,1,0.5]
        ])

        self.mesh = gl.GLMeshItem(vertexes=v, faces=f, faceColors=c)
        self.mesh.setGLOptions("additive")
        self.view.addItem(self.mesh)
        # vertexes is an np array of [x, y, z] coordinates
        # faces is an np array of [vertex1, vertex2, vertex3] using indices from the vertexes np array

    def run(self): # this function actually executes our Mesh instance and enables the GUI to run!
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

if __name__ == '__main__': # checks to see the Main function
 object = Mesh() # creates instance of your Mesh class by putting it on an object
 object.run() # object actually runs when calling run function
