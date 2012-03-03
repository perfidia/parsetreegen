# -*- coding: utf-8 -*-

from pysvg.structure import svg
from pysvg.text import text
from pysvg.builders import ShapeBuilder
from pysvg.builders import StyleBuilder
from pysvg.structure import g

class SVGTreeCreator:
    def __init__(self, conf):
        self.__conf = conf
        self.__nodeDefaultWidth = 100
        
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
        
    def determineTreeWidth(self, data, level = 1, result = None):
        '''
        Counts nodes (type = 'node', excluding type = 'reference') on each depth level.
    
        @param data: root node of tree or subtree
        @param level: depth level of node investigated currently
        @param result: dictionary with with levels as keys and number of nodes on this level as values
    
        @return: updated result
        '''
        if data['type'] == 'node':
            if result == None and level == 1:
                result = dict()
                result[1] = 1
                
            if level != 1 and result != None:
                if result.__contains__(level):
                    result[level] += 1
                else:
                    result[level] = 1
                    
            if data.has_key('children'):
                for child in data['children']:
                    result = self.determineTreeWidth(child, level + 1, result)
                                
        return result
        
    def prepareTree(self, rootNode):
        treeWidth = self.determineTreeWidth(rootNode)
        
        maxWidth = 0
        for level in treeWidth.keys():
            if treeWidth[level] > maxWidth:
                maxWidth = treeWidth[level]
        
        self.prepareNode(rootNode, maxWidth / 2 * (self.__nodeDefaultWidth + 150), 50)
        
        if rootNode['type'] == 'node':
            if rootNode.has_key('children'):
                i = 0
                for child in rootNode['children']:
                    self.prepareNode(child, i * (self.__nodeDefaultWidth + 150), 2 * 150)
                    i += 1
        
    def prepareNode(self, node, startX, startY):
        width = self.__nodeDefaultWidth
        height = 100
        
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
            