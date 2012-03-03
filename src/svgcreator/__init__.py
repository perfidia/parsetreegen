# -*- coding: utf-8 -*-

from pysvg.structure import svg
from pysvg.text import text
from pysvg.builders import ShapeBuilder
from pysvg.builders import StyleBuilder
from pysvg.structure import g

class SVGCreator:
    def __init__(self, conf):
        self.__conf = conf
        
        self.prepareSVGObject()
        self.prepareShapeBuilder()
        
    def prepareSVGObject(self):
        self.__SVGObject = svg()
        
    def prepareShapeBuilder(self):
        self.__shapeBuilder = ShapeBuilder()
        
    def prepareXML(self):
        return self.__SVGObject.getXML()
    
    def createSVGFile(self, fileName):
        self.__SVGObject.save(fileName)
        
    def prepareNode(self, node): # node is an instance of class Node 
        startX = 50
        startY = 50
        width = 100
        height = 200
        
        nodeGroup = g()
        
        self.prepareNodeContainer(startX, startY, width, height, nodeGroup)
        if node['type'] == 'node':
            i = 0
            for line in node['value']:                
                if isinstance(line, int):
                    #TODO insert horizontal line to separate
                    separatorObj = text('~~~~~~~~', startX, startY + (i * 15))
                    nodeGroup.addElement(separatorObj)
                elif isinstance(line, str):
                    txtObj = text(line, startX, startY + (i * 15))
                    nodeGroup.addElement(txtObj)
                else:
                    raise Exception("unsupported value type")
                
                i += 1
                
            self.__SVGObject.addElement(nodeGroup)
        
    def prepareNodeContainer(self, startX, startY, width, height, nodeGroup):
        rect = self.__shapeBuilder.createRect(startX, startY, width, height, strokewidth=self.__conf['frame']['thickness'], stroke='black')
        nodeGroup.addElement(rect) 
            