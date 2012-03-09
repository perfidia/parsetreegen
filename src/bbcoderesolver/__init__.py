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
            
            result = [];
            
            for line in lines:
                line = self.__generateBBCReplacements(line);
                
                print line;
                #result.append(self.__getBBCLine(line));
            
            self.__resolveMappings();
            
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
        