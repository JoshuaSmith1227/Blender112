from cmu_graphics import *

class button:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isHovered = False
    
    def __repr__(self):
        return f'Button at ({self.x}, {self.y})'

    def hovered(self, mx, my):
        if(self.x <= mx <= self.x+self.width and self.y <= my <= self.y+self.height):
            return True
        return False

#===================================================================================
#                               SLIDER CLASS
#===================================================================================
    
class slider(button):
    def __init__(self, sliderControlPoint, sliderWidth, x, y, width, height):
        super().__init__(self, x, y, width, height)
        self.control = sliderControlPoint
        self.controlSize = sliderWidth
    
    def hovered(self, mx, my):
        if(self.control == 'left'):
            if(self.x <= mx <= self.x + self.controlSize and self.y <= my <= self.y + self.height):
                return True
        elif(self.control == 'right'):
            if(self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.controlSize):
                return True
        return False

#===================================================================================
#                               SEARCH BAR CLASS
#===================================================================================

class searchBar(button):
    def __init__(self, data, key, x, y, width, height):
        super().__init__(self, x, y, width, height)
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
    def __init__(self, url, x, y, width, height, dropDownImage):
        super().__init__(x, y, width, height)
        self.url = url
        self.dropDownImage = dropDownImage
        self.drawDropDown = False

        self.ogURL = url
        self.ogPressed = url
    
    def __repr__(self):
        return f'{self.url[38:]}'

    def dropDownHovered(self, mx, my):
        if(self.x <= mx <= self.x + getImageSize(self.dropDownImage)[0] and self.y <= my <= self.y + getImageSize(self.dropDownImage)[1]):
            return True
        return False
    
    def dropDownButtons(self):
        pass
