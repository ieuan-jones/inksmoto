from transform import Transform
from matrix import Matrix
from path import Path
import logging, log

class Layer:
    def __init__(self, layerAttributes):
        self.attributes = layerAttributes
        self.paths      = []
        self.children   = []
        self.transformMatrix = Matrix()

        if self.attributes.has_key('transform'):
            self.transformMatrix = Transform().createTransformationMatrix(self.attributes['transform'])

    def addPath(self, pathAttributes):
        self.paths.append(Path(pathAttributes, self.transformMatrix))
        
    def addRect(self, rectAttributes):
        rectAttributes = self.transformRectIntoPath(rectAttributes)
        self.paths.append(Path(rectAttributes, self.transformMatrix))

    def addChild(self, childLayer):
        childLayer.addParentTransform(self.transformMatrix)
        self.children.append(childLayer)

    def addParentTransform(self, parentTranformMatrix):
        # parent transformation is applied before self transformation
        self.transformMatrix = parentTranformMatrix * self.transformMatrix

    def transformRectIntoPath(self, attrs):
       width  = float(attrs['width'])
       height = float(attrs['height'])
       x      = float(attrs['x'])
       y      = float(attrs['y'])

       if width == 0 or height == 0:
           raise Exception('Rectangle %s has its width or its height equals to zero' % attrs['id'])

       d = "M %f,%f L %f,%f L %f,%f L %f,%f L %f,%f z" % (x,y, x+width,y, x+width,y+height, x,y+height, x,y)
       attrs['d'] = d
       
       return attrs
