from cmu_graphics import *
import math
from MeshClass import*
from buttonClass import*
from cameraClass import*
from otherFunctions import*


def makeGrid(app):
    app.lines = []
    for i in range(-15, 16):
        app.lines.append( lineObject([-15, 2, i], [15, 2, i], app.camera, [0, 0, 0]) )
        app.lines.append( lineObject([i, 2, -15], [i, 2, 15], app.camera, [0, 0, 0]) )

        
def drawGrid(app):
    drawXYZlines(app)
    for line in app.lines:
        if(len(line.getTransformedPoints()) == 2):
            drawLinePoints(line.getTransformedPoints()[0], line.getTransformedPoints()[1], 'gray', False, 1, 40)


def drawXYZlines(app):
    x = lineObject([-15, 2, 0], [15, 2, 0], app.camera, [0, 0, 0]).getTransformedPoints()
    y = lineObject([0, 2, -15], [0, 2, 15], app.camera, [0, 0, 0]).getTransformedPoints()
    z = lineObject([0, 10, 0], [0, -10, 0], app.camera, [0, 0, 0]).getTransformedPoints()
    if(len(x) == 2):
        drawLinePoints(x[0], x[1], 'red', False, 1.5, 50)
    if(len(y) == 2):
        drawLinePoints(y[0], y[1], 'green', False, 1.5, 50)
    #drawLinePoints(z[0], z[1], 'blue', False, 1.5, 50)


def draw3DShape(app, mesh, i):
    frontTris = mesh.getTransformedPoints()[0]
    hiddenTris = mesh.getTransformedPoints()[1]

    if(i == app.selectedMeshIndex):
        drawOutline(frontTris)

    if(len(frontTris) < 10):
        for tri in range( len(hiddenTris) ):
            ax, ay = hiddenTris[tri].screenPoints[0], hiddenTris[tri].screenPoints[1]
            bx, by = hiddenTris[tri].screenPoints[2], hiddenTris[tri].screenPoints[3]
            cx, cy = hiddenTris[tri].screenPoints[4], hiddenTris[tri].screenPoints[5]
            drawPolygon(ax, ay, bx, by, cx, cy, fill = hiddenTris[tri].color, border = hiddenTris[tri].color, borderWidth = 1, opacity = 100) 

    for tri in range( len(frontTris) ):
        ax, ay = frontTris[tri].screenPoints[0], frontTris[tri].screenPoints[1]
        bx, by = frontTris[tri].screenPoints[2], frontTris[tri].screenPoints[3]
        cx, cy = frontTris[tri].screenPoints[4], frontTris[tri].screenPoints[5]
        drawPolygon(ax, ay, bx, by, cx, cy, fill = frontTris[tri].color, border = frontTris[tri].color, borderWidth = 1, opacity = 100)    
        
        #drawCircle(ax, ay, .9, fill = 'gray')
        #drawCircle(bx, by, .9, fill = 'gray')
        #drawCircle(cx, cy, .9, fill = 'gray')


def getMoveScaleRotatePoints(app, i):
    startPoint = vectorSubtract(app.meshList[i].translateList, app.meshList[i].rotationPoint)
    startPoint[1] += 1
    midpoint = point(startPoint, app.camera).getTransformedPoints()

    xLine = lineObject(startPoint, vectorAdd(startPoint, [1, 0, 0]), app.camera, app.worldPivot).getTransformedPoints()
    yLine = lineObject(startPoint, vectorAdd(startPoint, [0, 0, 1]), app.camera, app.worldPivot).getTransformedPoints()
    zLine = lineObject(startPoint, vectorAdd(startPoint, [0, -1, 0]), app.camera, app.worldPivot).getTransformedPoints()
    return [xLine, yLine, zLine]


def drawControl(app, i):
    startPoint = vectorSubtract(app.meshList[i].translateList, app.meshList[i].rotationPoint)
    startPoint[1] += 1
    midpoint = point(startPoint, app.camera).getTransformedPoints()

    if(app.move):
        xLine = getMoveScaleRotatePoints(app, i)[0]
        yLine = getMoveScaleRotatePoints(app, i)[1]
        zLine = getMoveScaleRotatePoints(app, i)[2]

        drawLinePoints(yLine[0], yLine[1], 'green', True, 1)
        drawLinePoints(zLine[0], zLine[1], 'blue', True, 1)
        drawLinePoints(xLine[0], xLine[1], 'red', True, 1)
    if(app.scale):
        xLine = getMoveScaleRotatePoints(app, i)[0]
        yLine = getMoveScaleRotatePoints(app, i)[1]
        zLine = getMoveScaleRotatePoints(app, i)[2]
        
        drawLinePoints(xLine[0], xLine[1], 'red', False, 1)
        drawLinePoints(yLine[0], yLine[1], 'green', False, 1)
        drawLinePoints(zLine[0], zLine[1], 'blue', False, 1)

        drawRect(xLine[1][0]-5, xLine[1][1]-5, 10, 10, fill = 'red')
        drawRect(yLine[1][0]-5, yLine[1][1]-5, 10, 10, fill = 'green')
        drawRect(zLine[1][0]-5, zLine[1][1]-5, 10, 10, fill = 'blue')
    if(app.rotate):
        draw3DCircle("C:\\Users\\Owner\\Downloads\\circle.obj", i, 'blue')
        draw3DCircle("C:\\Users\\Owner\Downloads\\yCircle2.obj", i, 'green')
        draw3DCircle("C:\\Users\\Owner\\Downloads\\zCircle2.obj", i, 'red')

    drawCircle(midpoint[0], midpoint[1], 3, fill = 'orange', border = 'black', borderWidth = .75)
    drawCircle(midpoint[0], midpoint[1], 15, fill = None, border = 'white', borderWidth = .75)


