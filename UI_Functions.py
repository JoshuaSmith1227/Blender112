from cmu_graphics import *
import math
from MeshClass import*
from buttonClass import*
from cameraClass import*
from otherFunctions import*
from drawFunctions import*

class imageStorage:
    def __init__(self):
        self.moveIcon = "C:\\Users\\Owner\\Downloads\\blenderIcons\\Move.png"
        self.pressedMove = "C:\\Users\\Owner\\Downloads\\blenderIcons\\selectedMove.png"
        self.moveSize = getImageSize(self.moveIcon)

        self.scaleIcon = "C:\\Users\\Owner\\Downloads\\blenderIcons\\Scale.png"
        self.pressedScale = "C:\\Users\\Owner\\Downloads\\blenderIcons\\SelectedScale.png"
        self.scaleSize = getImageSize(self.scaleIcon)

        self.rotateIcon = "C:\\Users\\Owner\\Downloads\\blenderIcons\\rotate.png"
        self.pressedRotate = "C:\\Users\\Owner\\Downloads\\blenderIcons\\PressedRotateIcon2.png"
        self.rotateSize = getImageSize(self.rotateIcon)

        self.transformIcon = "C:\\Users\\Owner\\Downloads\\blenderIcons\\transform.png"
        self.pressedTransform = "C:\\Users\\Owner\Downloads\\blenderIcons\\selectedTransform.png"
        self.transformSize = getImageSize(self.transformIcon)

        self.boxIcon = "C:\\Users\\Owner\\Downloads\\blenderIcons\\boxIcon2.png"
        self.pressedBoxIcon = "C:\\Users\\Owner\\Downloads\\blenderIcons\\selectedBoxSelect.png"
        self.boxSize = getImageSize(self.boxIcon)

        self.cursorIcon = "C:\\Users\\Owner\\Downloads\\blenderIcons\\3Dcursor.png"
        self.pressedCursorIcon = "C:\\Users\\Owner\\Downloads\\blenderIcons\\selected3Dcurson.png"
        self.cursorSize = getImageSize(self.cursorIcon)

        self.meshWindow = "C:\\Users\\Owner\\Downloads\\blenderIcons\\MeshWindow.png"
        self.meshWindowSize = getImageSize(self.meshWindow)

        self.modes = "C:\\Users\\Owner\\Downloads\\blenderIcons\\ObjectEditSculptIcon.png"
        self.modeSize = getImageSize(self.modes)

        self.editorTypeIcon = "C:\\Users\\Owner\\Downloads\\blenderIcons\\EditorTypeIcon.png"
        self.editorTypeSize = getImageSize(self.editorTypeIcon)

        self.editModeIcon = "C:\\Users\\Owner\\Downloads\\blenderIcons\\EditModeIcon.png"
        self.editModeSize = getImageSize(self.editModeIcon)

        self.objectModeIcon = "C:\\Users\\Owner\\Downloads\\blenderIcons\\ObjectModeIcon.png"
        self.objectModeSize = getImageSize(self.objectModeIcon)

        self.sculptModeIcon = "C:\\Users\\Owner\\Downloads\\blenderIcons\\SculptModeIcon.png"
        self.sculptModeSize = getImageSize(self.sculptModeIcon)

        self.objectEditSculpt = "C:\\Users\\Owner\\Downloads\\blenderIcons\\ObjectEditSculptIcon.png"
        self.objectEditSculptSize = getImageSize(self.objectEditSculpt)

        self.meshSelect = "C:\\Users\\Owner\\Downloads\\blenderIcons\\MeshSelect.png"
        self.meshSelectSize = getImageSize(self.meshSelect)

        self.select = "C:\\Users\\Owner\\Downloads\\blenderIcons\\Select2.png"
        self.selectSize = getImageSize(self.select)

        self.view = "C:\\Users\\Owner\\Downloads\\blenderIcons\\View.png"
        self.viewSize = getImageSize(self.view)

        self.solid = "C:\\Users\\Owner\\Downloads\\blenderIcons\\SolidMode.png"
        self.solidSize = getImageSize(self.solid)
        self.solidSelected = "C:\\Users\\Owner\\Downloads\\blenderIcons\\solidSelected2.png"

        self.wireframe = "C:\\Users\\Owner\\Downloads\\blenderIcons\\WireframeMode.png"
        self.wireframeSize = getImageSize(self.wireframe)
        self.wireframeSelected = "C:\\Users\\Owner\\Downloads\\blenderIcons\\WireframeSelected.png"

        self.xRay = "C:\\Users\\Owner\\Downloads\\blenderIcons\\XrayMode.png"
        self.xRaySize = getImageSize(self.xRay)
        self.xRaySelected = "C:\\Users\\Owner\\Downloads\\blenderIcons\\XraySelected.png"

        self.vertex = "C:\\Users\\Owner\\Downloads\\blenderIcons\\vertexIcon.png"
        self.vertexSize = getImageSize(self.vertex)

        self.meshIcon = "C:\\Users\\Owner\\Downloads\\blenderIcons\\meshIcon.png"
        self.meshIconSize = getImageSize(self.meshIcon)

        self.collectionIcon = "C:\\Users\\Owner\\Downloads\\blenderIcons\\collectionIcon.png"
        self.collectionSize = getImageSize(self.collectionIcon)

        self.arrow = "C:\\Users\\Owner\\Downloads\\blenderIcons\\arrow.png"
        self.arrowSize = getImageSize(self.arrow)

        self.eye = "C:\\Users\\Owner\\Downloads\\blenderIcons\\open Eye.png"
        self.eyeSize = getImageSize(self.eye)
        self.closedEye = "C:\\Users\\Owner\\Downloads\\blenderIcons\\closed Eye.png"
        self.closedEyeSize = getImageSize(self.closedEye)



