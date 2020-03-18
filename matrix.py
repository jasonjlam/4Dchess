import math

#print the matrix such that it looks like
#the template in the top comment
def printMatrix( matrix ):
    print ("-" * 2 * len(matrix))
    for r in range(0,4):
        for c in range(0, len(matrix)):
            # print("{}, {}".format(r,c))
            print(str(matrix[c][r]) + " ", end = '')
            if (c == len(matrix) - 1):
                print("")
    print ("-" * 2 * len(matrix))

#turn the paramter matrix into an identity matrix
#you may assume matrix is square
def identity( matrix ):
    for c in range(0, len(matrix)):
        for r in range(0, len(matrix[c])):
            if c == r:
                matrix[c][r] = 1
            else:
                matrix[c][r] = 0
    return matrix

#multiply m1 by m2, modifying m2 to be the product
#m1 * m2 -> m2
def matrixMulti( m1, m2 ):
    for c in range(0, len(m2)):
        temp = []
        for r in range(0, 4):
            # print ("{},{}".format(c,r))
            i = 0
            for x in range(0,4):
                # print("{}*{}".format(m1[x][r], m2[c][x]))
                i += m1[x][r] * m2[c][x]
                # print(i)
            temp.append(i)
        m2[c] = temp


def newMatrix(rows = 4, cols = 4):
    m = []
    for c in range( cols ):
        m.append( [] )
        for r in range( rows ):
            m[c].append( 0 )
    return m

def addPoint(matrix, x, y, z= 0):
    matrix.append([x,y,z, 1])

def scaleMatrix(sx, sy, sz):
    mat = newMatrix(4,0)
    mat.append([int(sx), 0, 0, 0])
    mat.append([0, int(sy), 0, 0])
    mat.append([0, 0, int(sz), 0])
    mat.append([0, 0, 0, 1])
    return mat

def translateMatrix(tx, ty, tz):
    mat = newMatrix(4,0)
    mat.append([1, 0, 0, 0])
    mat.append([0, 1, 0, 0])
    mat.append([0, 0, 1, 0])
    mat.append([int(tx), int(ty), int(tz), 1])
    return mat

def rotateMatrix(axis, theta):
    mat = newMatrix(4,0)
    theta = math.radians(theta)
    if axis == "x":
        mat.append([1, 0,0,0])
        mat.append([0, math.cos(theta), math.sin(theta), 0])
        mat.append([0, -math.sin(theta), math.cos(theta), 0])
    if axis == "y":
        mat.append([math.cos(theta), 0, -math.sin(theta), 0])
        mat.append([0,1,0,0])
        mat.append([math.sin(theta), 0, math.cos(theta), 0])
    if axis == "z":
        mat.append([math.cos(theta), math.sin(theta), 0, 0])
        mat.append([-math.sin(theta), math.cos(theta), 0, 0])
        mat.append([0, 0, 1, 0])
    mat.append([0, 0, 0, 1])
    printMatrix(mat)
    return mat

def bezier():
    bMat = newMatrix(4,0)
    bMat.append([-1, 3, -3, 1])
    bMat.append([3, -6, 3, 0])
    bMat.append([-3, 3, 0, 0])
    bMat.append([1, 0, 0, 0])
    return bMat
    pass

def hermite():
    hMat = newMatrix(4,0)
    hMat.append([2, -3, 0, 1])
    hMat.append([-2, 3, 0, 0])
    hMat.append([1, -2, 1, 0])
    hMat.append([1, -1, 0, 0])
    return hMat
    pass

def curveCoefficients( p0, p1, p2, p3):
    pMat = newMatrix(4,0)
    for p in range (4):
        pSet = [p0, p1, p2, p3]
        pMat.append([pSet[0][p],pSet[1][p],pSet[2][p],pSet[3][p]])
    return pMat
