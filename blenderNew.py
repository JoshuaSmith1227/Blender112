from cmu_graphics import *
import math
from MeshClass import*
from buttonClass import*
from cameraClass import*
from otherFunctions import*
from drawFunctions import*
from UI_Functions import*

#   pointInPolygon: https://www.geeksforgeeks.org/how-to-check-if-a-given-point-lies-inside-a-polygon/
#   Graham Scan Algorithm (Drawing Mesh Outline): https://www.geeksforgeeks.org/convex-hull-using-graham-scan/
#   Merge Sort from CS academy 

# ====================================================
#              On App StartS
# ==================================================== 

def onAppStart(app):
    app.imageStorage = imageStorage()
    app.width = 1300
    app.height = 800
    app.cameraVector = [0, 0, 0]

    app.cameraPos = [0, 0, 10]
    app.worldPivot = [.5, .5, .5]

    app.camera = Camera(app.cameraPos, [0, 0, 0], [0, 1, 0], 'World Camera')
    app.gizmoCamera = Camera([0, 0, 1], [0, 0, 0], [0, 1, 0], 'Gizmo Camera')

    app.meshSpawnPoint = [0, 0, 0]
    
    app.testMesh = Mesh( chooseMesh('cube'), 'pyramid', app.camera, app.worldPivot)
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
    app.mostRecentMesh = 0
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
    app.outlinerMode = {
                'Wireframe': False,
                'Solid': True
    }

    app.vertexMode = {
                'Vertex': False,
                'Edge': False,
                'Face': True
    }

    app.sidePannelX = 3*app.width/4

    app.eyeButtons = []
    app.collectionButtons = []
    app.sideButtons = getControlButtons(app)
    app.dropDownButtons = getDropDownButtons(app)
    app.sliderButton = getSliderButtons(app)

    app.nonDropDownButtons = app.sideButtons + app.dropDownButtons
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
    app.drawHelp = False

    app.numOfCollectionItems = 13
    app.copyedMesh = None
    app.selectedface = []
    app.selectedTris = []
    updateCollectionButtons(app)
    updateEditButtons(app)


def onKeyHold(app, keys):
    app.keys = []
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

    if(app.selectedMeshIndex != None):
        if('1' in keys):
            app.meshList[app.selectedMeshIndex].xAngle += .1
        if('2' in keys):
            app.meshList[app.selectedMeshIndex].yAngle += .1
        if('3' in keys):
            app.meshList[app.selectedMeshIndex].zAngle += .1

    if('`' in keys and app.selectedMeshIndex != None):
        app.worldPivot = vectorAdd(app.meshList[app.selectedMeshIndex].getMidpoint(), app.meshList[app.selectedMeshIndex].translateList)

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
    elif('x' in keys and app.selectedMeshIndex != None):
        app.mostRecentMesh = None
        app.meshList.pop(app.selectedMeshIndex)
        print(app.collectionButtons)
        updateCollectionButtons(app)
        app.selectedMeshIndex = None

def onKeyPress(app, key): 
    if('v' == key and app.copyedMesh != None):
        copy = Mesh(app.copyedMesh.points, app.copyedMesh.name[:-4], app.camera, app.worldPivot)
        copy.xScale = app.copyedMesh.xScale
        copy.yScale = app.copyedMesh.yScale
        copy.zScale = app.copyedMesh.zScale
        app.meshList.append(copy)
        updateCollectionButtons(app)
    app.copyedMesh = None
    if('c' == key and app.selectedMeshIndex != None):
        app.copyedMesh = app.meshList[app.selectedMeshIndex]


