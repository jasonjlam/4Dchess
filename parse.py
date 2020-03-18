from graphics import *
from matrix import *
import math

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         sphere: add a sphere to the edge matrix -
                     takes 4 arguemnts (cx, cy, cz, r)
         torus: add a torus to the edge matrix -
                    takes 5 arguemnts (cx, cy, cz, r1, r2)
         box: add a rectangular prism to the edge matrix -
                  takes 6 arguemnts (x, y, z, width, height, depth)
    	 circle: add a circle to the edge matrix -
    	         takes 4 arguments (cx, cy, cz, r)
    	 hermite: add a hermite curve to the edge matrix -
    	          takes 8 arguments (x0, y0, x1, y1, rx0, ry0, rx1, ry1)
    	 bezier: add a bezier curve to the edge matrix -
    	         takes 8 arguments (x0, y0, x1, y1, x2, y2, x3, y3)
         line: add a line to the edge matrix -
               takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
         ident: set the transform matrix to the identity matrix -
         scale: create a scale matrix,
                then multiply the transform matrix by the scale matrix -
                takes 3 arguments (sx, sy, sz)
         translate: create a translation matrix,
                    then multiply the transform matrix by the translation matrix -
                    takes 3 arguments (tx, ty, tz)
         rotate: create a rotation matrix,
                 then multiply the transform matrix by the rotation matrix -
                 takes 2 arguments (axis, theta) axis should be x y or z
         apply: apply the current transformation matrix to the edge matrix
         display: clear the screen, then
                  draw the lines of the edge matrix to the screen
                  display the screen
         save: clear the screen, then
               draw the lines of the edge matrix to the screen
               save the screen to a file -
               takes 1 argument (file name)
         quit: end parsing
See the file script for an example of the file format
"""
def parseFile( fname, points, transform, screen, color ):
    fd = open(fname, "r")
    lines = fd.readlines()
    lines = list(map(str.rstrip,lines))
    print(lines)
    for line in range(0, len(lines)):
        if lines[line] == "line":
            print("line")
            args = lines[line+1].split(" ")
            addEdge(points, float(args[0]), float(args[1]), float(args[2]), float(args[3]), float(args[4]), float(args[5]))
        elif lines[line] == "lineinv":
            print("lineinv")
            args = lines[line+1].split(" ")
            addEdge(points, float(args[0]), h - float(args[1]), float(args[2]), float(args[3]), h - float( args[4]), float(args[5]))
        elif lines[line] == "ident":
            print ("ident")
            transform = identity(transform)
        elif lines[line] == "scale":
            args = lines[line+1].split(" ")
            print ("scale")
            print(args)
            printMatrix(transform)
            printMatrix(scaleMatrix(float(args[0]), float(args[1]), float(args[2])))
            matrixMulti(scaleMatrix(float(args[0]), float(args[1]), float(args[2])), transform)
        elif lines[line] == "move":
            print ("move")
            args = lines[line+1].split(" ")
            matrixMulti(translateMatrix(float(args[0]), float(args[1]), float(args[2])),transform)
        elif lines[line] == "rotate":
            args = lines[line+1].split(" ")
            matrixMulti(rotateMatrix(args[0], float(args[1])), transform)
        elif lines[line] == "circle":
            args = lines[line+1].split(" ")
            print(args)
            addCircle(points, int(args[0]), int(args[1]), int(args[2]), int(args[3]), 0.01)
        elif lines[line] == "bezier":
            args = lines[line+1].split(" ")
            args = [int(i) for i in args]
            addCurve(points, int(args[0]), args[1], args[2], args[3], args[4], args[5], args[6], args[7], 0.01, "bezier")
        elif lines[line] == "bezierinv":
            args = lines[line+1].split(" ")
            args = [int(i) for i in args]
            addCurve(points, int(args[0]), h - args[1], args[2], h - args[3], args[4], h - args[5], args[6], h - args[7], 0.05, "bezier")
        elif lines[line] == "hermite":
            args = lines[line+1].split(" ")
            args = [float(i) for i in args]
            args = [int(i) for i in args]
            addCurve(points, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], 0.05, "hermite")
        elif lines[line] == "box":
            args = lines[line+1].split(" ")
            args = [int(i) for i in args]
            addBox(points, args[0], args[1], args[2], args[3], args[4], args[5])
        elif lines[line] == "sphere":
            args = lines[line+1].split(" ")
            args = [int(i) for i in args]
            addSphere(points, args[0], args[1], args[2], args[3], 0.02)
        elif lines[line] == "torus":
            args = lines[line+1].split(" ")
            args = [int(i) for i in args]
            addTorus(points, args[0], args[1], args[2], args[3], args[4], 0.01)

        elif lines[line] == "clear":
            points = newMatrix(4,0)
        elif lines[line] == "apply":
            print("apply")
            printMatrix(transform)
            printMatrix(points)
            matrixMulti(transform, points)
        elif lines[line] == "display":
            clearpixels()
            for i in range(0, len(points)):
                for x in range(0, len(points[i])):
                    points[i][x] = int(points[i][x])
            printMatrix(points)
            drawEdges(points, color)
            display()
        elif lines[line] == "save":
            args = lines[line+1].split(" ")
            saveExtension(args[0])
        elif lines[line] == "quit":
            return
