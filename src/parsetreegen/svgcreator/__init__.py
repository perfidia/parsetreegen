# -*- coding: utf-8 -*-

import math

from pysvg.structure import defs;
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
from parsetreegen.elements import Marker;

class SVGTreeCreator:
    def __init__(self, conf):
        self.__ARROW_MARKER_ID = "arrowMarker";

        self.__conf = conf

        self.__containerHeights = dict()
        self.__framesPositions = dict()
        self.__framesPositionsById = dict();

        self.__nodeRenderer = NodeRenderer(conf);
        self.__arrowRenderer = ArrowRenderer(conf);

        self.__prepareSVGObject()
        self.__prepareShapeBuilder()
        self.__prepareDefsContainer();

    def __prepareSVGObject(self):
        self.__SVGObject = svg()

    def __prepareShapeBuilder(self):
        self.__shapeBuilder = ShapeBuilder()

    def __prepareDefsContainer(self):
        self.__defs = defs();

        self.__defs.addElement(Marker(self.__ARROW_MARKER_ID))

        self.__SVGObject.addElement(self.__defs);

    def prepareXML(self):
        return self.__SVGObject.getXML()

    def createSVGFile(self, fileName):
        self.__SVGObject.save(fileName)

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
        #if node['type'] == 'node':
        if node.has_key('children'):
            for child in node['children']:
                #if child['type'] == 'node':
                self.prepareConnection(level, node, child);

                if child['type'] == 'reference':
                    refNode = self.__findNode(child['value'], self.__rootNode);
                    self.prepareRefConnection(child, refNode);

    def prepareConnection(self, level, startNode, endNode):
        startPositionFrame = self.__framesPositions[level][startNode['id']]
        endPositionFrame = self.__framesPositions[level + 1][endNode['id']]

        startX = startPositionFrame.x + startPositionFrame.width / 2;
        startY = startPositionFrame.y + startPositionFrame.height;
        endX = endPositionFrame.x + startPositionFrame.width / 2;
        endY = endPositionFrame.y;

        self.drawConnection(startX, startY, endX, endY, self.__conf['connection'], False)

    def prepareRefConnection(self, startNode, endNode):
        startPositionFrame = self.__framesPositionsById[startNode['id']]
        endPositionFrame = self.__framesPositionsById[endNode['id']]

        horizontalOffset = math.fabs(endPositionFrame.x - startPositionFrame.x);
        verticalOffset = math.fabs(endPositionFrame.y - startPositionFrame.y);

        top = endPositionFrame.y < startPositionFrame.y;
        bottom = not top;
        left = endPositionFrame.x < startPositionFrame.x;
        right = not left;

        if left and horizontalOffset > verticalOffset:
            #connect left edges
            startX = startPositionFrame.x;
            startY = startPositionFrame.y + startPositionFrame.height / 2;
            endX = endPositionFrame.x + startPositionFrame.width;
            endY = endPositionFrame.y + endPositionFrame.height / 2;
        elif top and verticalOffset > horizontalOffset:
            startX = startPositionFrame.x + startPositionFrame.width / 2;
            startY = startPositionFrame.y;
            endX = endPositionFrame.x + endPositionFrame.width / 2;
            endY = endPositionFrame.y + endPositionFrame.height;
        elif right and horizontalOffset > verticalOffset:
            startX = startPositionFrame.x + startPositionFrame.width;
            startY = startPositionFrame.y + startPositionFrame.height / 2;
            endX = endPositionFrame.x;
            endY = endPositionFrame.y + endPositionFrame.height / 2;
        elif bottom and verticalOffset > horizontalOffset:
            startX = startPositionFrame.x + startPositionFrame.width / 2;
            startY = startPositionFrame.y + startPositionFrame.height;
            endX = endPositionFrame.x + endPositionFrame.width / 2;
            endY = endPositionFrame.y;

        self.drawConnection(startX, startY, endX, endY, self.__conf['connection'], True)

    def drawConnection(self, startX, startY, endX, endY, connectionConf, isReference):

        diff = 10;

        if startX != endX:
            const = math.fabs(startY - endY) / math.fabs(startX - endX);
            offsetX = diff / math.sqrt(1 + const * const)
            offsetY = offsetX * const;

            if startX < endX:
                endX = endX - offsetX;
            else:
                endX = endX + offsetX;
        else:
            offsetY = diff;

        if startY < endY:
            endY = endY - offsetY;
        else:
            endY = endY + offsetY;


        line = self.__arrowRenderer.render(startX, startY, endX, endY, self.__ARROW_MARKER_ID, isReference);

        self.__SVGObject.addElement(line);

    def prepareNode(self, node, startX, startY):

        isRef = False;

        if node['type'] == 'reference':
            node = self.__findNode(node['value'], self.__rootNode);
            isRef = True;

        container = self.__nodeRenderer.render(node, startX, startY, isRef);
        self.__SVGObject.addElement(container);

    def __findNode(self, id, node):
        if node['type'] == 'node':
            if node['id'] == id:
                return node;
            elif node.has_key('children'):
                for child in node['children']:
                    found = self.__findNode(id, child)
                    if found != None:
                        return found;
        return None;


    def __determineFramesPositions(self, node, level = 0):
        '''
        Determines the spatial position of frames in SVG.

        @param node: root node of tree or subtree
        @param level: depth level of node investigated currently
        '''
        if not self.__framesPositions.__contains__(level):
            self.__framesPositions[level] = dict()

        self.__containerHeights[node['id']] = self.__nodeRenderer.getNodeHeight(node)

        x = (self.__conf['frame']['width'] + self.__conf['frame']['verticalOffset']) * len(self.__framesPositions[level])
        y = self.__findLevelVerticalPosition(level)
        width = self.__conf['frame']['width']
        height = self.__containerHeights[node['id']]

        framePosition = FramePosition(x, y, width, height);
        self.__framesPositions[level][node['id']] = framePosition;
        self.__framesPositionsById[node['id']] = framePosition;

        if node.has_key('children'):
            for child in node['children']:
                self.__determineFramesPositions(child, level + 1)

    def __updateFramesOffsets(self, node, parent = None, level = 0):
        if  node.has_key('children'):

            offsetValue = self.__calculateOffset(node)
            nodeEncountered = False

            for frameKey in self.__framesPositions[level]:
                if node['id'] == frameKey:
                    self.__framesPositions[level][frameKey].x += offsetValue

                    nodeEncountered = True
                else:
                    if nodeEncountered:
                        self.__framesPositions[level][frameKey].x += offsetValue * 2

            childCounter = 0
            for child in node['children']:
                self.__framesPositions[level + 1][child['id']].x = self.__framesPositions[level][node['id']].x - offsetValue + ((self.__conf['frame']['width'] + self.__conf['frame']['verticalOffset']) * childCounter)
                childCounter += 1
            for child in node['children']:
                self.__updateFramesOffsets(child, node, level + 1)

    def __calculateOffset(self, node):
        result = 0
        if node.has_key('children'):
            result = (len(node['children']) - 1) * (self.__conf['frame']['width'] + self.__conf['frame']['verticalOffset']) / 2
            for child in node['children']:
                result += self.__calculateOffset(child)

        return result

    def determineTreeLevels(self, data, level = 0, result = None):
        '''
        Grouping nodes according to depth levels. Considering type = 'node', excluding type = 'reference'.

        @param data: root node of tree or subtree
        @param level: depth level of node investigated currently
        @param result: dictionary with with levels as keys and list of nodes on this level as values

        @return: updated result
        '''
        #if data['type'] == 'node':
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
        self.__rootNode = rootNode;
        treeLevels = self.determineTreeLevels(rootNode)
        self.__determineFramesPositions(rootNode)
        self.__updateFramesOffsets(rootNode)
        self.prepareConnectionsLevels(treeLevels)
        self.prepareTreeLevels(treeLevels)

    def __findLevelVerticalPosition(self, level):
        maxLevelValue = 0
        if level <> 0:

            for nodeHeightKey, nodeHeightValue in self.__containerHeights.iteritems():
                for nodeKey in self.__framesPositions[level - 1]:
                    if nodeHeightKey == nodeKey and nodeHeightValue > maxLevelValue:
                        maxLevelValue = nodeHeightValue

            maxLevelValue += self.__findLevelVerticalPosition(level - 1) + self.__conf['frame']['horizontalOffset']

        return maxLevelValue

    def __nodeChildrenLen(self, node):
        result = 0
        if node.has_key('children'):
            for child in node['children']:
                if child['type'] == 'node' :
                    result += 1

        return result