def getControlButtons(app):
    dy = 40
    move = Picture(app.imageStorage.moveIcon, 15, 100+dy, 40, 32, app.imageStorage.pressedMove)
    scale = Picture(app.imageStorage.scaleIcon, 15, 133+dy, app.imageStorage.scaleSize[0]/1.4, app.imageStorage.scaleSize[1]/1.35, app.imageStorage.pressedScale)
    rotate = Picture(app.imageStorage.rotateIcon, 15, 168+dy, app.imageStorage.rotateSize[0]/1.5, app.imageStorage.rotateSize[1]/1.45, app.imageStorage.pressedRotate)
    transform = Picture(app.imageStorage.transformIcon, 15, 203+dy, app.imageStorage.transformSize[0]/1.3, app.imageStorage.transformSize[1]/1.3, app.imageStorage.pressedTransform)
    box = Picture(app.imageStorage.boxIcon, 15, 25+dy, app.imageStorage.boxSize[0]/.85, app.imageStorage.boxSize[1]/.9, app.imageStorage.pressedBoxIcon)
    cursor = Picture(app.imageStorage.cursorIcon, 16, 60+dy, app.imageStorage.cursorSize[0]/.8, app.imageStorage.cursorSize[1]/.9, app.imageStorage.pressedCursorIcon)
    
    editorIcon = Picture(app.imageStorage.editorTypeIcon, 16, 20, app.imageStorage.editorTypeSize[0]/1.3, app.imageStorage.editorTypeSize[1]/1.3, app.imageStorage.editorTypeIcon)
    app.currentMode = Picture(getCurrentMode(app), 60, 20, app.imageStorage.objectModeSize[0]/1.3,app.imageStorage.objectModeSize[1]/1.3, getCurrentMode(app))
    
    solid = Picture(app.imageStorage.solid, app.sidePannelX-50, 20, app.imageStorage.solidSize[0]/1.3, app.imageStorage.solidSize[1]/1.3, app.imageStorage.solidSelected)
    wireframe = Picture(app.imageStorage.wireframe, app.sidePannelX-30, 20, app.imageStorage.wireframeSize[0]/1.3, app.imageStorage.wireframeSize[1]/1.3, app.imageStorage.wireframeSelected)
    xRay = Picture(app.imageStorage.xRay, app.sidePannelX-90, 20, app.imageStorage.xRaySize[0]/1.3, app.imageStorage.xRaySize[1]/1.2, app.imageStorage.xRaySelected)

    arrow = Picture(app.imageStorage.arrow, app.sidePannelX-20, 80, app.imageStorage.arrowSize[0], app.imageStorage.arrowSize[1], app.imageStorage.arrow)

    return [move, scale, rotate, transform, box, cursor, editorIcon, solid, wireframe, xRay, arrow]