def cameraMove(app, mx, my):
    cameraDrag = [(mx-app.mx)*.005, (my-app.my)*.005]
    app.camera.yaw = app.initialYaw + cameraDrag[0]
    #app.camera.xAngle = app.initialxAngle - cameraDrag[1]*math.cos(app.camera.yaw )
    #app.camera.zAngle = app.initialzAngle + cameraDrag[1]*math.sin(app.camera.yaw )

    app.gizmoCamera.yaw = app.camera.yaw
    #app.gizmoCamera.xAngle = app.camera.xAngle
    #app.gizmoCamera.zAngle = app.camera.zAngle
    #print(app.camera.yaw%6.24, app.camera.xAngle%6.24, app.camera.zAngle%6.24)

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

def helpButton(app):
    drawCircle(355, 26.5, 10, fill = rgb(60, 60, 60))
    drawLabel('?', 355, 26.5, fill = 'white')

    if(app.drawHelp):
        drawBetterRect(app, 355, 45, 400, 300, rgb(35, 35, 35), 5)
        drawLabel('Camera Pan', 360, 55, align = 'left', fill = 'white')
        drawLabel('Forward | Backword | Left | Right', 360, 55+30, align = 'left', fill = 'white' )
        drawLabel('Up | Down', 360, 55+50, align = 'left', fill = 'white' )

        drawLabel('Rescale', 360, 55+80, align = 'left', fill = 'white' )
        drawLabel('Grab', 360, 55+100, align = 'left', fill = 'white' )

        drawLabel('X-axis', 360, 55+130, align = 'left', fill = 'white' )
        drawLabel('Y-axis', 360, 55+150, align = 'left', fill = 'white' )
        drawLabel('Z-axis', 360, 55+170, align = 'left', fill = 'white' )

        drawLabel('Update World Pivot', 360, 55+200, align = 'left', fill = 'white' )

        drawLabel('Delete Mesh', 360, 55+230, align = 'left', fill = 'white')
        drawLabel('Copy Mesh', 360, 55+250, align = 'left', fill = 'white')
        drawLabel('Paste Mesh', 360, 55+270, align = 'left', fill = 'white')

        drawLabel('Scroll Wheel', 310+400, 55, align = 'right', fill = 'white')
        drawLabel('W | A | S | D', 310+400, 55+30, align = 'right', fill = 'white')
        drawLabel('E | Q', 310+335, 55+50, align = 'left', fill = 'white')

        drawLabel('R', 310+335, 55+80, align = 'left', fill = 'white')
        drawLabel('G', 310+335, 55+100, align = 'left', fill = 'white')

        drawLabel('X', 310+335, 55+130, align = 'left', fill = 'white')
        drawLabel('Y', 310+335, 55+150, align = 'left', fill = 'white')
        drawLabel('Z', 310+335, 55+170, align = 'left', fill = 'white')
        drawLabel('`', 310+335, 55+200, align = 'left', fill = 'white')
        drawLabel('X', 310+335, 55+230, align = 'left', fill = 'white')
        drawLabel('C', 310+335, 55+250, align = 'left', fill = 'white')
        drawLabel('V', 310+335, 55+270, align = 'left', fill = 'white')
        

def helpButtonPressed(app, mx, my):
    if(10 >= dist(355, mx, 26.5, my)):
        app.drawHelp = True

