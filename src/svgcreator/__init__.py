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
        self.__nodeDefaultHeight = 100
        
        self.__textStyle = StyleBuilder()
        self.__textStyle.setFontFamily(fontfamily=self.__conf['frame']['font']['name'])
        self.__textStyle.setFontSize(self.__conf['frame']['font']['size'].__str__() + 'px')
        
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
        
    def determineTreeLevels(self, data, level = 0, result = None):
        '''
        Grouping nodes according to depth levels. Considering type = 'node', excluding type = 'reference'.
    
        @param data: root node of tree or subtree
        @param level: depth level of node investigated currently
        @param result: dictionary with with levels as keys and list of nodes on this level as values
    
        @return: updated result
        '''
        if data['type'] == 'node':
            if result == None and level == 0:
                result = dict()                
                
            if not result.__contains__(level):
                result[level] = dict()
            result[level][len(result[level].keys())] = data
                    
            if data.has_key('children'):
                for child in data['children']:
                    result = self.determineTreeLevels(child, level + 1, result)
                                
        return result
        
    def prepareTree(self, rootNode):
        treeLevels = self.determineTreeLevels(rootNode)
        
        self.prepareTreeLevels(treeLevels)
        
#        if rootNode['type'] == 'node':
#            if rootNode.has_key('children'):
#                i = 0
#                for child in rootNode['children']:
#                    self.prepareNode(child, i * (self.__nodeDefaultWidth + 150), 2 * 150)
#                    i += 1
    
    def prepareTreeLevels(self, treeLevels):
        for level in treeLevels.keys():
            self.prepareTreeLevel(treeLevels[level], level)
    
    def prepareTreeLevel(self, nodes, level):
        i = 0
        for node in nodes.values():
            self.prepareNode(node, i * (self.__nodeDefaultWidth + 150), level * 120)
            i += 1
        
    def prepareNode(self, node, startX, startY):
        width = self.__nodeDefaultWidth
        height = self.__nodeDefaultHeight
        
        startX += self.__conf['frame']['padding']
        startY += self.__conf['frame']['padding']
        
        nodeGroup = g()
        nodeGroup.set_style(self.__textStyle.getStyle())        
        
        self.prepareNodeContainer(startX, startY, width, height, nodeGroup)
        if node['type'] == 'node':
            i = 1
            for line in node['value']:                
                if isinstance(line, int):
                    #TODO insert horizontal line to separate
                    separatorObj = text('~~~~~~~~', startX + self.__conf['frame']['padding'], startY + (i * 15) + self.__conf['frame']['padding'])
                    nodeGroup.addElement(separatorObj)
                elif isinstance(line, str):
                    txtObj = text(line, startX + self.__conf['frame']['padding'], startY + (i * 15) + self.__conf['frame']['padding'])
                    nodeGroup.addElement(txtObj)
                else:
                    raise Exception("unsupported value type")
                
                i += 1
                
            self.__SVGObject.addElement(nodeGroup)
        
    def prepareNodeContainer(self, startX, startY, width, height, nodeGroup):
        rect = self.__shapeBuilder.createRect(startX, startY, width, height, strokewidth=self.__conf['frame']['thickness'], stroke='black')
        nodeGroup.addElement(rect) 
            