'''
Created on Mar 19, 2012

@author: hilfman
'''

from pysvg.text import text
from pysvg.text import tspan
from parsetreegen.bbcoderesolver import BBCodeResolver;
from pysvg.builders import StyleBuilder
from pysvg.builders import ShapeBuilder
from pysvg.structure import g

class NodeRenderer(object):
    def __init__(self, conf):

        self.__shapeBuilder = ShapeBuilder()

        self.__fontSize = conf['frame']['font']['size'];
        self.__fontFamily = conf['frame']['font']['name'];
        self.__alignment = conf['frame']['font']['align'];

        self.__frameThickness = conf['frame']['thickness'];
        self.__frameWidth = conf['frame']['width'];
        self.__framePadding = conf['frame']['padding'];

        self.__separatorWidth = conf['frame']['separator']['width'];

        self.__textStyle = StyleBuilder()
        self.__textStyle.setFontFamily(self.__fontFamily)
        self.__textStyle.setFontSize(self.__fontSize.__str__() + 'px')

        self.__LINE_SEPARATOR = 5;
        
        self.__resolver = BBCodeResolver();

    def __createLines(self, values):
        result = [];

        for value in values:
            if type(value) in [str, unicode]:
                lines = self.__resolver.resolveString(value);
                
                if isinstance(lines, list):
                    for line in lines:
                        result.append(line);
            elif isinstance(value, int):
                result.append(value);
            else:
                assert 1 == 2

        return result;

    def __determineLineHeight(self, isSeparator):
        if isSeparator:
            return self.__separatorWidth + self.__LINE_SEPARATOR;
        else:
            return self.__fontSize + self.__LINE_SEPARATOR;

    def __determineContainterHeight(self, lines):
        #TODO wrapping!

        height = 0;

        for line in lines:
            if isinstance(line, int):
                height = height + self.__determineLineHeight(True);
            else:
                height = height + self.__determineLineHeight(False);

        return height + 2 * self.__framePadding;

    def __prepareNodeContainer(self, startX, startY, width, height, isReference):
        nodeGroup = g()
        nodeGroup.set_style(self.__textStyle.getStyle())

        if isReference:
            color = 'gray';
        else:
            color = 'white';

        rect = self.__shapeBuilder.createRect(startX, startY, width, height, strokewidth = self.__frameThickness, stroke='black', fill=color)
        nodeGroup.addElement(rect)

        return nodeGroup;

    def render(self, node, startX, startY, isReference = False):
        if node['type'] != 'node':
            raise Exception("Wrong input object. Expected type: 'node'");

        lines = self.__createLines(node['value']);

        height = self.__determineContainterHeight(lines);

        nodeContainer = self.__prepareNodeContainer(startX, startY, self.__frameWidth, height, isReference)

        y = startY + self.__framePadding;

        for line in lines:
            if isinstance(line, int): # if int, then render horizontal line
                lineHeight = self.__determineLineHeight(True);
                x = startX;

                separatorObj = self.__shapeBuilder.createLine(x, y, x + self.__frameWidth, y, strokewidth = self.__separatorWidth)
                nodeContainer.addElement(separatorObj)

            elif isinstance(line, list): #list, because line is list of bbcoded spans
                lineHeight = self.__determineLineHeight(False);
                x = startX + self.__framePadding;

                txtObj = text(None, x, y + self.__fontSize);

                for txt in line:
                    span = tspan();
                    span.appendTextContent(txt.getText());
                    span.setAttribute("style", txt.getStyle())
                    txtObj.addElement(span)

                nodeContainer.addElement(txtObj)
            else:
                raise Exception("unsupported value type")

            y = y + lineHeight;

        return nodeContainer;

    #pseudo static method
    def getNodeHeight(self, node):
        lines = self.__createLines(node['value']);
        return self.__determineContainterHeight(lines);