def controlButtonPressed(app, mx, my):   
    controlButtons = app.controlButtons[0:6]
    modeButtons = app.controlButtons[7:10]
    
    for button in app.controlButtons:
        if(button.hovered(mx, my)):
            if(isinstance(button, Picture)):               
                if(button in controlButtons):
                    for b in controlButtons:
                        b.reset()
                if(button in modeButtons):
                    for b in modeButtons:
                        b.reset()             
                button.switch()  
            if(button.name != None and button.name[-3:] == 'eye'):
                meshName = button.name[:-4]
                MeshIndex = app.meshList.index(meshName)
                app.meshList[MeshIndex].hidden = not app.meshList[MeshIndex].hidden
                
            app.selectedButton = button

    for button2 in app.editButtons:
        if(button2.hovered(mx, my)):
            for b in app.editButtons:
                b.reset()
            button2.switch()
            app.selectedButton = button2

    if( isinstance(app.selectedButton, Picture) ):
        if(app.selectedButton.name == 'vertexEdit'):
            app.vertexMode['Vertex'] = True
            app.vertexMode['Edge'] = False
            app.vertexMode['Face'] = False
        elif(app.selectedButton.name == 'edgeEdit'):
            app.vertexMode['Vertex'] = False
            app.vertexMode['Edge'] = True
            app.vertexMode['Face'] = False
        elif(app.selectedButton.name == 'faceEdit'):
            app.vertexMode['Vertex'] = False
            app.vertexMode['Edge'] = False
            app.vertexMode['Face'] = True

    if(app.selectedButton == 'Edit'):
        app.modeStates['Edit'] = True
        app.modeStates['Object'] = False
        app.modeStates['Sculpt'] = False
        app.editorMode.url = getCurrentMode(app)       
    elif(app.selectedButton == 'Object'):
        app.modeStates['Edit'] = False
        app.modeStates['Object'] = True
        app.modeStates['Sculpt'] = False
        app.editorMode.url = getCurrentMode(app)
    elif(app.selectedButton == 'Sculpt'):
        app.modeStates['Edit'] = False
        app.modeStates['Object'] = False
        app.modeStates['Sculpt'] = True
        app.editorMode.url = getCurrentMode(app)

    if(app.selectedButton == 'WireframeSelected.png'):
        app.outlinerMode['Wireframe'] = True
        app.outlinerMode['Solid'] = False
    elif(app.selectedButton == 'solidSelected2.png'):
        app.outlinerMode['Wireframe'] = False
        app.outlinerMode['Solid'] = True
            

def controlButtonHovered(app, mx, my):
    app.hoveredButton = None
    for button in app.controlButtons:
        if(button.hovered(mx, my)):
            app.hoveredButton = button

    for button in app.editButtons:
        if(button.hovered(mx, my)):
            app.hoveredButton = button

def resetSliderDragState(app, mx, my):
    app.sideButtons[10].isHovered = False
    for slider in app.sliderButton:
        slider.canDrag = False

def sliderHovered(app, mx, my):
    if(app.sideButtons[10].hovered(mx, my)):
        app.sideButtons[10].isHovered = True
        
    for slider in app.sliderButton:
        if( slider.hovered(mx, my) ):
            slider.canDrag = True

def dragSliders(app, mx, my):
    for slid in app.sliderButton:
        if(slid.canDrag):
            if(slid.control == 'left' or slid.control == 'right'):
                slid.width = slid.endPoint - mx
                slid.x = mx 
                if(slid == 'sidePannel'):
                    slider.updateAll(mx, None, slid.endPoint - mx, None)
                
                for i in range(len(app.collectionButtons)):
                    app.collectionButtons[i].x = mx
                    app.collectionButtons[i].width = slid.endPoint - mx
            elif(slid.control == 'top'):
                slid.height = slid.endPoint - my
                slid.y = my 

def selectMesh(app, mx, my):
    sortedList = painterSort(app.meshList)
    if ableToDeselect(app, mx, my):
        app.selectedMeshIndex = None
    for i in range( len(app.meshList) ):
        if(not sortedList[i].hidden):
            if( selectedMesh(app, app.meshList[i], mx, my) or app.selectedButton == app.meshList[i].name):
                app.selectedMeshIndex = i   
                app.mostRecentMesh = i

def drawDropDownMenus(app, mx, my):
    for b in app.dropDownButtons:
        if(b.hovered(mx, my)):
            b.drawDropDown = True

def getRidOfDropDownMenu(app, mx, my):
    for b in app.dropDownButtons:
        if(not b.dropDownHovered(mx, my) and b.drawDropDown):
            b.drawDropDown = False
            app.controlButtons = app.nonDropDownButtons[:] + app.collectionButtons + app.eyeButtons

