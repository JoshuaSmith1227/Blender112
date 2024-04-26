from cmu_graphics import *
import math
from MatrixOperations import*
from cameraClass import*
from otherFunctions import*

class Mesh:
    meshCounts = dict()
    def __init__(self, points, name, camera, worldPivot):
        self.normalizePoints = [[0, 0, 0, 0] for i in range(4)]
        self.normalizeRotationX = [[0, 0, 0, 0] for i in range(4)]
        self.normalizeRotationY = [[0, 0, 0, 0] for i in range(4)]
        self.normalizeRotationZ = [[0, 0, 0, 0] for i in range(4)] 
        self.normalizeRescale = [[0, 0, 0, 0] for i in range(4)]

        self.cameraVector = camera.cameraPos
        self.camera = camera

        self.points = points

        if(name not in Mesh.meshCounts):
            Mesh.meshCounts[name] = 1
        else:
            Mesh.meshCounts[name] += 1
        
        self.name = f'{name}.00{str(Mesh.meshCounts[name])}'

        self.xTrans = 0
        self.yTrans = 1
        self.zTrans = 0
        self.translateList = [self.xTrans, self.yTrans, self.zTrans]

        self.xAngle = 0
        self.yAngle = 0
        self.zAngle = 0

        self.xScale = 1
        self.yScale = 1
        self.zScale = 1

        self.lightingVector = [0, 0, -1]
        self.rotationPoint = self.getMidpoint()

        self.worldPivot = worldPivot
                
        self.initializeConstants()
        self.initializeTransforms()

        self.hidden = False
    
    def __repr__(self):
        return self.name
    
    def __eq__(self, other):
        return self.name == other
    
    def translate(self, point, x, y, z):
        return [point[0] + x, point[1] + y, point[2] + z]

    def getMidpoint(self):
        avgX = 0
        avgY = 0
        avgZ = 0
        counter = 0
        for tri in self.points:
            for point in tri:
                avgX += point[0]
                avgY += point[1]
                avgZ += point[2]
                counter += 1
        return [avgX/counter, avgY/counter, avgZ/counter]

    def getTransformedPoints(self):
        self.frontTris = []
        self.hiddenTris = []

        for triangle in self.points:
            xT = 0
            yT = 0
            zT = 0
            self.worldPivot = vectorAdd(app.worldPivot, self.rotationPoint)
            # Translate to new Origin ===========================================================
            translatedToRotationPointP1 = self.translate(triangle[0], -self.rotationPoint[0], -self.rotationPoint[1], -self.rotationPoint[2])
            translatedToRotationPointP2 = self.translate(triangle[1], -self.rotationPoint[0], -self.rotationPoint[1], -self.rotationPoint[2])
            translatedToRotationPointP3 = self.translate(triangle[2], -self.rotationPoint[0], -self.rotationPoint[1], -self.rotationPoint[2])
            translatedToRotationPoint = [translatedToRotationPointP1, translatedToRotationPointP2, translatedToRotationPointP3]
            #=====================================================================

            # Scale =============================================================
            scaledP1 = matrixMultiply(translatedToRotationPoint[0], 0, 0, 0, self.normalizeRescale)
            scaledP2 = matrixMultiply(translatedToRotationPoint[1], 0, 0, 0, self.normalizeRescale)
            scaledP3 = matrixMultiply(translatedToRotationPoint[2], 0, 0, 0, self.normalizeRescale)
            #=====================================================================

            # Rotate Z ===========================================================
            rotatedP1Z = matrixMultiply(scaledP1, xT, yT, zT, self.normalizeRotationZ)
            rotatedP2Z = matrixMultiply(scaledP2, xT, yT, zT, self.normalizeRotationZ)
            rotatedP3Z = matrixMultiply(scaledP3, xT, yT, zT, self.normalizeRotationZ)
            #=====================================================================
            
            # Rotate Y ===========================================================
            rotatedP1Y = matrixMultiply(rotatedP1Z, xT, yT, zT, self.normalizeRotationY)
            rotatedP2Y = matrixMultiply(rotatedP2Z, xT, yT, zT, self.normalizeRotationY)
            rotatedP3Y = matrixMultiply(rotatedP3Z, xT, yT, zT, self.normalizeRotationY)
            #=====================================================================
            
            # Rotate X ===========================================================
            rotatedP1X = matrixMultiply(rotatedP1Y, xT, yT, zT, self.normalizeRotationX)
            rotatedP2X = matrixMultiply(rotatedP2Y, xT, yT, zT, self.normalizeRotationX)
            rotatedP3X = matrixMultiply(rotatedP3Y, xT, yT, zT, self.normalizeRotationX)
            #=====================================================================

            # Translate to new World Pivot ===========================================================
            worldPivotPoint1 = self.translate( rotatedP1X, -self.worldPivot[0], -self.worldPivot[1], -self.worldPivot[2])
            worldPivotPoint2 = self.translate( rotatedP2X, -self.worldPivot[0], -self.worldPivot[1], -self.worldPivot[2])
            worldPivotPoint3 = self.translate( rotatedP3X, -self.worldPivot[0], -self.worldPivot[1], -self.worldPivot[2])
            #=========================================================================================
                     
            self.mutatePoint([worldPivotPoint1, worldPivotPoint2, worldPivotPoint3])
            self.translateList = [self.xTrans, self.yTrans, self.zTrans]

            # Camera Z Rotation ===========================================================
            zTri1 = matrixMultiply( worldPivotPoint1, 0, 0, 0, self.camera.getCameraZRotation() )
            zTri2 = matrixMultiply( worldPivotPoint2, 0, 0, 0, self.camera.getCameraZRotation() )
            zTri3 = matrixMultiply( worldPivotPoint3, 0, 0, 0, self.camera.getCameraZRotation() )
            #=========================================================================================

            # Camera X Rotation ===========================================================
            xTri1 = matrixMultiply( zTri1, 0, 0, 0, self.camera.getCameraXRotation() )
            xTri2 = matrixMultiply( zTri2, 0, 0, 0, self.camera.getCameraXRotation() )
            xTri3 = matrixMultiply( zTri3, 0, 0, 0, self.camera.getCameraXRotation() )
            #=========================================================================================
            
            # Camera Yaw Rotation ===========================================================
            yawTri1 = matrixMultiply( xTri1, 0, 0, 0, self.camera.getYawMatrix() )
            yawTri2 = matrixMultiply( xTri2, 0, 0, 0, self.camera.getYawMatrix() )
            yawTri3 = matrixMultiply( xTri3, 0, 0, 0, self.camera.getYawMatrix() )
            #=========================================================================================

            # Translate Back from World Pivot ===========================================================
            worldPivotPointRevered1 = self.translate( yawTri1, self.worldPivot[0], self.worldPivot[1], self.worldPivot[2])
            worldPivotPointRevered2 = self.translate( yawTri2, self.worldPivot[0], self.worldPivot[1], self.worldPivot[2])
            worldPivotPointRevered3 = self.translate( yawTri3, self.worldPivot[0], self.worldPivot[1], self.worldPivot[2])
            #=========================================================================================

            # Camera Transforms ==================================
            viewedTriP1 = matrixMultiply( worldPivotPointRevered1, 0, 0, 0, self.camera.lookAt() )
            viewedTriP2 = matrixMultiply( worldPivotPointRevered2, 0, 0, 0, self.camera.lookAt() )
            viewedTriP3 = matrixMultiply( worldPivotPointRevered3, 0, 0, 0, self.camera.lookAt() )
            #======================================================

            # Translate mesh back from rotation point ==================================
            rotatedAndTranslatedBackP1 = self.translate(viewedTriP1, self.rotationPoint[0], self.rotationPoint[1], self.rotationPoint[2])
            rotatedAndTranslatedBackP2 = self.translate(viewedTriP2, self.rotationPoint[0], self.rotationPoint[1], self.rotationPoint[2])
            rotatedAndTranslatedBackP3 = self.translate(viewedTriP3, self.rotationPoint[0], self.rotationPoint[1], self.rotationPoint[2])
            #=====================================================================
                                                          
            rotatedTri = [rotatedAndTranslatedBackP1, rotatedAndTranslatedBackP2, rotatedAndTranslatedBackP3]
            
            # Triangle Leg 1 ==========================
            line1X = rotatedTri[0][0]-rotatedTri[1][0]
            line1Y = rotatedTri[0][1]-rotatedTri[1][1]
            line1Z = rotatedTri[0][2]-rotatedTri[1][2]
            v1 = (line1X, line1Y, line1Z)
            #==========================================
            
            # Triangle Leg 2 ==========================
            line2X = rotatedTri[0][0]-rotatedTri[2][0]
            line2Y = rotatedTri[0][1]-rotatedTri[2][1]
            line2Z = rotatedTri[0][2]-rotatedTri[2][2]
            v2 = (line2X, line2Y, line2Z)
            #==========================================
            
            normalVector = getNormalVector(v1, v2)
            normalUnitVector = convertToUnitVector(normalVector)
            
            xT = 0
            yT = 0
            zT = 0
            
            # Translate/ Normalize Points ===================================================
            normalizedP1 = matrixMultiply(rotatedTri[0], xT, yT, zT, self.normalizePoints)
            normalizedP2 = matrixMultiply(rotatedTri[1], xT, yT, zT, self.normalizePoints)
            normalizedP3 = matrixMultiply(rotatedTri[2], xT, yT, zT, self.normalizePoints)
            translatedTri = [normalizedP1, normalizedP2, normalizedP3]
            #=====================================================================
        
            # Lighting Info ==================================================================================
            grayScale = ( dotProduct( [0, 0, 0], normalUnitVector, convertToUnitVector(self.lightingVector ) ) ) + 0.5
            if(grayScale > 1.7):
                grayScale = 1
            elif(grayScale < .5):
                grayScale = .5
            #==================================================================================================          

            # Project Points on Screen ==========================
            ax = translatedTri[0][0]*.5*self.screenWidth
            ay = translatedTri[0][1]*.5*self.screenHeight
            
            bx = translatedTri[1][0]*.5*self.screenWidth
            by = translatedTri[1][1]*.5*self.screenHeight
            
            cx = translatedTri[2][0]*.5*self.screenWidth
            cy = translatedTri[2][1]*.5*self.screenHeight
            #====================================================
            
            dotProd = dotProduct(app.cameraVector, normalUnitVector, translatedTri[0])
            newTri = Triangle((ax, ay, bx, by, cx, cy), triangle, dotProd, rgb(150*grayScale, 150*grayScale, 150*grayScale), translatedTri )

            if(dotProd <= 0):    
                self.frontTris.append(newTri)
            else:
                self.hiddenTris.append(newTri)
        
        self.frontTris = sortMeshData(self.frontTris)
        return (self.frontTris, self.hiddenTris)

    def mutatePoint(self, tri):
        tri[0][0] += self.xTrans
        tri[0][1] += self.yTrans
        tri[0][2] += self.zTrans

        tri[1][0] += self.xTrans
        tri[1][1] += self.yTrans
        tri[1][2] += self.zTrans

        tri[2][0] += self.xTrans
        tri[2][1] += self.yTrans
        tri[2][2] += self.zTrans

