from cmu_graphics import *
import math
from MeshClass import*
from buttonClass import*
from cameraClass import*
from otherFunctions import*
from drawFunctions import*
from UI_Functions import*

#   pointInPolygon: https://www.geeksforgeeks.org/how-to-check-if-a-given-point-lies-inside-a-polygon/
#   Graham Scan Algorithm: https://www.geeksforgeeks.org/convex-hull-using-graham-scan/
#   Merge Sort from CS academy 

# ====================================================
#              On App StartS
# ==================================================== 

def onAppStart(app):
    app.imageStorage = imageStorage()
    app.width = 1100
    app.height = 700
    app.cameraVector = [0, 0, 0]

    app.cameraPos = [0, 0, 10]
    app.worldPivot = [.5, .5, .5]
    app.camera = Camera(app.cameraPos, [0, 0, 0], [0, 1, 0])
    
    app.testMesh = Mesh( chooseMesh('cube'), 'cube', app.camera, app.worldPivot)
    app.testMesh2 = Mesh( chooseMesh('pyramid'), 'pyramid', app.camera, app.worldPivot)

    app.testMesh.zTrans = 0
    app.testMesh.xTrans = 0
    app.testMesh.yTrans = 1

    app.testMesh2.zTrans = 15
    app.testMesh2.xTrans = 3
    app.testMesh2.yTrans = 0

    app.p1 = point(app.testMesh.getMidpoint(), app.camera)

    app.meshList = [app.testMesh]

    app.selectedMeshIndex = 0
    app.lines = []

    app.scale = False
    app.move = True
    app.rotate = False
    app.boxSelect = False

    app.modeStates = {
                'Object': True,
                'Edit': False,
                'Sculpt': False,
                    }

    app.sideButtons = getControlButtons(app)
    app.dropDownButtons = getDropDownButtons(app)

    app.controlButtons = app.sideButtons + app.dropDownButtons
    
    app.selectedButton = None
    app.hoveredButton = None

    app.mx = 1
    app.my = 1
    app.draggedMy = 1
    app.draggedMx = 1
    app.movedMy = 1
    app.movedMx = 1

    app.moveScaleRotateButtons = [0, 0, 0]
    app.selectedAxis = []
    app.drawDottedLine = False
    app.keyPress = False
    app.grab = False
    app.showMeshWindow = False
    app.keys = []


    
def onKeyHold(app, keys):
    app.keys = keys
    vForward = vectorMultiply(app.camera.lookDir, .3)
    vRight = vectorMultiply(getNormalVector(app.camera.lookDir, app.camera.up), .3)

    if('s' in keys):
        app.camera.cameraPos = vectorAdd([0, 0, .3], app.camera.cameraPos)
        app.camera.target = vectorAdd([0, 0, .3], app.camera.target)     
    elif('w' in keys):
        app.camera.cameraPos = vectorSubtract(app.camera.cameraPos, [0, 0, .3])
        app.camera.target = vectorSubtract(app.camera.target, [0, 0, .3])    
    elif('d' in keys):
        app.camera.cameraPos = vectorSubtract(app.camera.cameraPos, [.3, 0, 0])
        app.camera.target = vectorSubtract(app.camera.target, [.3, 0, 0])  
        #app.testMesh.worldPivot = vectorSubtract(app.testMesh.worldPivot, [0, 0, .1])
    elif('a' in keys):
        app.camera.cameraPos = vectorAdd(app.camera.cameraPos, [.3, 0, 0])
        app.camera.target = vectorAdd(app.camera.target, [.3, 0, 0])  
        #app.testMesh.worldPivot = vectorAdd([0, 0, .1], app.testMesh.worldPivot)
    elif('q' in keys):
        app.camera.cameraPos[1] -= .3
        app.camera.target[1] -= .3
    elif('e' in keys):
        app.camera.cameraPos[1] += .3
        app.camera.target[1] += .3

    if('tab' in keys):
        app.modeStates['Edit'] = True
        app.modeStates['Object'] = False
        app.modeStates['Sculpt'] = False
        app.currentMode.url = getCurrentMode(app)

    if(app.selectedMeshIndex != None):
        if('r' in keys):
            app.drawDottedLine = True
            app.selectedAxis = ['x-axis', 'y-axis', 'z-axis']
            app.move = False
            app.rotate = False
            app.scale = True
            app.selectedButton = 'SelectedScale.png'
            app.keyPress = True
        
        if('g' in keys):
            app.grab = True
            app.selectedAxis = ['x-axis', 'y-axis', 'z-axis']
            app.move = True
            app.rotate = False
            app.scale = False
            app.selectedButton = 'selectedMove.png'
            app.keyPress = True

    if( app.selectedButton == 'SelectedScale.png' or app.selectedButton == 'selectedMove.png'):
        if('x' in keys):
            app.keyPress = True
            app.selectedAxis = ['x-axis']
            #app.drawDottedLine = True
        if('y' in keys):
            app.keyPress = True
            app.selectedAxis = ['y-axis']
            #app.drawDottedLine = True
        if('z' in keys):
            app.keyPress = True
            app.selectedAxis = ['z-axis']
            #app.drawDottedLine = True


