from cmu_graphics import *
import random
import copy
import math
from MeshClass import*
from buttonClass import*
from cameraClass import*

def extractPoints(txtFile):
    s = open(txtFile, "r").read()
    i = 1
    vertexDict = dict()
    finalPoints = []
    for line in s.splitlines():
        words = line.split()
        if(words[0] == 'v'):           
            vertexDict[i] = (float(words[1]), float(words[2]), float(words[3]))
            i += 1
        if(words[0] == 'f'):
            finalPoints.append([vertexDict[int(words[1])], vertexDict[int(words[2])], vertexDict[int(words[3])]])
    return finalPoints   

def extractPointsLines(txtFile):
    s = open(txtFile, "r").read()
    i = 1
    vertexDict = dict()
    finalPoints = []
    for line in s.splitlines():
        words = line.split()
        if(words[0] == 'v'):           
            vertexDict[i] = (float(words[1]), float(words[2]), float(words[3]))
            i += 1
        if(words[0] == 'l'):
            finalPoints.append([vertexDict[int(words[1])], vertexDict[int(words[2])]])
    return finalPoints  

# ====================================================
#              Choose Mesh
# ====================================================     

def chooseMesh(s):
    one = [-.5, .5, .5]
    two = [.5, .5, .5]
    three = [-.5, .5, -.5]
    four = [.5, .5, -.5]
    five   = [0, 1.3, 0]
    
    pyramid = [
        [three, two, one],
        [two, four, five],
        [three, one, five],
        [four, three, five],
        [one, two, five],
        [three, four, two]
        ]
    rectHeight = 1
    size = 1
    Plane = [
            [(0, 0, 0), (0, size, 0), (size, size, 0)], 
            [(0, 0, 0), (size, size, 0), (size, 0, 0)], 
            ]
    Rect = [
            #south
            [(0, 0, 0), (0, rectHeight, 0), (1, rectHeight, 0)], 
            [(0, 0, 0), (1, rectHeight, 0), (1, 0, 0)], 
            #east
            [(1, 0, 0), (1, rectHeight, 0), (1, rectHeight, 1)], 
            [(1, 0, 0), (1, rectHeight, 1), (1, 0, 1)], 
            #north
            [(1, 0, 1), (1, rectHeight, 1), (0, rectHeight, 1)], 
            [(1, 0, 1), (0, rectHeight, 1), (0, 0, 1)], 
            #west
            [(0, 0, 1), (0, rectHeight, 1), (0, rectHeight, 0)], 
            [(0, 0, 1), (0, rectHeight, 0), (0, 0, 0)], 
            #Top
            [(0, rectHeight, 0), (0, rectHeight, 1), (1, rectHeight, 1)], 
            [(0, rectHeight, 0), (1, rectHeight, 1), (1, rectHeight, 0)], 
            #Bottom
            [(1, 0, 1), (0, 0, 1), (0, 0, 0)], 
            [(1, 0, 1), (0, 0, 0), (1, 0, 0)], 
        ]
    monkey = extractPoints("C:\\Users\\Owner\\Downloads\\Monkey2.obj")
    cylindar = extractPoints("C:\\Users\\Owner\\Downloads\\CylindarTest.obj")
    sphere = extractPoints("C:\\Users\\Owner\\Downloads\\Sphere2.obj")
    chicken = extractPoints("C:\\Users\Owner\\Downloads\\Low Poly Chicken.obj")
    teapot = extractPoints("C:\\Users\\Owner\\Downloads\\teapot.obj")
    torus = extractPoints("C:\\Users\\Owner\\Downloads\\Torus.obj")
    twoCubes = extractPoints("C:\\Users\\Owner\\Downloads\\twoCubes.obj")


    if(s == 'pyramid'):
        return pyramid
    elif(s == 'cube'):
        return Rect
    elif(s == 'plane'):
        return Plane
    elif(s == 'monkey'):
        return monkey
    elif(s == 'cylindar'):
        return cylindar
    elif(s == 'sphere'):
        return sphere
    elif(s == 'chicken'):
        return chicken
    elif(s == 'teapot'):
        return teapot
    elif(s == 'torus'):
        return torus
    elif(s == 'twoCubes'):
        return twoCubes

# ====================================================
#           Tuple List <-> List
# ==================================================== 

def listToTupleList(L):
    result = []
    for i in range(0, len(L), 2):
        t = (L[i], L[i+1])
        result.append(t)
    return result

def tupleToList(L):
    result = []
    for t in L:
        result.append(t[0])
        result.append(t[1])
    return result

# ====================================================
#           TRIANGLE FUNCTIONS
# ==================================================== 

def centerPoint(triangle):
    x = [p[0] for p in triangle]
    y = [p[1] for p in triangle]
    return sum(x) / 3, sum(y) / 3

def rescaleTri(triangle, scaleFactor):
    centroid = centerPoint(triangle)

    result = []
    for point in triangle:
        newPoint = (
            centroid[0] + scaleFactor * (point[0] - centroid[0]),
            centroid[1] + scaleFactor * (point[1] - centroid[1])
        )
        result.append(newPoint)
    
    return result

