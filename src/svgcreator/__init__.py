# -*- coding: utf-8 -*-

from pysvg.structure import svg
from pysvg.text import text
from pysvg.text import tspan;
from pysvg.builders import ShapeBuilder
from pysvg.builders import StyleBuilder
from pysvg.structure import g
from bbcoderesolver import BBCodeResolver
from bbcoderesolver.BBCText import BBCText;
from bbcoderesolver.BBCLine import BBCLine;

class SVGTreeCreator:
    def __init__(self, conf):
        self.__conf = conf
        
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
            self.prepareNode(node, i * (self.__conf['frame']['width'] + 150), level * 120)
            i += 1
        
    def prepareNode(self, node, startX, startY):
        
        width = self.__conf['frame']['width'];
        height = self.__determineContainterHeight(node);
        
        startX += self.__conf['frame']['padding']
        startY += self.__conf['frame']['padding']
        
        nodeGroup = g()
        nodeGroup.set_style(self.__textStyle.getStyle())        
        
        
        self.prepareNodeContainer(startX, startY, width, height, nodeGroup)
        if node['type'] == 'node':
            i = 1
            
            lines = self.__createLines(node['value'])
            
            for line in lines:                
                if isinstance(line, int):
                    separatorObj = self.__shapeBuilder.createLine(startX, startY + (i * 15), startX + width, startY + (i * 15), strokewidth=self.__conf['frame']['separator']['width'])
                    nodeGroup.addElement(separatorObj)
                elif isinstance(line, list):
                    txtObj = text(None, startX + self.__conf['frame']['padding'], startY + (i * 15) + self.__conf['frame']['padding']);
                    
                    for txt in line:
                        span = tspan();
                        span.appendTextContent(txt.getText());
                        span.setAttribute("style", txt.getStyle())
                        txtObj.addElement(span)
                    
                    nodeGroup.addElement(txtObj)
                else:
                    raise Exception("unsupported value type")
                
                i += 1
                
            self.__SVGObject.addElement(nodeGroup)
        
    def prepareNodeContainer(self, startX, startY, width, height, nodeGroup):
        rect = self.__shapeBuilder.createRect(startX, startY, width, height, strokewidth=self.__conf['frame']['thickness'], stroke='black', fill='white')
        nodeGroup.addElement(rect) 
        
    def __determineContainterHeight(self, node):
        linesNumber = len(self.__createLines(node['value']));
        #TODO wrapping!
        return linesNumber * self.__determineLineHeight();
    
    def __determineLineHeight(self):
        return 18;
    
    def __createLines(self, values):
        resolver = BBCodeResolver();
        
        result = [];
        
        for value in values:
            if isinstance(value, str):
                lines = resolver.resolveString(value);
                if isinstance(lines, list):
                    for line in lines:
                        result.append(line);
            elif isinstance(value, int):
                result.append(value);
        
        return result;
        