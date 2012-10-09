'''
Created on Mar 8, 2012

@author: Tomasz Hulak
'''

class BBCText:
    def __init__(self, bold, italics, strike, underline, color, text):
        self.__isBold = bold;
        self.__isItalics = italics;
        self.__isStrike = strike;
        self.__isUnderline = underline;
        self.__color = color;
        self.__text = text;

    def isBold(self):
        return self.__isBold;

    def isItalics(self):
        return self.__isItalics;

    def isStrike(self):
        return self.__isStrike;

    def isUnderline(self):
        return self.__isUnderline;

    def getColor(self):
        return self.__color;

    def getText(self):
        return self.__text;

    def getStyle(self):
        style = "";
        if self.isBold():
            style = style + "font-weight: bold; ";
        if self.isItalics():
            style = style + "font-style: italic; ";
        if self.isStrike():
            style = style + "text-decoration: line-through; ";
        if self.isUnderline():
            style = style + "text-decoration : underline; ";

        style = style + "color: #" + self.getColor() + ";";

        return style;

    #####
    # Setters create new object to make this class immutable.
    #####

    def setBold(self, isBold):
        return BBCText(isBold, self.__isItalics, self.__isStrike, self.__isUnderline, self.__color);

    def setItalics(self, isItalics):
        return BBCText(self.__isBold, isItalics, self.__isStrike, self.__isUnderline, self.__color);

    def setStrike(self, isStrike):
        return BBCText(self.__isBold, self.__isItalics, isStrike, self.__isUnderline, self.__color);

    def setUnderline(self, isUnderline):
        return BBCText(self.__isBold, self.__isItalics, self.__isStrike, isUnderline, self.__color);

    def setColor(self, color):
        return BBCText(self.__isBold, self.__isItalics, self.__isStrike, self.__isUnderline, color);