def getDropDownButtons(app):
    modeButtonList = ['Object', 'Edit', 'Sculpt']
    app.editorMode = DropDown(getCurrentMode(app), 60, 20, app.imageStorage.objectModeSize[0]/1.3, app.imageStorage.objectModeSize[1]/1.3, app.imageStorage.objectEditSculpt, modeButtonList)
    MeshButtonList = ['Plane', 'cube', 'circle', 'UV Sphere', 'Ice Sphere', 'Cylinder', 'Cone', 'Torus', 'Grid', 'Monkey']
    addMesh = DropDown(None, 300, 20, 30, 15, app.imageStorage.meshSelect, MeshButtonList, 'Add')
    viewButtonList = ['Camera', 'Top', 'Bottom', 'Front', 'Back', 'Right', 'Left']
    view = DropDown(None, 250, 20, 30, 15, app.imageStorage.view, viewButtonList, 'view')
    selectButtonList = ['All', 'None', 'Invert', 'Box Select', 'Circle Select']
    select = DropDown(None, 200, 20, 35, 15, app.imageStorage.select, selectButtonList, 'select')
    return [app.editorMode, addMesh, view, select]


def updateControlButtonPos(app):
    buttons = app.controlButtons[7:10]
    for i in range(len(buttons)):
        if(i == 2):
            buttons[i].x = app.sliderButton[0].x - 20 * (i+1) - 20
        else:
            buttons[i].x = app.sliderButton[0].x - 20 * (i+1) -10

def getSliderButtons(app):
    sidePanel = slider( app.sidePannelX, 0, app.width - app.sidePannelX, app.height,'left', 20, rgb(60, 60, 60), 'sidePannel')
    modifierPanel = slider( app.sidePannelX, app.height/3, app.width - app.sidePannelX, app.height - app.height/3 ,'top', 20, rgb(45, 45, 45), 'modifierPanel')
    collectionPanel = slider( app.sidePannelX, 0, app.width - app.sidePannelX, app.height/3 ,'top', 20, rgb(45, 45, 45), 'collectionPanel')
    return [sidePanel, collectionPanel, modifierPanel]

def updateTransformPanel(app, mx, my):
    arrow = app.sideButtons[10]
    if(arrow.isHovered):
        if(mx <= app.sliderButton[0].x-20):
            arrow.x = mx
            arrow.open = True
        else:
            arrow.x = app.sliderButton[0].x - 20

    if(not arrow.open):
        arrow.x = app.sliderButton[0].x - 20

    if(app.sliderButton[0].x - (arrow.x+arrow.width) - 25 < 0):
        arrow.open = False
        arrow.x = app.sliderButton[0].x - 20

def drawTransformPanel(app):
    arrow = app.sideButtons[10]
    if(app.sliderButton[0].x - (arrow.x+arrow.width) - 20 > 0 and arrow.open):
        drawBetterRect(app, arrow.x+arrow.width, arrow.y, app.sliderButton[0].x - arrow.x - 10, 330, rgb(55, 55, 55), 3)
        drawLabel('Transform', arrow.x +25, arrow.y+10, fill = 'white', align = 'left')

        start = [arrow.y+60, arrow.y+ 150, arrow.y + 240]
        axis = ['X', 'Y', 'Z']
        mesh = app.meshList[app.mostRecentMesh]
        labels = ['Location:', 'Rotation', 'Scale:']
        units = ['m', '°', '']
        transforms = [[mesh.xTrans, mesh.yTrans, mesh.zTrans], [rTod(mesh.xAngle)%360, rTod(mesh.yAngle)%360, rTod(mesh.zAngle)%360], [mesh.xScale, mesh.yScale, mesh.zScale]]
        for j in range(len(start)):
            drawLabel(labels[j], arrow.x+25, start[j]-13, align = 'left', fill = 'white')
            for i in range(3):   
                height = 23
                width = (app.sliderButton[0].x - (arrow.x + arrow.width))/1.2
                drawRect(arrow.x+25, start[j] + height*i, width, height-2, fill = rgb(70, 70, 70))
                drawLabel(axis[i], arrow.x + 30, start[j] + height*i+10, fill = 'white', align = 'left')
                drawLabel(f'{pythonRound(transforms[j][i], 2)} {units[j]}', arrow.x + width+18, start[j] + height*i+10, fill = 'white', align = 'right')
                