# ============================================================
#       update Matricies 
# ============================================================

    def initializeTransforms(self):
        # Rotation Z =======================================
        self.normalizeRotationZ[0][0] = math.cos(self.zAngle)
        self.normalizeRotationZ[0][1] = math.sin(self.zAngle)
        self.normalizeRotationZ[1][0] = -1 * math.sin(self.zAngle)
        self.normalizeRotationZ[1][1] = math.cos(self.zAngle)
        self.normalizeRotationZ[2][2] = 1
        self.normalizeRotationZ[3][3] = 1
        #=================================================
        
        # Rotation X =======================================
        self.normalizeRotationX[0][0] = 1
        self.normalizeRotationX[1][1] = math.cos(self.xAngle*.5)
        self.normalizeRotationX[1][2] = math.sin(self.xAngle*.5)
        self.normalizeRotationX[2][1] = -1*math.sin(self.xAngle*.5)
        self.normalizeRotationX[2][2] = math.cos(self.xAngle*.5)
        self.normalizeRotationX[3][3] = 1
        #=================================================
        
        # Rotation Y =======================================
        self.normalizeRotationY[0][0] = math.cos(self.yAngle)
        self.normalizeRotationY[0][2] = math.sin(self.yAngle)
        self.normalizeRotationY[2][0] = -1*math.sin(self.yAngle)
        self.normalizeRotationY[1][1] = 1
        self.normalizeRotationY[2][2] = math.cos(self.yAngle)
        self.normalizeRotationY[3][3] = 1
        # ================================================= 

        # Normalize =======================================
        self.normalizePoints[0][0] = self.aspectRatio * self.FOVrad
        self.normalizePoints[1][1] = self.FOVrad
        self.normalizePoints[2][2] = self.far / (self.far - self.near)
        self.normalizePoints[3][2] = (-1*self.far * self.near)/ (self.far - self.near)
        self.normalizePoints[2][3] = 1
        self.normalizePoints[3][3] = 1    
        # =================================================

        # Scale ===========================================
        self.normalizeRescale[0][0] = self.xScale
        self.normalizeRescale[1][1] = self.yScale
        self.normalizeRescale[2][2] = self.zScale
        self.normalizeRescale[3][3] = 1
        # =================================================
        
    def initializeConstants(self):
        self.far = 10000
        self.near = .1
        self.screenWidth = 3000
        self.screenHeight = 3000
        self.aspectRatio = self.screenWidth/self.screenHeight
        self.FOV = math.pi/3
        self.FOVrad = 1/math.tan(self.FOV)