def updateCollectionButtons(app):
    num = int(app.height/20)
    spacing = app.height/num
    start = 1
    app.collectionButtons = []
    app.eyeButtons = []
    for i in range(len(app.meshList)):
        app.eyeButtons.append( Picture(app.imageStorage.eye, app.width-30, app.sliderButton[0].y + spacing*(i + start+1), app.imageStorage.eyeSize[0]/1.3, app.imageStorage.eyeSize[1]/1.3, app.imageStorage.closedEye, f'{app.meshList[i].name}.eye'))
        app.collectionButtons.append( button(app.sliderButton[0].x, app.sliderButton[0].y + spacing*(i + start+1), app.sliderButton[0].width, spacing, app.meshList[i].name))

    app.controlButtons = app.nonDropDownButtons[:] + app.collectionButtons + app.eyeButtons

def drawEditButtons(app):
    if(app.modeStates['Edit']):
        drawRect(60, 50, 70, 25, fill = rgb(35, 35, 35), opacity = 50)

        for button in app.editButtons:
            drawImage(button.url, button.x, button.y, width = button.width, height = button.height)

def updateEditButtons(app):
    vertexEdit = Picture(app.imageStorage.vertexEdit, 65, 50, app.imageStorage.vertexEditSize[0]/1.15, app.imageStorage.vertexEditSize[1]/1.15, app.imageStorage.vertEditS, 'vertexEdit') 
    edgeEdit = Picture(app.imageStorage.edgeEdit, 85, 50, app.imageStorage.edgeEditSize[0]/1.15, app.imageStorage.edgeEditSize[1]/1.15, app.imageStorage.edgeEdits, 'edgeEdit') 
    faceEdit = Picture(app.imageStorage.faceEdit, 105, 50, app.imageStorage.faceEditSize[0]/1.2, app.imageStorage.faceEditSize[1]/1.2, app.imageStorage.faceEdisS, 'faceEdit') 

    if(app.modeStates['Edit']):
        app.editButtons = [vertexEdit, edgeEdit, faceEdit]
    else:
        app.editButtons = []

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
    for b in app.editButtons:
        if(b.hovered(mx, my)):
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
        if('x-axis' in app.selectedAxis and 'y-axis' in app.selectedAxis and 'z-axis' in app.selectedAxis):
            startPoint = vectorSubtract(app.meshList[app.selectedMeshIndex].translateList, app.meshList[app.selectedMeshIndex].rotationPoint)
            startPoint[1] += 1
            u = vectorMultiply( convertToUnitVector([app.xScaleInitial, app.yScaleInitial, app.zScaleInitial]), .05)
            app.meshList[app.selectedMeshIndex].xScale = abs(app.xScaleInitial + (mx - app.mx)*u[0])
            app.meshList[app.selectedMeshIndex].yScale = abs(app.yScaleInitial + (mx - app.mx)*u[1])
            app.meshList[app.selectedMeshIndex].zScale = abs(app.zScaleInitial + (mx - app.mx)*u[2])
        if('x-axis' in app.selectedAxis and len(app.selectedAxis) != 3):      
            app.meshList[app.selectedMeshIndex].xScale = abs(app.xScaleInitial + (mx - app.mx)*.008 *squareWave('cos', app.camera.yaw)*-1)
            if(app.meshList[app.selectedMeshIndex].xScale < .1):
                app.meshList[app.selectedMeshIndex].yAngle = math.pi
        if('y-axis' in app.selectedAxis and len(app.selectedAxis) != 3):
            app.meshList[app.selectedMeshIndex].zScale = abs(app.zScaleInitial + (mx - app.mx)*.008)
            if(app.meshList[app.selectedMeshIndex].zScale < .1):
                app.meshList[app.selectedMeshIndex].yAngle = math.pi
        if('z-axis' in app.selectedAxis and len(app.selectedAxis) != 3):
            app.meshList[app.selectedMeshIndex].yScale = abs(app.yScaleInitial - (my - app.my)*.008)
            if(app.meshList[app.selectedMeshIndex].yScale < .1):
                app.meshList[app.selectedMeshIndex].zAngle += math.pi%6.24