def rTod(angle):
    return (angle*360)/(math.pi*2)    

def updateButtons(app, mx, my):
    ddButtons = None
    for dropDown in app.dropDownButtons:
        if(dropDown.dropDownHovered(mx, my)):
            ddButtons = dropDown.getDropDownButtons()
    
    if(ddButtons != None):
        app.controlButtons += ddButtons

def drawSliderButtons(app):
    for b in app.sliderButton:
        num = int(app.height/20)
        spacing = app.height/num
        start = 1
        if(b == 'sidePannel'):
            drawRect(b.x-5, b.y, b.width, b.height, fill = rgb(30, 30, 30))
            drawRect(b.x, b.y, b.width, b.height, fill = b.color)

        if(b == 'collectionPanel'):
            for i in range(num):                            
                if(i == 0):
                    drawBetterRect(app, b.x+3, b.y + spacing*(i + start), b.width, spacing, rgb(45, 45, 45), 3)
                elif(i == num-1):
                    drawBetterRect(app, b.x+3, b.y + spacing*(i + start), b.width, spacing, rgb(45, 45, 45), 3)   
                elif(i % 2 == 0):
                    drawRect(b.x, b.y + spacing*(i + start), b.width, spacing, fill = rgb(45, 45, 45))
                elif(i % 2 == 1):
                    drawRect(b.x, b.y + spacing*(i + start), b.width, spacing, fill = rgb(50, 50, 50))
     
        if(b == 'modifierPanel'):
            drawRect(b.x-5, b.y-2, b.width+5, b.height, fill = rgb(30, 30, 30))
            drawRect(b.x, b.y, b.width, b.height, fill = b.color)

    
    drawImage(app.imageStorage.collectionIcon, app.sliderButton[0].x+10, app.sliderButton[0].y+20, width = app.imageStorage.collectionSize[0]/1.3, height = app.imageStorage.collectionSize[1]/1.3)
    drawLabel('Scene Collection', app.sliderButton[0].x+45, app.sliderButton[0].y+28, align = 'left', fill = 'white') 
    drawLine(app.sliderButton[0].x+20, app.sliderButton[0].y+40, app.sliderButton[0].x+20, app.sliderButton[0].y+40 + len(app.collectionButtons)*(spacing), fill = 'white', lineWidth = .5)
    for i in range(len(app.collectionButtons)):
        x1 = app.collectionButtons[i].x+75 + (app.collectionButtons[i].width)/20
        x2 = app.collectionButtons[i].x+30 + (app.collectionButtons[i].width)/20

        eye = app.eyeButtons[i]
        drawImage(eye.url, eye.x, eye.y, width = eye.width, height = eye.height)

        drawImage(app.imageStorage.meshIcon, x2, app.collectionButtons[i].y, width = app.imageStorage.meshIconSize[0]/1.3, height = app.imageStorage.meshIconSize[1]/1.3)
        drawLabel(app.collectionButtons[i].name, x1, app.collectionButtons[i].y+11, fill = 'white', align = 'left')    
        drawImage(app.imageStorage.vertex, x1 + len(app.collectionButtons[i].name)*8, app.collectionButtons[i].y, width = app.imageStorage.vertexSize[0]/1.35, height = app.imageStorage.vertexSize[1]/1.35)
        if(app.selectedMeshIndex != None):
            if( app.meshList[app.selectedMeshIndex].name == app.collectionButtons[i].name):
                drawRect(app.collectionButtons[i].x, app.collectionButtons[i].y, app.collectionButtons[i].width, app.collectionButtons[i].height, fill = rgb(16, 42, 115), opacity = 30 )

