# -*- coding: utf-8 -*-

import math

from pysvg.structure import svg
from pysvg.text import text
from pysvg.text import tspan
from pysvg.builders import ShapeBuilder
from pysvg.builders import StyleBuilder
from pysvg.structure import g
from parsetreegen.bbcoderesolver import BBCodeResolver
from parsetreegen.bbcoderesolver.BBCText import BBCText
from parsetreegen.bbcoderesolver.BBCLine import BBCLine
from ParseTreeGenStructures import FramePosition
from parsetreegen.renderers.NodeRenderer import NodeRenderer;
from parsetreegen.renderers.ArrowRenderer import ArrowRenderer;

class SVGTreeCreator:
    def __init__(self, conf):
        self.__conf = conf
        
        self.__containerHeights = dict()
        self.__framesPositions = dict()
        
        self.__nodeRenderer = NodeRenderer(conf);
        self.__arrowRenderer = ArrowRenderer(conf);
        
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
        
    def determineFramesPositions(self, node, level = 0):
        '''
        Determines the spatial position of frames in SVG.
    
        @param node: root node of tree or subtree
        @param level: depth level of node investigated currently    
        '''
        if node['type'] == 'node':
            if not self.__framesPositions.__contains__(level):
                self.__framesPositions[level] = dict()
                
            self.__containerHeights[node['id']] = self.__nodeRenderer.getNodeHeight(node);
            
            x = (self.__conf['frame']['width'] + self.__conf['frame']['verticalOffset']) * len(self.__framesPositions[level])
            y = (self.__containerHeights[node['id']] + self.__conf['frame']['horizontalOffset']) * level
            width = self.__conf['frame']['width']
            height = self.__containerHeights[node['id']]
            
            self.__framesPositions[level][node['id']] = FramePosition(x, y, width, height)
                
            if not level == 0:                
                self.__updateFramesOffsets()
                    
            if node.has_key('children'):
                for child in node['children']:
                    self.determineFramesPositions(child, level + 1)
    
        
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
        self.determineFramesPositions(rootNode)
        treeLevels = self.determineTreeLevels(rootNode)
        self.prepareConnectionsLevels(treeLevels)
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
            #self.prepareNode(node, i * (self.__conf['frame']['width'] + 150), level * 120)
            self.prepareNode(node, self.__framesPositions[level][node['id']].x, self.__framesPositions[level][node['id']].y)
            i += 1
            
    def prepareConnectionsLevels(self, treeLevels):  
        for level in treeLevels.keys():
            self.prepareConnectionsLevel(treeLevels[level], level)
            
    def prepareConnectionsLevel(self, nodes, level):
        for node in nodes.values():
            self.prepareConnectionsForNode(level, node)
    
    def prepareConnectionsForNode(self, level, node):
        if node['type'] == 'node':
            if node.has_key('children'):
                for child in node['children']:
                    if child['type'] == 'node':
                        self.prepareConnection(level, node, child)
                    
    def prepareConnection(self, level, startNode, endNode):
        startPositionFrame = self.__framesPositions[level][startNode['id']]
        endPositionFrame = self.__framesPositions[level + 1][endNode['id']]
        
        startX = startPositionFrame.x + startPositionFrame.width / 2;
        startY = startPositionFrame.y + startPositionFrame.height;
        endX = endPositionFrame.x + startPositionFrame.width / 2;
        endY = endPositionFrame.y;        
        
        self.drawConnection(startX, startY, endX, endY, self.__conf['connection'])
        
    def drawConnection(self, startX, startY, endX, endY, connectionConf):
        line = self.__shapeBuilder.createLine(startX, startY, endX, endY, strokewidth=connectionConf['thickness'], stroke="black")
        self.__SVGObject.addElement(line);
        
        slope = float();
        
        if connectionConf['marker'] == 'small':
            markerSize = float(25);
        elif connectionConf['marker'] == 'normal':
            markerSize = float(50);
        elif connectionConf['marker'] == 'large':
            markerSize = float(75); 
        
        startX = float(startX)
        startY = float(startY)
        endX = float(endX)
        endY = float(endY)
        
        if ((endX - startX) != 0) and ((endY - startY) != 0):
            slope = (endY - startY) / (endX - startX)
        else:
            slope = 1.5707


        slopeArrow1 = slope + (slope * 0.4)
        slopeArrow2 = slope - (slope * 0.4)
            
        arrow1MarkerXFactor = markerSize * math.cos(slopeArrow1)
        arrow1MarkerYFactor = markerSize * math.sin(slopeArrow1)
        
        arrow2MarkerXFactor = markerSize * math.cos(slopeArrow2)
        arrow2MarkerYFactor = markerSize * math.sin(slopeArrow2)
        
        if slope < 0:
            arrow1StartX = endX + arrow1MarkerXFactor
            arrow2StartX = endX + arrow2MarkerXFactor
        
            arrow1StartY = endY + arrow1MarkerYFactor
            arrow2StartY = endY + arrow2MarkerYFactor
        else:
            arrow1StartX = endX - arrow1MarkerXFactor
            arrow2StartX = endX - arrow2MarkerXFactor
        
            arrow1StartY = endY - arrow1MarkerYFactor
            arrow2StartY = endY - arrow2MarkerYFactor
        
        arrow1 = self.__shapeBuilder.createLine(arrow1StartX, arrow1StartY, endX, endY, strokewidth=connectionConf['thickness'], stroke="black") 
        arrow2 = self.__shapeBuilder.createLine(arrow2StartX, arrow2StartY, endX, endY, strokewidth=connectionConf['thickness'], stroke="black")
        
        self.__SVGObject.addElement(arrow1);
        self.__SVGObject.addElement(arrow2);        
    
    def prepareNode(self, node, startX, startY):
        container = self.__nodeRenderer.render(node, startX, startY);
        self.__SVGObject.addElement(container);

    
    def __updateFramesOffsets(self):
        pass
        