def getSign(m, n):
    if(n-m > 0): return 1
    elif(n-m < 0): return -1

def initiazliseMoveScaleRotate(app):
    if(app.selectedMeshIndex != None):
        app.xTransInitial = app.meshList[app.selectedMeshIndex].xTrans
        app.yTransInitial = app.meshList[app.selectedMeshIndex].yTrans
        app.zTransInitial = app.meshList[app.selectedMeshIndex].zTrans

        app.xScaleInitial = app.meshList[app.selectedMeshIndex].xScale
        app.yScaleInitial = app.meshList[app.selectedMeshIndex].yScale
        app.zScaleInitial = app.meshList[app.selectedMeshIndex].zScale

def selectFace(app, mx, my):
    if(app.selectedMeshIndex != None and app.modeStates['Edit']):
        for face in app.meshList[app.selectedMeshIndex].faces:
            f = set()
            for tri in app.meshList[app.selectedMeshIndex].faces[face]:
                ax, ay = tri.screenPoints[0], tri.screenPoints[1]
                bx, by = tri.screenPoints[2], tri.screenPoints[3]
                cx, cy = tri.screenPoints[4], tri.screenPoints[5]
                f.add((ax, ay))
                f.add((bx, by))
                f.add((cx, cy))

            finalFace = clockSort(sorted(f)) 
            
            if(pointInPolygon(finalFace, mx, my)):
                app.selectedface = finalFace
                app.selectedTris = app.meshList[app.selectedMeshIndex].faces[face]
                
                

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

def changeView(app, button):
    if(button == 'Bottom'):
        app.camera.xAngle = math.pi
        app.gizmoCamera.xAngle = math.pi
        app.camera.yaw = 0
        app.gizmoCamera.yaw = 0
        app.selectedButton = None
    elif(button == 'Top'):
        app.camera.yaw = 0
        app.camera.xAngle = -math.pi
        app.gizmoCamera.xAngle = -math.pi
        app.gizmoCamera.yaw = 0
        app.selectedButton = None
    elif(button == 'Front'):
        app.camera.xAngle = 0
        app.camera.yaw = math.pi/2
        app.gizmoCamera.yaw = math.pi/2
        app.gizmoCamera.xAngle = 0
        app.selectedButton = None
    elif(button == 'Back'):
        app.camera.xAngle = 0
        app.camera.yaw = -math.pi/2
        app.gizmoCamera.yaw = -math.pi/2
        app.gizmoCamera.xAngle = 0
        app.selectedButton = None
    elif(button == 'Right'):
        app.camera.xAngle = 0
        app.camera.yaw = math.pi
        app.gizmoCamera.yaw = math.pi
        app.gizmoCamera.xAngle = 0
        app.selectedButton = None
    elif(button == 'Left'):
        app.camera.xAngle = 0
        app.camera.yaw = -math.pi
        app.gizmoCamera.yaw = -math.pi
        app.gizmoCamera.xAngle = 0
        app.selectedButton = None


def onMousePress(app, mx, my, button):
    if(app.vertexMode['Face']):
        selectFace(app, mx, my)
    if(app.selectedButton == 'Edit'):
        updateEditButtons(app)
    app.drawHelp = False
    app.initArrowPos = app.sideButtons[10].x
    sliderHovered(app, mx, my)
    helpButtonPressed(app, mx, my)
    app.drawDottedLine = False
    drawDropDownMenus(app, mx, my)
    initializeCameraMove(app, mx, my)
    initiazliseMoveScaleRotate(app)
    controlButtonPressed(app, mx, my) 
    if(button == 0):
        selectMesh(app, mx, my)   
    updateControls(app)       
    updateButtons(app, mx, my)
    moveScaleRotateHovered(app, mx, my)   
    if( spawnNewMesh(app, app.selectedButton) ):
        updateCollectionButtons(app)
    changeView(app, app.selectedButton)
    

