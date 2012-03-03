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
        
    def prepareNode(self, node): # node is an instance of class Node 
        self.prepareNodeContainer()
        if node['type'] == 'node':
            self.prepareNodeHeader("TestNodeHeader")
#            for line in node['value']:
#                if isinstance(line, int):
#                    pass
#                elif isinstance(line, str):
#                    pass
#                else:
#                    raise Exception("unsupported value type")
        
    def prepareNodeContainer(self):
        self.__nodeContainer = g() 
        
    def prepareNodeHeader(self, headerText):        
        rect = self.__shapeBuilder.createRect(0, 0, 100, 55, strokewidth=1, stroke='black')
        headerTextObj = text("Node type:", 5, 20)
        nodeTypeText = text(headerText, 5, 40)
        nodeTypeTextStyle = StyleBuilder()
        nodeTypeTextStyle.setFontWeight('bold')
        nodeTypeText.set_style(nodeTypeTextStyle.getStyle())
        self.__nodeContainer.addElement(rect)
        self.__nodeContainer.addElement(headerTextObj)
        self.__nodeContainer.addElement(nodeTypeText)
        self.__SVGObject.addElement(self.__nodeContainer)
        
    