# ====================================================================
# --------------------------------------------------------------------
#                           POINT CLASS
# --------------------------------------------------------------------
#===================================================================
            
class point:
    def __init__(self, points, camera):
        self.points = points
        self.worldPivot = [.5, .5, .5]
        self.camera = camera
        self.normalizePoints = [[0, 0, 0, 0] for i in range(4)]
        self.initializeConstants()
        self.initializeMatrix()

           
    def getTransformedPoints(self):
        finalPoints = []
        for point in [self.points]:
            if(app.selectedMeshIndex != None):
                self.worldPivot = vectorSubtract(app.worldPivot, [0, 0, 0])
                #self.worldPivot = vectorSubtract(app.worldPivot, app.meshList[app.selectedMeshIndex].rotationPoint)
            else:
                self.worldPivot = vectorSubtract(app.worldPivot, [0, 0, 0])

            worldPivotPoint = self.translate( point, -self.worldPivot[0], -self.worldPivot[1], -self.worldPivot[2])

            zRotated = matrixMultiply(worldPivotPoint, 0, 0, 0, self.camera.getCameraZRotation())
            xRotated = matrixMultiply(zRotated, 0, 0, 0, self.camera.getCameraXRotation())
            yawRotated = matrixMultiply(xRotated, 0, 0, 0, self.camera.getYawMatrix())

            worldPivotPointReverted = self.translate( yawRotated, self.worldPivot[0], self.worldPivot[1], self.worldPivot[2])
            viewedPoint = matrixMultiply(worldPivotPointReverted, 0, 0, 0, self.camera.lookAt())       

            if viewedPoint[2] < self.near:
                return None
            
            normalizedP1 = matrixMultiply(viewedPoint, 0, 0, 0, self.normalizePoints)
            projectedX = normalizedP1[0]*.5*self.screenWidth
            projectedY = normalizedP1[1]*.5*self.screenHeight
            
            finalPoints.append( [projectedX, projectedY] )

        return(projectedX, projectedY)

    def translate(self, point, x, y, z):
        return [point[0] + x, point[1] + y, point[2] + z]
    
    def initializeMatrix(self):
        self.normalizePoints[0][0] = self.aspectRatio * self.FOVrad
        self.normalizePoints[1][1] = self.FOVrad
        self.normalizePoints[2][2] = self.far / (self.far - self.near)
        self.normalizePoints[3][2] = (-1*self.far * self.near)/ (self.far - self.near)
        self.normalizePoints[2][3] = 1
        self.normalizePoints[3][3] = 1    

    def initializeConstants(self):
        self.far = 10000
        self.near = .1
        self.screenWidth = 3000
        self.screenHeight = 3000
        self.aspectRatio = self.screenWidth/self.screenHeight
        self.FOV = math.pi/3
        self.FOVrad = 1/math.tan(self.FOV)