def onMouseDrag(app, mx, my, button):
    if(button[0] == 1):
        cameraMove(app, mx, my)  
    elif(button[0] == 0):
        dragSliders(app, mx, my)
        sliderHovered(app, mx, my)
        updateTransformPanel(app, mx, my)
        updateControlButtonPos(app)
        app.draggedMx = mx
        app.draggedMy = my
        transformMoveScaleRotate(app, mx, my)
    
def onMouseRelease(app, mx, my):
    resetSliderDragState(app, mx, my)
    app.selectedAxis = []
    app.draggedMx = 0
    app.draggedMy = 0
    app.mx = 0
    app.my = 0

def onKeyRelease(app, key):
    pass

def redrawAll(app):    
    drawRect(0, 0, app.width, app.height, fill = 'black')
    drawBetterRect(app, 10, 20, app.sliderButton[0].x- 25, app.height-30, rgb(60, 60, 60), 8)
    
    drawRect(0, 0, app.width, 50, fill = rgb(35, 35, 35), opacity = 50)
    drawLabel(app.selectedButton, 700, 100, fill = 'white')
    drawLabel(app.hoveredButton, 700, 120, fill = 'white')
    drawGrid(app)
    selected = None

    sortedList = painterSort(app.meshList)
    if(app.selectedMeshIndex != None and not app.outlinerMode['Wireframe'] and not sortedList[app.selectedMeshIndex].hidden):
        drawOutline(app.meshList[app.selectedMeshIndex].getTransformedPoints()[1])
        
    for i in range(len(app.meshList)):
        if(not sortedList[i].hidden):
            draw3DShape(app, sortedList[i], i)
        if(i == app.selectedMeshIndex):
            selected = i    
        
        
    if(selected != None):
        drawControl(app, selected)

    drawWorldOrigin()
    drawControlButtons(app)
    drawTransformPanel(app)
    
    if(app.mostRecentMesh != None):
        if(app.editButtons == []):
            drawLabel('User Perspective', 70, 70, fill = 'white', align = 'left', size = 12)
            drawLabel(f'(1) Scene Collection | {app.meshList[app.mostRecentMesh]}', 70, 90, fill = 'white', align = 'left', size = 12)
        else:
            drawLabel('User Perspective', 70, 105, fill = 'white', align = 'left', size = 12)
            drawLabel(f'(1) Scene Collection | {app.meshList[app.mostRecentMesh]}', 70, 125, fill = 'white', align = 'left', size = 12)

    if(app.drawDottedLine):
        startPoint = vectorSubtract(app.meshList[app.selectedMeshIndex].translateList, app.meshList[app.selectedMeshIndex].rotationPoint)
        startPoint[1] += 1
        midpoint = point(startPoint, app.camera).getTransformedPoints()
        drawLine(app.movedMx, app.movedMy, midpoint[0], midpoint[1], dashes = True , arrowStart = True)

    drawSelectedAxisLines(app)
    drawSliderButtons(app)
    drawLabel(f'{' '.join(app.keys)}', 100, app.height-100, fill = 'white', size = 30)
    drawEditButtons(app)
    drawDropDowns(app)
    
    if(app.boxSelect):
        drawLine(app.mx, app.my, app.draggedMx, app.my, fill = 'white', dashes = True)
        drawLine(app.mx, app.my, app.mx, app.draggedMy, fill = 'white', dashes = True)
        drawLine(app.draggedMx, app.draggedMy, app.draggedMx, app.my, fill = 'white', dashes = True)
        drawLine(app.mx, app.draggedMy, app.draggedMx, app.draggedMy, fill = 'white', dashes = True)
    drawControlDetails(app)    
    drawRotationGizmo(app)
    helpButton(app)

def onStep(app):
    makeGrid(app)
    if(app.selectedMeshIndex != None):
        app.meshList[app.selectedMeshIndex].initializeTransforms()
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