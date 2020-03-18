import array
import math
from matrix import *
from subprocess import Popen, PIPE
from os import remove

pixels = [0]
w = 0
h = 0
header = ""

def createPixels(width, height, maxval):
    global pixels
    global w
    global h
    global header
    pixels = array.array('B', [255, 255, 255] * width * height)
    w  = width
    h = height
    header = "P3 " + str(w) + " "+ str(h) + " " + str(maxval) + "\n"

def writeImage(path):
    fd = open(path, 'w')
    print ("Writing image...")
    fd.write(header)
    for pixel in pixels:
        fd.write(str(pixel) + " ")
    fd.close()

def clearpixels():
    global pixels
    for x in range(len(pixels)):
        pixels[x] = 255;

def colorPixel (x, y, color):
    newy = h - 1 - y
    index = (w * (h- y - 1) + x) * 3
    global pixels
    if ( x >= 0 and x < w and newy >= 0 and newy < h ):
        pixels[index] = color[0]
        pixels[index + 1] = color[1]
        pixels[index + 2] = color[2]

def getPixel(x,y):
    index = (w * y + x) * 3
    global pixels
    return [pixels[index], pixels[index + 1], pixels[index + 2]]

def saveExtension(fname ):
    ppmName = fname[:fname.find('.')] + '.ppm'
    writeImage(ppmName)
    p = Popen( ["convert", ppmName, fname ], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppmName)

def display():
    ppmName = 'pic.ppm'
    writeImage(ppmName )
    p = Popen( ['display', ppmName], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppmName)

def drawLine (p0, p1, color):
    x0 = p0[0]
    x1 = p1[0]
    y0 = p0[1]
    y1 = p1[1]
    print("plotting line {},{} to {},{}".format(x0, y0, x1, y1))
    a = y1-y0
    b = x1-x0
    if abs(a) < abs (b):
        if x0 > x1:
            drawLine([x1, y1], [x0, y0], color)
            # print ("swapped 1,2")
        else:
            i = 1
            y = y0
            # print ("slope{}".format(slope))
            if a < 0:
                i = -1
                a *= -1
            d = 2 * a - b
            for x in range (x0,x1 + 1):
                colorPixel(x, y, color)
                # print("drew {}, {}".format(x,y))
                if d > 0:
                    d -= 2 * b
                    if a > 0:
                        y +=i
                    else:
                        y -=i
                d += 2 * a
    else:
        if y0 > y1:
            drawLine([x1, y1], [x0, y0], color)
        else:
            x = x0
            # print ("slope{}".format(slope))
            i = 1
            if b < 0:
                i = -1
                b *= -1
            d = 2 * b - a
            for y in range (y0,y1 + 1):
                colorPixel(x, y, color)
                # print("drew {}, {}".format(x,y))
                if d > 0:
                    d -= 2 * a
                    if b > 0:
                        x +=i
                    else :
                        x -=i
                d += 2 * b

def addEdge ( matrix, x0, y0, z0, x1, y1, z1 ):
    addPoint(matrix, x0, y0, z0)
    addPoint(matrix, x1, y1, z1)
# def fillColor(color):
#     for i in range(0, w * h):
#         if getPixel()

def drawEdges(matrix, color):
    for i in range(0, int(math.floor(len(matrix))/2)):
        drawLine([int(matrix[i*2][0]), int(matrix[i*2][1])],
        [int(matrix[i*2+1][0]), int(matrix[i*2 +1][1])], color)

def addCircle(matrix, cx, cy, cz, r, step):
    for i in range(int(1/step)):
        x0 = cx + r * math.cos(i * step * 2 * math.pi)
        y0 = cy + r * math.sin(i * step * 2 * math.pi)
        x1 = cx + r * math.cos((i+1) * step * 2 * math.pi)
        y1 = cy + r * math.sin((i+1) * step * 2 * math.pi)
        addEdge(matrix, x0, y0, 1, x1, y1, 1)