def cameraMove(app, mx, my):
    cameraDrag = [(mx-app.mx)*.005, (my-app.my)*.005]
    app.camera.yaw = app.initialYaw + cameraDrag[0]
    #app.camera.xAngle = app.initialxAngle - cameraDrag[1]*math.cos(app.camera.yaw )
    #app.camera.zAngle = app.initialzAngle + cameraDrag[1]*math.sin(app.camera.yaw )

def initializeCameraMove(app, mx, my):
    app.initialYaw = app.camera.yaw
    app.initialxAngle = app.camera.xAngle
    app.initialzAngle = app.camera.zAngle
    app.mx = mx
    app.my = my

def updateControls(app):
    if(app.selectedButton == "selectedMove.png"):
        app.move = True
        app.rotate = False
        app.scale = False
        app.boxSelect = False
    elif(app.selectedButton == 'SelectedScale.png'):
        app.move = False
        app.rotate = False
        app.scale = True
        app.boxSelect = False
    elif(app.selectedButton == 'PressedRotateIcon2.png'):
        app.move = False
        app.rotate = True
        app.scale = False
        app.boxSelect = False
    elif(app.selectedButton == 'selectedTransform.png'):
        app.move = True
        app.rotate = True
        app.scale = True
        app.boxSelect = False
    elif(app.selectedButton == 'selectedBoxSelect.png'):
        app.move = False
        app.rotate = False
        app.scale = False
        app.boxSelect = True


def controlButtonPressed(app, mx, my):   
    for button in app.controlButtons:
        if(button.hovered(mx, my)):
            if(isinstance(button, Picture)):
                button.url = button.ogPressed
            app.selectedButton = button
        else:
            if(15 <= mx <= 54 and 25+40 <= my <= 236+40):
                if(isinstance(button, Picture)):
                    button.url = button.ogURL

def controlButtonHovered(app, mx, my):
    app.hoveredButton = None
    for button in app.controlButtons:
        if(button.hovered(mx, my)):
            app.hoveredButton = button


def selectMesh(app, mx, my):
    if ableToDeselect(app, mx, my):
        app.selectedMeshIndex = None

    for i in range( len(app.meshList) ):
        if( selectedMesh(app, app.meshList[i], mx, my) ):
            app.selectedMeshIndex = i   

def drawDropDownMenus(app, mx, my):
    for b in app.dropDownButtons:
        if(b.hovered(mx, my)):
            b.drawDropDown = True

def getRidOfDropDownMenu(app, mx, my):
    for b in app.dropDownButtons:
        if(not b.dropDownHovered(mx, my) and b.drawDropDown):
            b.drawDropDown = False

def moveScaleRotateHovered(app, mx, my):
    foundButton = False
    i = 0
    app.selectedAxis = []
    for b in app.moveScaleRotateButtons:
        if(isinstance(b, button)):
            if(b.hovered(mx, my)):
                if(i == 0):
                    app.selectedAxis.append('x-axis')
                elif(i == 1):
                    app.selectedAxis.append('y-axis')
                elif(i == 2):
                    app.selectedAxis.append('z-axis')
                b.isHovered = True
                foundButton = True
            else:
                b.isHovered = False
            i += 1
    return foundButton


def ableToDeselect(app, mx, my):
    if(moveScaleRotateHovered(app, mx, my) ):
        return False
    
    for b in app.controlButtons:
        if(b.hovered(mx, my)):
            return False

    return True

def transformMoveScaleRotate(app, mx, my):
    if(app.move):
        if('x-axis' in app.selectedAxis):      
            app.meshList[app.selectedMeshIndex].xTrans = app.xTransInitial - (mx - app.mx)*.008*squareWave('cos', app.camera.yaw)
        if('y-axis' in app.selectedAxis):
            app.meshList[app.selectedMeshIndex].zTrans = app.zTransInitial - (mx - app.mx)*.008*squareWave('sin', app.camera.yaw)*-1
        if('z-axis' in app.selectedAxis):
            app.meshList[app.selectedMeshIndex].yTrans = app.yTransInitial + (my - app.my)*.008
    elif(app.scale):
        if('x-axis' in app.selectedAxis):      
            app.meshList[app.selectedMeshIndex].xScale = abs(app.xScaleInitial + (mx - app.mx)*.008 *squareWave('cos', app.camera.yaw)*-1)
            if(app.meshList[app.selectedMeshIndex].xScale < .1):
                app.meshList[app.selectedMeshIndex].yAngle = math.pi
        if('y-axis' in app.selectedAxis):
            app.meshList[app.selectedMeshIndex].zScale = abs(app.zScaleInitial + (mx - app.mx)*.008)
            if(app.meshList[app.selectedMeshIndex].zScale < .1):
                app.meshList[app.selectedMeshIndex].yAngle = math.pi
        if('z-axis' in app.selectedAxis):
            app.meshList[app.selectedMeshIndex].yScale = abs(app.yScaleInitial - (my - app.my)*.008)
            if(app.meshList[app.selectedMeshIndex].yScale < .1):
                app.meshList[app.selectedMeshIndex].zAngle += math.pi%6.24


