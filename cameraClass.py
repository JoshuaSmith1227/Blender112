import math
from MatrixOperations import*
from MeshClass import*
from cmu_graphics import *

class Camera:
    def __init__(self, pos, target, up, name):
        self.normalizePoints = [[0, 0, 0, 0] for i in range(4)]

        self.cameraPos = pos
        self.target = target
        self.up = up
        self.lookDir = [0, 0, 1]

        self.yaw = 0
        self.xAngle = 0
        self.zAngle = 0

        self.name = name

        self.initializeConstants()
        self.lookAt()

    def __eq__(self, other):
        return self.name == other

    def lookAt(self):
        newForward = convertToUnitVector(vectorSubtract(self.target, self.cameraPos))
        a = vectorMultiply(newForward, dotProductNoCamera(self.up, newForward))
        newUp = convertToUnitVector(vectorSubtract(self.up, a))
        newRight = getNormalVector(newUp, newForward)

        viewMatrix = [
                [newRight[0], newRight[1], newRight[2], 0],
                [newUp[0], newUp[1], newUp[2], 0],
                [newForward[0], newForward[1], newForward[2], 0],
                [self.cameraPos[0], self.cameraPos[1], self.cameraPos[2], 1],
        ]
        
        return self.invertMatrix(viewMatrix)
    
    def updateLookDir(self):
        self.up = [0, 1, 0]
        self.target = [0, 0, 1]
        self.lookDir[0] += .01
        self.target = vectorAdd(self.target, self.lookDir)
        self.lookAt()


    def invertMatrix(self, L):
        M = [[0, 0, 0, 0] for i in range(4)]
        M[0][0], M[0][1], M[0][2], M[0][3] = L[0][0], L[1][0], L[2][0], 0
        M[1][0], M[1][1], M[1][2], M[1][3] = L[0][1], L[1][1], L[2][1], 0
        M[2][0], M[2][1], M[2][2], M[2][3] = L[0][2], L[1][2], L[2][2], 0
        M[3][0] = -(L[3][0] * L[0][0] + L[3][1] * L[1][0] + L[3][2] * L[2][0])
        M[3][1] = -(L[3][0] * L[0][1] + L[3][1] * L[1][1] + L[3][2] * L[2][1])
        M[3][2] = -(L[3][0] * L[0][2] + L[3][1] * L[1][2] + L[3][2] * L[2][2])
        M[3][3] = 1
        return M


    def getYawMatrix(self):
        self.yaw%= math.pi*2
        self.yawMatrix = [[0, 0, 0, 0] for i in range(4)]
        self.yawMatrix[0][0] = math.cos(self.yaw)
        self.yawMatrix[0][2] = math.sin(self.yaw)
        self.yawMatrix[2][0] = -1*math.sin(self.yaw)
        self.yawMatrix[1][1] = 1
        self.yawMatrix[2][2] = math.cos(self.yaw)
        self.yawMatrix[3][3] = 1
        return self.yawMatrix

    def getCameraXRotation(self):
        #self.xAngle%= math.pi*2
        self.cameraXRotation = [[0, 0, 0, 0] for i in range(4)]
        self.cameraXRotation[0][0] = 1
        self.cameraXRotation[1][1] = math.cos(self.xAngle*.5)
        self.cameraXRotation[1][2] = math.sin(self.xAngle*.5)
        self.cameraXRotation[2][1] = -1*math.sin(self.xAngle*.5)
        self.cameraXRotation[2][2] = math.cos(self.xAngle*.5)
        self.cameraXRotation[3][3] = 1
        return self.cameraXRotation
    
    def getCameraZRotation(self):
        #self.zAngle%= math.pi*2
        self.cameraZRotation = [[0, 0, 0, 0] for i in range(4)]
        self.cameraZRotation[0][0] = math.cos(self.zAngle)
        self.cameraZRotation[0][1] = math.sin(self.zAngle)
        self.cameraZRotation[1][0] = -1 * math.sin(self.zAngle)
        self.cameraZRotation[1][1] = math.cos(self.zAngle)
        self.cameraZRotation[2][2] = 1
        self.cameraZRotation[3][3] = 1
        return self.cameraZRotation

    def initializeConstants(self):
        self.far = 10000
        self.near = .1
        self.screenWidth = 3000
        self.screenHeight = 3000
        self.aspectRatio = self.screenWidth/self.screenHeight
        self.FOV = math.pi/3
        self.FOVrad = 1/math.tan(self.FOV)

    
    
    


    

        