def addCurve (matrix, x0, y0, x1, y1, x2, y2, x3, y3, step, type):
    for i in range(int(1/step)):
        coeffMat = curveCoefficients([x0, y0, 0, 1], [x1, y1, 0, 1], [x2, y2, 0, 1], [x3, y3, 0, 1])
        if (type == "hermite"):
            curveMat = hermite()
        elif (type == "bezier"):
            curveMat = bezier()
        matrixMulti(curveMat, coeffMat)
        points = []
        stepMat = [(i * step) **3, (i *step) **2, (i * step), 1]
        for m in range(4):
            x = 0
            for  n in range(4):
                x += stepMat[n] * coeffMat[m][n]
            points.append(x)
        coeffMat = curveCoefficients([x0, y0, 0, 1], [x1, y1, 0, 1], [x2, y2, 0, 1], [x3, y3, 0, 1])
        matrixMulti(curveMat, coeffMat)
        stepMat = [((i+1) * step) **3, ((i+1) *step) **2, ((i+1) * step), 1]
        for m in range(4):
            x = 0
            for n in range(4):
                x += stepMat[n] * coeffMat[m][n]
            points.append(x)
        addEdge(matrix, points[0], points[1], 0, points[4], points[5], 0)

def addBox (matrix, x, y, z, width, height, depth):
    # for i in range(y, y - height):
    #     addEdge(matrix, x, i, z, x + width, i, z)
    #     addEdge(matrix, x, i, z - depth, x + width, i, z - depth )
    #     addEdge(matrix, x, i, z, x, i, z - depth)
    #     addEdge(matrix, x + width, i, z, x + width, i, z - depth )
    # for i in range (x, x + width):
    #     addEdge(matrix, i, y, z, i, y, z - depth)
    #     addEdge(matrix, i, y - height, z, i, y - height, z - depth)
        addEdge(matrix, x, y, z, x + width, y, z)
        addEdge(matrix, x, y - height, z, x + width, y - height, z)
        addEdge(matrix, x, y - height, z - depth, x + width, y - height, z - depth)
        addEdge(matrix, x, y, z - depth, x + width, y, z - depth)

        addEdge(matrix, x, y, z, x, y, z - depth)
        addEdge(matrix, x + width, y, z, x + width, y, z - depth)
        addEdge(matrix, x, y - height, z, x, y - height, z - depth)
        addEdge(matrix, x + width, y - height, z, x + width, y - height, z - depth)

        addEdge(matrix, x, y, z, x, y - height, z)
        addEdge(matrix, x + width, y, z, x + width, y - height, z)
        addEdge(matrix, x, y, z - depth, x, y - height, z - depth)
        addEdge(matrix, x + width, y, z - depth, x + width, y - height, z - depth)

def generateSphere(cx, cy, cz, r, step):
    mat = newMatrix(4,0)
    for phi in range(int(1/step)):
        for theta in range(int(1/step)):
            mat.append([r * math.cos(theta * math.pi * step) + cx,
                        r * math.sin(theta * math.pi * step) * math.cos(phi * 2 * math.pi * step) + cy,
                        r * math.sin(theta * math.pi * step) * math.sin(phi * 2 * math.pi * step) + cz, 1])
    return mat

def addSphere(matrix, cx, cy, cz, r, step):
    mat = generateSphere(cx, cy, cz, r, step)
    for point in mat:
        addEdge(matrix, point[0], point[1], point[2], point[0] + 1, point[1] + 1, point[2] + 1)


def generateTorus(cx, cy, cz, r0, r1, step):
    mat = newMatrix(4,0)
    for phi in range(int(1/step)):
        for theta in range(int(1/step)):
            mat.append([(r1 + r0 * math.cos(theta * 2 * math.pi * step)) * math.cos(phi * 2 * math.pi * step) + cx,
                        r0 * math.sin(theta * 2 * math.pi * step) + cy,
                        (-1 * (r1 + r0 * math.cos(theta * 2 * math.pi * step)) * math.sin(phi * 2 * math.pi * step)) + cz, 1])
    return mat

def addTorus(matrix, cx, cy, cz, r0, r1, step):
    mat = generateTorus(cx, cy, cz, r0, r1, step)
    for point in mat:
        addEdge(matrix, point[0], point[1], point[2], point[0] + 1, point[1] + 1, point[2] + 1)