def initiazliseMoveScaleRotate(app):
    if(app.selectedMeshIndex != None):
        app.xTransInitial = app.meshList[app.selectedMeshIndex].xTrans
        app.yTransInitial = app.meshList[app.selectedMeshIndex].yTrans
        app.zTransInitial = app.meshList[app.selectedMeshIndex].zTrans

        app.xScaleInitial = app.meshList[app.selectedMeshIndex].xScale
        app.yScaleInitial = app.meshList[app.selectedMeshIndex].yScale
        app.zScaleInitial = app.meshList[app.selectedMeshIndex].zScale

#========================================================
#========================================================
#                      USER INPUTS
#========================================================
#========================================================


def onMouseMove(app, mx, my):
    getRidOfDropDownMenu(app, mx, my)
    if(app.keyPress):
        app.mx = mx
        app.my = my
        app.keyPress = not app.keyPress
    if(app.drawDottedLine or app.grab):
        transformMoveScaleRotate(app, mx, my)
    controlButtonHovered(app, mx, my)

    app.movedMx = mx
    app.movedMy = my

def onMousePress(app, mx, my, button):
    app.drawDottedLine = False
    drawDropDownMenus(app, mx, my)
    initializeCameraMove(app, mx, my)
    initiazliseMoveScaleRotate(app)
    controlButtonPressed(app, mx, my) 
    if(button == 0):
        selectMesh(app, mx, my)   
    updateControls(app)       
    
    moveScaleRotateHovered(app, mx, my)    

def onMouseDrag(app, mx, my, button):
    if(button[0] == 1):
        cameraMove(app, mx, my)
    elif(button[0] == 0):
        app.draggedMx = mx
        app.draggedMy = my
        transformMoveScaleRotate(app, mx, my)
    
def onMouseRelease(app, mx, my):
    app.selectedAxis = []
    app.draggedMx = 0
    app.draggedMy = 0
    app.mx = 0
    app.my = 0

def onKeyRelease(app, key):
    app.keys = []

def redrawAll(app):    
    drawRect(0, 0, app.width, app.height, fill = rgb(30, 30, 30))
    drawBetterRect(app, 15, 25, app.width-30, app.height-20, rgb(60, 60, 60), 13)
    drawLabel(app.selectedButton, 700, 100, fill = 'white')
    drawLabel(app.hoveredButton, 700, 120, fill = 'white')
    drawGrid(app)
    for i in range(len(app.meshList)):
        draw3DShape(app, app.meshList[i], i)
        if(i == app.selectedMeshIndex):
            drawControl(app, i)

    drawWorldOrigin()
    drawControlButtons(app)
    drawLabel('User Perspective', 70, 70, fill = 'white', align = 'left', size = 12)
    drawLabel('(1) Scene Collection | Cube', 70, 90, fill = 'white', align = 'left', size = 12)
    if(app.drawDottedLine):
        startPoint = vectorSubtract(app.meshList[app.selectedMeshIndex].translateList, app.meshList[app.selectedMeshIndex].rotationPoint)
        startPoint[1] += 1
        midpoint = point(startPoint, app.camera).getTransformedPoints()
        drawLine(app.movedMx, app.movedMy, midpoint[0], midpoint[1], dashes = True , arrowStart = True)
    drawSelectedAxisLines(app)

    drawLabel(' '.join(app.keys), 100, app.height-100, fill = 'white', size = 30)
    drawDropDowns(app)
    if(app.boxSelect):
        drawLine(app.mx, app.my, app.draggedMx, app.my, fill = 'white', dashes = True)
        drawLine(app.mx, app.my, app.mx, app.draggedMy, fill = 'white', dashes = True)
        drawLine(app.draggedMx, app.draggedMy, app.draggedMx, app.my, fill = 'white', dashes = True)
        drawLine(app.mx, app.draggedMy, app.draggedMx, app.draggedMy, fill = 'white', dashes = True)
    drawControlDetails(app)    

def onStep(app):
    makeGrid(app)
    app.testMesh.initializeTransforms()
    updateMoveScaleRotateButtons(app)


def selectedMesh(app, mesh, mx, my):
    meshPoints = mesh.getTransformedPoints()[0]
    for tri in range( len(meshPoints) ):
        points = listToTupleList(meshPoints[tri].screenPoints)
        if( pointInPolygon(points, mx, my) ):
            return True
    return False


def main():
    runApp()

main()