# -*- coding: utf-8 -*-

from pysvg.structure import svg
from pysvg.text import text
from pysvg.builders import ShapeBuilder
from pysvg.builders import StyleBuilder
from pysvg.structure import g

class SVGCreator:
    def __init__(self):
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
        
    def drawNode(self, node): # node is an instance of class Node 
        self.prepareNodeContainer()
        
        
    def prepareNodeContainer(self):
        self.__nodeContainer = g() 
        
    def prepareNodeHeader(self, nodeType):
        self.prepareNodeContainer()
        rect = self.__shapeBuilder.createRect(0, 0, 100, 55, strokewidth=1, stroke='black')
        headerText = text("Node type:", 5, 20)
        nodeTypeText = text(nodeType, 5, 40)
        nodeTypeTextStyle = StyleBuilder()
        nodeTypeTextStyle.setFontWeight('bold')
        nodeTypeText.set_style(nodeTypeTextStyle.getStyle())
        self.__nodeContainer.addElement(rect)
        self.__nodeContainer.addElement(headerText)
        self.__nodeContainer.addElement(nodeTypeText)
        self.__SVGObject.addElement(self.__nodeContainer)
        
    