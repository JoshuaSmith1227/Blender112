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

    return [move, scale, rotate, transform, box, cursor, editorIcon]

def getDropDownButtons(app):
    modeButtonList = ['Object', 'Edit', 'Sculpt']
    editorMode = DropDown(getCurrentMode(app), 60, 20, app.imageStorage.objectModeSize[0]/1.3, app.imageStorage.objectModeSize[1]/1.3, app.imageStorage.objectEditSculpt, modeButtonList)
    MeshButtonList = ['Plane', 'cube', 'circle', 'UV Sphere', 'Ice Sphere', 'Cylinder', 'Cone', 'Torus', 'Grid', 'Monkey']
    addMesh = DropDown(None, 300, 20, 30, 15, app.imageStorage.meshSelect, MeshButtonList, 'Add')
    viewButtonList = ['Camera', 'Top', 'Bottom', 'Front', 'Back', 'Right', 'Left']
    view = DropDown(None, 250, 20, 30, 15, app.imageStorage.view, viewButtonList, 'view')
    selectButtonList = ['All', 'None', 'Invert', 'Box Select', 'Circle Select']
    select = DropDown(None, 200, 20, 35, 15, app.imageStorage.select, selectButtonList, 'select')
    return [editorMode, addMesh, view, select]

def getSliderButtons(app):
    sidePanel = slider('left', 20, app.sidePannelX, 0, app.width - app.sidePannelX, app.height)
    return [sidePanel]

def updateButtons(app, mx, my):
    ddButtons = None
    for dropDown in app.dropDownButtons:
        if(dropDown.dropDownHovered(mx, my)):
            ddButtons = dropDown.getDropDownButtons()
    
    if(ddButtons != None):
        app.controlButtons += ddButtons

def drawSliderButtons(app):
    for b in app.sliderButton:
        pass

def drawDropDowns(app):
    for b in app.dropDownButtons:
        if(b.url != None):
            drawImage(b.url, b.x, b.y, width = b.width, height = b.height)
        else:
            drawBetterRect(app, b.x, b.y, b.width, b.height, rgb(65, 65, 65), 3)
            drawLabel(b.name, b.x+b.width/2, b.y+b.height/2, fill = 'white')
        if(b.drawDropDown):
            drawImage(b.dropDownImage, b.x, b.y + b.height, width = getImageSize(b.dropDownImage)[0]/1.3, height = getImageSize(b.dropDownImage)[1]/1.3 )
            drawRect(b.x, b.y, b.width, b.height, fill = rgb(60, 81, 88), opacity = 30 )


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
    
        