def drawDropDowns(app):
    for b in app.dropDownButtons:
        if(b.url != None):
            drawImage(b.url, b.x, b.y, width = b.width, height = b.height)
        else:
            drawBetterRect(app, b.x, b.y, b.width, b.height, rgb(65, 65, 65), 3)
            drawLabel(b.name, b.x+b.width/2, b.y+b.height/2, fill = 'white')
        if(b.drawDropDown):
            drawImage(b.dropDownImage, b.x, b.y + b.height, width = getImageSize(b.dropDownImage)[0]/1.3, height = getImageSize(b.dropDownImage)[1]/1.3 )
            drawRect(b.x, b.y, b.width, b.height, fill = rgb(16, 42, 115), opacity = 50 )


def updateMoveScaleRotateButtons(app):
    if(app.selectedMeshIndex != None):
        points = getMoveScaleRotatePoints(app, app.selectedMeshIndex)
        xControl = button(points[0][1][0]-10, points[0][1][1]-10, 20, 20)
        yControl = button(points[1][1][0]-10, points[1][1][1]-10, 20, 20)
        zControl = button(points[2][1][0]-10, points[2][1][1]-10, 20, 20)
        app.moveScaleRotateButtons = [xControl, yControl, zControl]

def drawControlButtons(app):
    for button in app.controlButtons:
        if(isinstance(button, Picture)):
            drawImage(button.url, button.x, button.y, width = button.width, height = button.height)
        elif(isinstance(button, DropDown)):
            drawBetterRect(app, button.x, button.y, button.width, button.height, rgb(40, 40, 40), 3)
        else:
            drawBetterRect(app, button.x, button.y, button.width, button.height, rgb(50, 50, 50), 3)
            drawLabel(button.name, button.x+button.width/2, button.y+button.height/2, fill = 'white')
        

def drawControlDetails(app):
    if(app.hoveredButton != None):
        drawRect(app.hoveredButton.x, app.hoveredButton.y, app.hoveredButton.width, app.hoveredButton.height, fill = rgb(60, 60, 60), opacity = 30)

    if(app.hoveredButton == "Move.png"):
        drawBetterRect(app, app.hoveredButton.x+45, app.hoveredButton.y+7, 50, 20, rgb(30, 30, 30), 3)
        drawLabel('Move', app.hoveredButton.x+70, app.hoveredButton.y+15, fill = 'white', size = 10)
    elif(app.hoveredButton == 'Scale.png'):
        drawBetterRect(app, app.hoveredButton.x+45, app.hoveredButton.y+7, 50, 20, rgb(30, 30, 30), 3)
        drawLabel('Scale', app.hoveredButton.x+70, app.hoveredButton.y+15, fill = 'white', size = 10)
    elif(app.hoveredButton == 'rotate.png'):
        drawBetterRect(app, app.hoveredButton.x+45, app.hoveredButton.y+7, 50, 20, rgb(30, 30, 30), 3)
        drawLabel('Rotate', app.hoveredButton.x+70, app.hoveredButton.y+15, fill = 'white', size = 10)
    elif(app.hoveredButton == 'transform.png'):
        drawBetterRect(app, app.hoveredButton.x+45, app.hoveredButton.y+7, 50, 20, rgb(30, 30, 30), 3)
        drawLabel('Transform', app.hoveredButton.x+70, app.hoveredButton.y+15, fill = 'white', size = 10)
    elif(app.hoveredButton == '3Dcursor.png'):
        drawBetterRect(app, app.hoveredButton.x+45, app.hoveredButton.y+7, 50, 20, rgb(30, 30, 30), 3)
        drawLabel('Cursor', app.hoveredButton.x+70, app.hoveredButton.y+15, fill = 'white', size = 10)
    elif(app.hoveredButton == 'boxIcon2.png'):
        drawBetterRect(app, app.hoveredButton.x+45, app.hoveredButton.y+7, 50, 20, rgb(30, 30, 30), 3)
        drawLabel('Select Box', app.hoveredButton.x+70, app.hoveredButton.y+15, fill = 'white', size = 10)
    
        
