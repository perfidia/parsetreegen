'''
Created on Mar 19, 2012

@author: hilfman
'''

from pysvg.builders import ShapeBuilder

class ArrowRenderer(object):
    def __init__(self, conf):
        self.__lineType = conf['connection']['style'];
        self.__thickness = conf['connection']['thickness'];
        self.__markerSize = conf['connection']['marker'];

        self.__refLineType = conf['reference']['style'];
        self.__refMarkerSize = conf['reference']['marker'];
        self.__refThickness = conf['reference']['thickness'];

        self.__shapeBuilder = ShapeBuilder()

    def render(self, startX, startY, endX, endY, arrowMarker, isReference):

        if isReference:
            return self.__renderReference(startX, startY, endX, endY, arrowMarker);
        else:
            return self.__renderArrow(startX, startY, endX, endY, arrowMarker);

    def __renderArrow(self, startX, startY, endX, endY, arrowMarker):

        line = self.__shapeBuilder.createLine(startX, startY, endX, endY);

        if self.__lineType == "dashed":
            lineStyle = "stroke-dasharray:8 4 20 4;"
        elif self.__lineType == 'dotted':
            lineStyle = "stroke-dasharray:4 4;";
        else:
            lineStyle = "";

        line.setAttribute("style", "marker-end:url(#" + arrowMarker + ");fill:none;stroke:black;stroke-width:" + str(self.__thickness) + ";width:3;" + lineStyle);

        return line;

    def __renderReference(self, startX, startY, endX, endY, arrowMarker):

        line = self.__shapeBuilder.createLine(startX, startY, endX, endY);

        if self.__refLineType == "dashed":
            lineStyle = "stroke-dasharray:8 4 20 4;"
        elif self.__refLineType == 'dotted':
            lineStyle = "stroke-dasharray:4 4;";
        else:
            lineStyle = "";

        line.setAttribute("style", "marker-end:url(#" + arrowMarker + ");fill:none;stroke:black;stroke-width:" + str(self.__refThickness) + ";width:3;" + lineStyle);

        return line;