# ====================================================================
# --------------------------------------------------------------------
#                           TRIANGLE CLASS
# --------------------------------------------------------------------
#===================================================================

class Triangle:
    def __init__(self, screenPoints, origionalPoints, normalVector, color, preProjectedTri):
        self.screenPoints = screenPoints
        self.origionalPoints = origionalPoints
        self.normalVector = normalVector
        self.color = color
        self.preProjectedTri = preProjectedTri
        self.avg = (self.preProjectedTri[0][2]+self.preProjectedTri[1][2]+self.preProjectedTri[2][2])/3
    
    def __repr__(self):
        return f'Triangle: {self.avg}'

# ====================================================================
# --------------------------------------------------------------------
#                          LINE CLASS
# --------------------------------------------------------------------
#===================================================================

class lineObject(point):
    def __init__(self, p1, p2, camera, worldPivot, name = None):
        self.p1 = p1
        self.p2 = p2
        self.line = self.sortPoints([p1, p2])
        self.camera = camera
        self.worldPivot = worldPivot

        self.normalizePoints = [[0, 0, 0, 0] for i in range(4)]
        self.initializeConstants()
        self.initializeMatrix()
        self.preProjectPoints = []
        self.name = name
    
    def sortPoints(self, line):
        p1, p2 = line
        if(p1[2] > p2[2]):
            return [p2, p1]
        else:
            return [p1, p2]
        
    def __eq__(self, other):
        return self.name == other
    
    def __repr__(self):
        return self.name

    def projectPoint(self, point):
        normalizedP1 = matrixMultiply(point, 0, 0, 0, self.normalizePoints)
        projectedX = normalizedP1[0]*.5*self.screenWidth
        projectedY = normalizedP1[1]*.5*self.screenHeight
        return [projectedX, projectedY]


    def mutatePoint(self, point):
        point[0] += app.meshList[app.selectedMeshIndex].rotationPoint[0]
        point[1] += app.meshList[app.selectedMeshIndex].rotationPoint[1]
        point[2] += app.meshList[app.selectedMeshIndex].rotationPoint[2]

    def getTransformedPoints(self):
        finalLine = []
        self.preProjectPoints = []
        for point in self.line:
            if(self.camera.name != 'Gizmo Camera'):
                self.worldPivot = vectorSubtract(app.worldPivot, [0, 0, 0])
            else:
                self.worldPivot = [0, 0, 0]
            
            worldPivotPoint = self.translate( point, -self.worldPivot[0], -self.worldPivot[1], -self.worldPivot[2])

            zRotated = matrixMultiply(worldPivotPoint, 0, 0, 0, self.camera.getCameraZRotation())
            xRotated = matrixMultiply(zRotated, 0, 0, 0, self.camera.getCameraXRotation())
            yawRotated = matrixMultiply(xRotated, 0, 0, 0, self.camera.getYawMatrix())
            worldPivotPointReverted = self.translate( yawRotated, self.worldPivot[0], self.worldPivot[1], self.worldPivot[2])
            viewedPoint = matrixMultiply(worldPivotPointReverted, 0, 0, 0, self.camera.lookAt()) 

            self.preProjectPoints.append(viewedPoint)   

            if(point == self.line[0]):
                lineStartViewed = viewedPoint                   
            elif(point == self.line[1]):
                lineEndViewed = viewedPoint

        # CAMERA CLIPPING ==========================================================================
        farPlane = 30
        if(lineStartViewed[2] > farPlane):
            if lineEndViewed[2] <= farPlane:
                intersection = intersectPlane([0, 0, -farPlane], [0, 0, -1], lineStartViewed, lineEndViewed)
                finalLine.append(self.projectPoint(intersection))
                finalLine.append(self.projectPoint(lineEndViewed))
        elif(lineEndViewed[2] > farPlane):
            if lineStartViewed[2] <= farPlane:
                intersection = intersectPlane([0, 0, -farPlane], [0, 0, -1], lineEndViewed, lineStartViewed)
                finalLine.append(self.projectPoint(lineStartViewed))
                finalLine.append(self.projectPoint(intersection))
        elif(lineStartViewed[2] < self.near and lineEndViewed[2] >= self.near):
            intersection = intersectPlane([0, 0, self.near], [0, 0, 1], lineStartViewed, lineEndViewed)
            finalLine.append(self.projectPoint(intersection))
            finalLine.append(self.projectPoint(lineEndViewed))
        elif(lineEndViewed[2] < self.near and lineStartViewed[2] >= self.near):
            intersection = intersectPlane([0, 0, self.near], [0, 0, 1], lineEndViewed, lineStartViewed)
            finalLine.append(self.projectPoint(lineStartViewed))
            finalLine.append(self.projectPoint(intersection))
        elif(lineStartViewed[2] >= self.near and lineEndViewed[2] >= self.near):
            finalLine.append(self.projectPoint(lineStartViewed))
            finalLine.append(self.projectPoint(lineEndViewed))
        #========================================================================================
        
        
        return finalLine