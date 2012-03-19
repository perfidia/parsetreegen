# -*- coding: utf-8 -*-

'''
Created on Mar 8, 2012

@author: Tomasz Hulak
'''

from BBCText import BBCText;
import re;

class BBCodeTag:
    def __init__(self, openTag, close, pattern):
        self.__open = openTag;
        self.__close = close;
        self.__pattern = pattern;
    
    def getOpenTag(self):
        return self.__open;
    
    def getCloseTag(self):
        return self.__close;
    
    def getPattern(self):
        return self.__pattern;
    
    def getOpenTagEscaped(self):
        return self.__escapeTag(self.getOpenTag());
        
    def getCloseTagEscaped(self):
        return self.__escapeTag(self.getCloseTag());
        
    def __escapeTag(self, tag):
        tag = tag.replace("[", "\[");
        tag = tag.replace("]", "\]");
        return tag;

class BBCodeBold(BBCodeTag):
    def __init__(self):
        BBCodeTag.__init__(self, "[b]", "[/b]", "\[b\].*?\[/b\]");
    
class BBCodeItalic(BBCodeTag):
    def __init__(self):
        BBCodeTag.__init__(self, "[i]", "[/i]", "\[i\].*?\[/i\]");
        
class BBCodeUnderline(BBCodeTag):
    def __init__(self):
        BBCodeTag.__init__(self, "[i]", "[/i]", "\[i\].*?\[/i\]");
        
class BBCodeStrike(BBCodeTag):
    def __init__(self):
        BBCodeTag.__init__(self, "[s]", "[/s]", "\[s\].*?\[/s\]");
        
class BBCodeColor(BBCodeTag):
    def __init__(self):
        BBCodeTag.__init__(self, "\[color=[a-zA-Z]+\]", "\[/color\]", "\[color=[a-zA-Z]+\].*?\[/color\]");
        
    def getOpenTagEscaped(self):
        return self.getOpenTag();
        
    def getCloseTagEscaped(self):
        return self.getCloseTag();

class BBCodeResolver:
    
    def __init__(self):
        self.__mapping = dict();
        self.__mappingIndex = 1;
        
        self.__BOLD_FLAG = 'b';
        self.__ITALIC_FLAG = 'i';
        self.__UNDERLINE_FLAG = 'u';
        self.__STRIKE_FLAG = 's';
        self.__COLOR_FLAG = 'c=';
    
    def resolveString(self, text):
        
        if isinstance(text, str):
            lines = text.split("[br]");
            convertedLines = [];
            
            result = [];
            
            for line in lines:
                line = self.__generateBBCReplacements(line);
                convertedLines.append(line);
            
            self.__resolveMappings();
            
            for line in convertedLines:
                result.append(self.getBBCLine(line));
            
            return result;
        else:
            return text;
    
    def __generateBBCReplacements(self, line):
        line = self.__divideText(line, BBCodeBold(), self.__BOLD_FLAG);
        line = self.__divideText(line, BBCodeStrike(), self.__STRIKE_FLAG);
        line = self.__divideText(line, BBCodeItalic(), self.__ITALIC_FLAG);
        line = self.__divideText(line, BBCodeUnderline(), self.__UNDERLINE_FLAG);
        line = self.__divideText(line, BBCodeColor(), self.__COLOR_FLAG);
        
        return line;
        
    def __divideText(self, string, tag, flag):
        
        strLen = len(string);
        match = re.search(tag.getPattern(), string);
        while match != None:
            
            before = match.string[0:match.start()];
            after = match.string[match.end(): strLen];
            
            found = match.string[match.start():match.end()];
            
            found = re.sub(tag.getOpenTagEscaped(), "", found);
            found = re.sub(tag.getCloseTagEscaped(), "", found);
            
            replacement = self.__createNewReplacement(flag);
            
            self.__mapping[replacement] = dict();
            self.__mapping[replacement]['value'] = found;
            self.__mapping[replacement]['checked'] = False;
            
            string = before + replacement + after;

            match = re.search(tag.getPattern(), string);
            
        return string;
            
    def __resolveMappings(self):
        for key in self.__mapping.keys():
            if not self.__mapping[key]['checked']:
                self.__mapping[key]['value'] = self.__generateBBCReplacements(self.__mapping[key]['value']);
                self.__mapping[key]['checked'] = True;
                print self.__mapping[key]['value']
    
    #unused        
    def __mappingChecked(self):
        for key in self.__mapping.keys():
            if not self.__mapping[key]['checked']:
                return False
        return True;
    
    def getBBCLine(self, lineString):
        return self.__getBBCLine(lineString, [], "0");
    
    def __getBBCLine(self, lineString, types, prevColor):
        texts = [];
        
        lineLen = len(lineString);
        lastIndex = 0;
        pattern = "{\$[0-9]+([bisu]|(c=[a-zA-Z]+))}";
        match = re.search(pattern, lineString);
        color = None;
        
        while match != None:
            if match.start() > lastIndex:
                plainText = match.string[lastIndex:match.start()]
                texts.append(self.__toBBCText(plainText, types, color));
            id = match.string[match.start():match.end()];
            type = self.__resolveMappingType(id);
            typesTemp = list(types);
            typesTemp.append(type);
            
            lastIndex = match.end();
            
            if type == 'c':
                match = re.search("[a-zA-Z][a-zA-Z]+");
                color = match.string[match.start():match.end()];
                
            if color == None:
                color = prevColor;
            
            innerResult = self.__getBBCLine(self.__mapping[id]['value'], typesTemp, color);
            for element in innerResult:
                texts.append(element);
            
            match = re.search(pattern, match.string[match.end():lineLen]);
            
        if lastIndex != lineLen:
            texts.append(self.__toBBCText(lineString[lastIndex:lineLen], types, color))
            
        return texts;
            
            
            
    def __toBBCText(self, string, types, color):
        isBold = False;
        isItalic = False;
        isStrike = False;
        isUnderline = False;
        color = self.__resolveColor(color);
        
        if types.__contains__('b'):
            isBold = True;
        if types.__contains__('i'):
            isItalic = True;
        if types.__contains__('s'):
            isStrike = True;
        if types.__contains__('u'):
            isUnderline = True;
                
        return BBCText(isBold, isItalic, isStrike, isUnderline, color, string);
        
        
            
    def __resolveColor(self, color):
        if color != None:
            color = color.lower();
            if color == 'red':
                return "1";
            elif color == 'blue':
                return "2";
            elif color == 'black':
                return "3";
            elif color == 'white':
                return "4";
            elif color == 'pink':
                return "5";
            elif color == 'brown':
                return "6";

        return "7";
            
    def __resolveMappingType(self, mapping):
        return re.sub("{\$[0-9]+", "", mapping)[0];
    
    '''
    Replacements for BBCode tags. 
    
    For example:
    "[s]Foo [b]bar[/b][/s]" would create
    "[s]Foo {$1b}[/s]", where {$1b} is replacement for
        "[b]bar[/b]".
    '''
    def __createNewReplacement(self, flag):
        result = "{$" + str(self.__mappingIndex) + flag + "}";
        self.__mappingIndex = self.__mappingIndex + 1;
        return result;
        