def draw3DCircle(txtfile, i, color):
    startPoint = vectorSubtract(app.meshList[i].translateList, app.meshList[i].rotationPoint)
    startPoint[1] += 1
    midpoint = point(startPoint, app.camera).getTransformedPoints()
    
    circle = extractPointsLines(txtfile)
    for line in circle:
        lineSegment = lineObject(vectorAdd(line[0], startPoint), vectorAdd(line[1], startPoint), app.camera, app.worldPivot).getTransformedPoints()
        drawLinePoints(lineSegment[0], lineSegment[1], color, False, 2, 70)

def squareWave(trigFunction, angle):
    if(trigFunction == 'sin'):
        if(math.sin(angle) > 0):
            return 1
        else:
            return -1
    elif(trigFunction == 'cos'):
        if(math.cos(angle) > 0):
            return 1
        else:
            return -1
    elif(trigFunction == 'tan'):
        if(math.tan(angle) > 0):
            return 1
        else:
            return -1

def drawWorldOrigin():
    p1 = point(vectorAdd(app.meshSpawnPoint, [0, 2, 0]), app.camera).getTransformedPoints()
    startPoint = vectorAdd(app.meshSpawnPoint, [0, 2, 0])
    xLine = lineObject(vectorAdd(startPoint, [-.1, 0, 0]), vectorAdd(startPoint, [.1, 0, 0]), app.camera, app.worldPivot).getTransformedPoints()
    yLine = lineObject(vectorAdd(startPoint, [0, 0, -.1]), vectorAdd(startPoint, [0, 0, .1]), app.camera, app.worldPivot).getTransformedPoints()
    zLine = lineObject(vectorAdd(startPoint, [0, .1, 0]), vectorAdd(startPoint, [0, -.1, 0]), app.camera, app.worldPivot).getTransformedPoints()
    
    if(p1 != None):
        if(len(p1) == 2):
            drawCircle(p1[0], p1[1], 10, fill = None, border = 'white', borderWidth = .5)
    if(xLine != None):
        if(len(xLine) == 2):
            drawLinePoints(xLine[0], xLine[1], 'black', False, 1)
    if(yLine != None):
        if(len(yLine) == 2):
            drawLinePoints(yLine[0], yLine[1], 'black', False, 1)
    if(zLine != None):
        if(len(zLine) == 2):
            drawLinePoints(zLine[0], zLine[1], 'black', False, 1)
    if(p1 != None):
        if(len(p1) == 2):
            drawCircle(p1[0], p1[1], 2.5, fill = 'orange', border = 'black', borderWidth = .2)


def drawSelectedAxisLines(app):
    if(app.selectedMeshIndex != None and app.move):
        startPoint = vectorSubtract(app.meshList[app.selectedMeshIndex].translateList, app.meshList[app.selectedMeshIndex].rotationPoint)
        startPoint[1] += 1
        if('x-axis' in app.selectedAxis):
            xLine = lineObject(vectorAdd([-20, 0, 0], startPoint), vectorAdd([20, 0, 0], startPoint), app.camera, app.worldPivot).getTransformedPoints()
            drawLinePoints(xLine[0], xLine[1], 'red', False, 1)
        if('y-axis' in app.selectedAxis):
            yLine = lineObject(vectorAdd([0, 0, -20], startPoint), vectorAdd([0, 0, 20], startPoint), app.camera, app.worldPivot).getTransformedPoints()
            drawLinePoints(yLine[0], yLine[1], 'green', False, 1)
        if('z-axis' in app.selectedAxis):
            zLine = lineObject(vectorAdd([0, -20, 0], startPoint), vectorAdd([0, 20, 0], startPoint), app.camera, app.worldPivot).getTransformedPoints()
            drawLinePoints(zLine[0], zLine[1], 'blue', False, 1)

def drawOutline(frontTris):
    result = []
    for tri in range( len(frontTris) ):
        ax, ay = frontTris[tri].screenPoints[0], frontTris[tri].screenPoints[1]
        bx, by = frontTris[tri].screenPoints[2], frontTris[tri].screenPoints[3]
        cx, cy = frontTris[tri].screenPoints[4], frontTris[tri].screenPoints[5]
        result.extend([(ax, ay), (bx, by), (cx, cy)])
    drawPolygon(*tupleToList(resizePolygon(grahamScan(result), 1.025)), fill = 'orange')


def spawnNewMesh(app, meshName):

    if(meshName == 'plane'):
        app.selectedButton = None
        app.meshList.append( Mesh( chooseMesh('plane'), 'plane', app.camera, app.worldPivot) )
    elif(meshName == 'cube'):
        app.selectedButton = None
        app.meshList.append(  Mesh( chooseMesh('cube'), 'cube', app.camera, app.worldPivot) )
    elif(meshName == 'Circle'):
        pass
    elif(meshName == 'UV Sphere'):
        pass
    elif(meshName == 'Ice Sphere'):
        pass
    elif(meshName == 'Cylinder'):
        app.selectedButton = None
        app.meshList.append(  Mesh( chooseMesh('cylindar'), 'cylindar', app.camera, app.worldPivot) )


    
        

