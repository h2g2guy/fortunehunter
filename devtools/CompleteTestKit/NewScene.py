import pygame
from pygame.sprite import RenderUpdates

class Scene(pygame.sprite.RenderUpdates):

    def __init__(self, *sprites):

       self._spritelist = []
       RenderUpdates.__init__(self, *sprites)

       self.xPos = 0
       self.yPos = 0
       self.xSize = 0
       self.ySize = 0
       
       self.calcPosition()
       #self.calcSize()
       #self.setRelativePositions()

    def calcPosition(self):
    
       lowestX = 9000
       lowestY = 9000
       
       cnt = 0
       while cnt < len(self._spritelist):
           if self._spritelist[cnt][0].getXPos() < lowestX: lowestX = self._spritelist[cnt][0].getXPos()
           if self._spritelist[cnt][0].getYPos() < lowestY: lowestY = self._spritelist[cnt][0].getYPos()
           cnt += 1

       self.xPos = lowestX
       self.yPos = lowestY

    #def calcSize(self):

    def addObjects(self, newDrawableObjects):
        for sprite in newDrawableObjects:
           RenderUpdates.add_internal(self, sprite)
           self._spritelist.append(sprite)

    #def setRelativePositions(self):

    def removeObject(self, sprite):
       RenderUpdates.remove_internal(self, sprite)
       self._spritelist.remove(sprite)

    #def getObject(self, index):

    def getListSize(self):

       return len(self._spritelist)

    def getList(self):

       return list(self._spritelist)

    #def moveObjects(self):

    #def moveScene(self, xNudge = 0, yNudge = 0):

    #def setPosition(self, newXPos = None, newYPos = None):

    def getXPos(self):
       return self.xPos

    def getYPos(self):
       return self.yPos

    #def getXSize(self):

    #def getYSize(self):

    #@def scaleObjects(self, newXSize = None, newYSize = None):

    #def scaleScene(self, newXSize = None, newYSize = None):

    #def updateAnimations(self, t):

    #def nextFrame(self):
