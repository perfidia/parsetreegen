# -*- coding: utf-8 -*-

__all__ = ["defaultConf", "read", "to_svg", "to_text"]

'''Parse Tree Generator

Created on Apr 29, 2011

@author: Bartosz Achimowicz

Supported BBCODEs:
Tag         Description   Example
[b]	        bold          [b]example[/b]
[i]	        italic        [i]example[/i]
[s]         strikethrough [s]example[/s]
[u]	        underline     [u]example[/u]
[color=red]	color         [color=red]red example[/color]
[br]        new line
'''

import re
import json

import svgcreator

# Default configuration for the generator
defaultConf = {
        # jednosta jest px
        'frame': {                    # ramka zawierajaca tekst
            'thickness': 2,           # grubosc ramki
            'padding': 5,             # odstep pomiedzy ramka i tekstem
            'width': 300,             # szerokosc ramki
            'horizontalOffset': 50,   # odstep miedzy ramkami w pionie
            'verticalOffset': 50,     # odstep miedzy ramkami w poziomie
            'separator': {            # seperator w ramce
                'width': 1,           # grubość linni
            },
            'font': {                 # czcionka
                'name': 'Arial',      # rodzaj czcionki
                'size': 10,           # rozmiar czcionki
                'align': 'justified', # left, right, justified ... UNSUPPORTED
            },
        },
        'connection': {               # polaczenie pomiedzy ramkami
            'thickness': 2,           # grubosc linii
            'marker': 'normal',       # rodzaj grotu: small, normal, large .. UNSUPPORTED
            'style':  'straight',     # pattern linii przerywanej: straight, dashed, dotted
        },
        'reference': {                # referencja do innej ramki
            'thickness': 2,           # grubosc linii
            'marker': 'normal',       # rodzaj grotu: small, normal, large
            'style': 'dashed',        # pattern linii przerywanej: straight, dashed, dotted
            'color': 'grey',          # TODOs
        }
}

def read(filename):
    '''Read file and return data representation

    @param filename file with a data for a parse tree (similar to json)

    @return data representation
    '''

    fd = open(filename, 'rb')
    data = fd.read();
    data = re.sub("#.*\n", "", data);
    data = re.sub("\s", "", data);
    nodes = re.findall("\w+\s*=\s*{.*?}", data);
    fd.close()

    replacements = dict();

    # There are two type of input files:
    # - with defined nodes
    # - plain json file
    
    # handle file with defined nodes
    for node in nodes:
        match = re.search("\w+", node);
        nodeName = match.string[match.start():match.end()];

        match = re.search("{.*?}", node)
        nodeContent = match.string[match.start():match.end()];

        match = re.search("'children':\[.*?\]", nodeContent);

        if match != None:
            childrenSection = match.string[match.start():match.end()];

            for key in replacements.iterkeys():
                if re.match(".*" + key + ".*", childrenSection):
                    replacements[key]['child'] = True;
                childrenSection = re.sub(key, "replacements['" + key + "']['node']", childrenSection);

            nodeContent = re.sub("'children':\[.*?\]", childrenSection, nodeContent);

        n = eval(nodeContent);

        replacements[nodeName] = dict();
        replacements[nodeName]['child'] = False;
        replacements[nodeName]['node'] = n

    for value in replacements.itervalues():
        if not value['child']:
            return value['node'];

    # handle plain json
    if len(nodes) == 0:
        return json.loads(data)

    raise Exception("Did not find root node");

def to_svg(data, filename=None, conf=None):
    '''Generate svg image for provided data

    @param data data representation
    @param filename place where to store the image; if None then do not save anything
    @param conf configuration

    @return SVG representation of file
    '''
    
    if conf != None:
        svgCreator = svgcreator.SVGTreeCreator(conf)
    else:
        svgCreator = svgcreator.SVGTreeCreator(defaultConf)

    svgCreator.prepareTree(data)
    # svgCreator.determineFramesPositions(data)
    if filename != None:
        svgCreator.createSVGFile(filename)

    return svgCreator.prepareXML()

def __partial(data, indent, nodes):
    result = ''

    spacing = ' ' * indent

    if data['type'] == 'node':
        nodes[data['id']] = data

        for line in data['value']:
            if isinstance(line, int):
                result += spacing + '-' * 10 + '\n'
            elif isinstance(line, basestring):
                result += spacing + line + '\n'
            else:
                raise Exception("unsupported value type")

        result += '\n'

        if data.has_key('children'):
            for child in data['children']:
                result += __partial(child, indent + 5, nodes)
    elif data['type'] == 'reference':
        result += spacing + '#reference ' + data['value'] + '\n'
        result += __partial(nodes[data['value']], indent, nodes)
    else:
        raise Exception("unsupported node type")

    return result

def to_text(data):
    '''Pretty print

    @param data input data

    @return string
    '''

    return __partial(data, 0, {})
