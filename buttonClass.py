from cmu_graphics import *

class button:
    def __init__(self, x, y, width, height, name = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isHovered = False
        self.name = name
    
    def __repr__(self):
        return f'{self.name}'
    
    def __eq__(self, other):
        return self.name == other


    def hovered(self, mx, my):
        if(self.x <= mx <= self.x+self.width and self.y <= my <= self.y+self.height):
            return True
        return False

#===================================================================================
#                               SLIDER CLASS
#===================================================================================
    
class slider(button):
    instances = []
    def __init__(self, x, y, width, height, sliderControlPoint, sliderWidth, color, name = None):
        super().__init__(x, y, width, height)
        self.control = sliderControlPoint
        self.controlSize = sliderWidth
        self.name = name
        self.canDrag = False
        self.endPoint = self.x + self.width
        self.color = color
        slider.instances.append(self)
    
    @classmethod
    def updateAll(cls, x = None, y = None, width = None, height = None):
        for instance in cls.instances:
            if(x != None):
                instance.x = x
            if(y != None):
                instance.y = y
            if(width != None):
                instance.width = width
            if(height != None):
                instance.height = height

    def hovered(self, mx, my):
        if(self.control == 'left'):
            if(self.x <= mx <= self.x + self.controlSize and self.y <= my <= self.y + self.height):
                return True
        elif(self.control == 'right'):
            if(self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.controlSize):
                return True
            
        if(self.control == 'top'):
            if(self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.controlSize):
                return True
        return False

#===================================================================================
#                               SEARCH BAR CLASS
#===================================================================================

class searchBar(button):
    def __init__(self, data, key, x, y, width, height):
        super().__init__(x, y, width, height)
        self.data = data
        self.key = key
    
    def getSearchData(self):
        result = []
        setData = set(self.data)
        for word in setData:
            if(self.key in word):
                result.append(word)
        return result

#===================================================================================
#                               PICTURE CLASS
#===================================================================================       

class Picture(button):
    def __init__(self, url, x, y, width, height, pressedURL):
        super().__init__(x, y, width, height)
        self.url = url
        self.pressedURL = pressedURL

        self.ogURL = url
        self.ogPressed = pressedURL

    def __repr__(self):
        return f'{self.url[38:]}'

    def __eq__(self, other):
        if(self.url[38:] == other):
            return True
        return False

    def switch(self):
        self.url, self.pressedURL = self.pressedURL, self.url

#===================================================================================
#                               Drop Down
#=================================================================================== 

class DropDown(button):
    def __init__(self, url, x, y, width, height, dropDownImage, ButtonList, name = None, ):
        super().__init__(x, y, width, height)
        self.url = url
        self.dropDownImage = dropDownImage
        self.drawDropDown = False

        self.ogURL = url
        self.ogPressed = url

        self.name = name
        self.buttonList = ButtonList
    
    def __repr__(self):
        if(self.url != None):
            return f'{self.url[38:]}'
        else:
            return self.name

    def dropDownHovered(self, mx, my):
        if(self.x <= mx <= self.x + getImageSize(self.dropDownImage)[0] and self.y + self.height <= my <= self.y + getImageSize(self.dropDownImage)[1] or self.hovered(mx, my)):
            return True
        return False
    
    def getDropDownButtons(self):
        result = []
        num = len(self.buttonList)
        spacing = (getImageSize(self.dropDownImage)[1]/1.3)/num
        if(self.drawDropDown):
            for i in range(num):
                result.append( button(self.x, self.y + self.height + spacing*i, getImageSize(self.dropDownImage)[0]/1.3, spacing, self.buttonList[i]) )
            return result
