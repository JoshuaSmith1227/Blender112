from cmu_graphics import *
import random
import copy
import math


#==============================================
#               CROSS PRODUCT
#==============================================

def getNormalVector(v1, v2):
    Ax, Ay, Az, = v1[0], v1[1], v1[2]
    Bx, By, Bz = v2[0], v2[1], v2[2]
    
    Nx = Ay*Bz - Az*By
    Ny = Az*Bx - Ax*Bz
    Nz = Ax*By - Ay*Bx
    
    return [Nx, Ny, Nz]

#==============================================
#               Normalize Vector
#==============================================

def convertToUnitVector(v):
    pythag = (v[0]**2 + v[1]**2 + v[2]**2)**.5
    if(pythag != 0):
        Nx = v[0]/pythag
        Ny = v[1]/pythag
        Nz = v[2]/pythag
        return [Nx, Ny, Nz]
    return [0, 0, 0]

#==============================================
#               DOT PRODUCT
#==============================================

def dotProduct(cameraVector, v1, v2):
    Ax, Ay, Az = v1[0], v1[1], v1[2]
    Bx, By, Bz = v2[0], v2[1], v2[2]
    
    Dx = Ax*(Bx-cameraVector[0])
    Dy = Ay*(By-cameraVector[1])
    Dz = Az*(Bz-cameraVector[2])

    return Dy + Dx + Dz

def dotProductNoCamera(v1, v2):
    Ax, Ay, Az = v1[0], v1[1], v1[2]
    Bx, By, Bz = v2[0], v2[1], v2[2]
    
    Dx = Ax*(Bx)
    Dy = Ay*(By)
    Dz = Az*(Bz)

    return Dy + Dx + Dz

#==============================================
#               VECTOR MATRIX MULTIPLY
#==============================================

def matrixMultiply(point, xT, yT, zT, transformMatrix):
    x = point[0]+xT
    y = point[1]+yT
    z = point[2]+zT
    
    xOut = x*transformMatrix[0][0] + y*transformMatrix[1][0] + z*transformMatrix[2][0] + transformMatrix[3][0]
    yOut = x*transformMatrix[0][1] + y*transformMatrix[1][1] + z*transformMatrix[2][1] + transformMatrix[3][1]
    zOut = x*transformMatrix[0][2] + y*transformMatrix[1][2] + z*transformMatrix[2][2] + transformMatrix[3][2]
    
    w = x*transformMatrix[0][3] + y*transformMatrix[1][3] + z*transformMatrix[2][3] + transformMatrix[3][3]
    
    if(w != 0):
        xOut /= w
        yOut /= w
        zOut /= w
        
    return [xOut, yOut, zOut]

#==============================================
#        VECTOR MATRIX MULTIPLY(NON NORMALIZED)
#==============================================

def vectorMatrixMultiply(v, M):
    output = [0, 0, 0, 0]
    v1 = v
    v1.append(1)

    output[0] = v1[0] + M[0][0] + v1[1] + M[1][0] + v1[2] + M[2][0] + v1[3] + M[3][0]
    output[1] = v1[0] + M[0][1] + v1[1] + M[1][1] + v1[2] + M[2][1] + v1[3] + M[3][1]
    output[2] = v1[0] + M[0][2] + v1[1] + M[1][2] + v1[2] + M[2][2] + v1[3] + M[3][2]
    output[3] = v1[0] + M[0][3] + v1[1] + M[1][3] + v1[2] + M[2][3] + v1[3] + M[3][3]
    return output

#==============================================
#               MATRIX MATRIX MULTIPLY
#==============================================

def matrixMatrixMultiply(M1, M2):
    if(len(M1[0]) != 4):
        for row in M1:
            row.append(1)  
    if(len(M2[0]) != 4):
        for row in M2:
            row.append(1)  

    result = [[0, 0, 0, 0] for i in range(4)]
    for c in range(4):
        for r in range(4):
            result[r][c] = (M1[r][0] * M2[0][c] + M1[r][1] * M2[1][c]+ M1[r][2]*M2[2][c]+ M1[r][3]*M2[3][c])
    return result

#==============================================
#         VECTOR ADD/ SUBTRACT/ MULTIPLY/ DIVIDE
#==============================================

def vectorAdd(v1, v2):
    return [v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2]]
    
def vectorSubtract(v1, v2):
    return [v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2]]
    
def vectorMultiply(v1, c):
    return [v1[0]*c, v1[1]*c, v1[2]*c]
    
def vectorDivide(v1, c):
    return [v1[0]/c, v1[1]/c, v1[2]/c]

def intersectPlane(point, planeNormal, lineStart, lineEnd):
    planeNormal = convertToUnitVector(planeNormal)
    planeDotProd = -dotProductNoCamera(planeNormal, point)
    ad = dotProductNoCamera(lineStart, planeNormal)
    bd = dotProductNoCamera(lineEnd, planeNormal)
    t = (planeDotProd - ad)/(bd-ad)
    lineStartToEnd = vectorSubtract(lineEnd, lineStart)
    lineIntersect = vectorMultiply(lineStartToEnd, t)
    return vectorAdd(lineStart, lineIntersect)


def planePointDist(point, plane):
    point = convertToUnitVector(point)
    return plane[0]*point[0] + plane[1]*point[1] + plane[2]*point[2] - dotProductNoCamera(plane, point)