def drawTriangle(x0, y0, x1, y1, x2, y2):
    drawLine(x1, y1, x2, y2, fill = 'orange', lineWidth = 4)
    drawLine(x0, y0, x1, y1, fill = 'orange', lineWidth = 4)
    drawLine(x2, y2, x0, y0, fill = 'orange', lineWidth = 4)
    
def distance(x0, x1, y0, y1):
    return ((x0-x1)**2+(y0-y1)**2)**.5


def pointInPolygon(points, mx, my):
    inside = False
    x1, y1 = points[0]
    for i in range(len(points) + 1):
        x2, y2 = points[i % len(points)]
        if my > min(y1, y2):
            if my < max(y1, y2):
                if mx < max(x1, x2):
                    if y1 != y2:
                        xinters = (my - y1) * (x2 - x1) / (y2 - y1) + x1
                    if x1 == x2 or mx <= xinters:
                        inside = not inside
        x1, y1 = x2, y2

    return inside

def drawLinePoints(p1, p2, color, drawArrow, width, opacity = 100):
    x0, y0 = p1[0], p1[1]
    x1, y1 = p2[0], p2[1]
    drawLine(x0, y0, x1, y1, fill = color, arrowEnd = drawArrow, lineWidth = width, opacity = opacity)


def intersect(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    
    a = (x1*y2 - y1*x2)
    b = (x3*y4 - y3*x4)
    
    x1Diff = x1 - x2
    y1Diff = y1 - y2
    x2Diff = x3 - x4
    y2Diff = y3 - y4
    
    detDiff = (x1Diff * y2Diff - y1Diff * x2Diff)
    if(detDiff == 0):
        return None
    
    xIntersect = (a * x2Diff - x1Diff * b)/detDiff
    yIntersect = (a * y2Diff - y1Diff * b)/detDiff

    if (min(x1, x2) <= xIntersect <= max(x1, x2) and
        min(y1, y2) <= yIntersect <= max(y1, y2) and
        min(x3, x4) <= xIntersect <= max(x3, x4) and
        min(y3, y4) <= yIntersect <= max(y3, y4)):
        return (xIntersect, yIntersect)
    else:
        return None



def polar_angle(p0, p1=None):
    if p1 == None: p1 = polar_angle.P0
    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]
    return math.atan2(y_span, x_span)

def distance(p0, p1=None):
    if p1 == None: p1 = distance.P0
    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]
    return y_span**2 + x_span**2

def det(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def grahamScan(points):
    pivot = min(points, key=lambda p: (p[1], p[0]))
    polar_angle.P0 = pivot
    distance.P0 = pivot
    sorted_points = sorted(points, key=lambda p: (polar_angle(p), -distance(p)))
    convex_hull = sorted_points[:3]
    for p in sorted_points[3:]:
        while len(convex_hull) > 1 and det(convex_hull[-2], convex_hull[-1], p) <= 0:
            convex_hull.pop()
        convex_hull.append(p)

    return convex_hull


def sortMeshData(triangles):
    if len(triangles) <= 1:
        return triangles
    mid = len(triangles) // 2
    left_half = sortMeshData(triangles[:mid])
    right_half = sortMeshData(triangles[mid:])

    return merge(left_half, right_half)

def merge(left, right):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        m1 = sum(vertex[2] for vertex in left[i].preProjectedTri) / len(left[i].preProjectedTri)
        m2 = sum(vertex[2] for vertex in right[j].preProjectedTri) / len(right[j].preProjectedTri)
        if m1 > m2:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    while i < len(left):
        merged.append(left[i])
        i += 1
    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged

def getAverage(points):
    avgX = 0
    avgY = 0
    for point in points:
        avgX += point[0]
        avgY += point[1]
    return (avgX/len(points), avgY/len(points))
    

def resizePolygon(points, scaleFactor):
    avgPoint = getAverage(points)
    newPoly = []
    for point in points:
        dx = avgPoint[0] + scaleFactor * (point[0]-avgPoint[0])
        dy = avgPoint[1] + scaleFactor * (point[1]-avgPoint[1])
        newPoly.append( (dx, dy) )
    return newPoly

def drawBetterRect(app, x, y, width, height, color, borderWidth, o = 100):
    drawCircle(x, y, borderWidth, fill = color, opacity = o)
    drawCircle(x+width, y, borderWidth, fill = color, opacity = o)
    drawCircle(x, y+height, borderWidth, fill = color, opacity = o)
    drawCircle(x+width, y+height, borderWidth, fill = color, opacity = o)
    
    drawRect(x, y-borderWidth, width, height+(2*borderWidth), fill = color, opacity = o)
    drawRect(x-borderWidth, y, width+(2*borderWidth), height, fill = color, opacity = o)
    drawRect(x, y, width, height, fill = color, opacity = o)

def getCurrentMode(app):
    for e in app.modeStates:
        if(app.modeStates[e] and e == 'Object'):
            return app.imageStorage.objectModeIcon
        elif(app.modeStates[e] and e == 'Edit'):
            return app.imageStorage.editModeIcon
        elif(app.modeStates[e] and e == 'Sculpt'):
            return app.imageStorage.scluptModeIcon
        
def dist(x0, x1, y0, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**.5