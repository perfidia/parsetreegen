# -*- coding: utf-8 -*-

'''
Created on Apr 29, 2011

@author: Bartosz Achimowicz

BBCODE:
Znacznik	Opis	Przykład
[b]	tekst pogrubiony	[b]przykład[/b]
[i]	tekst pochyły	[i]przykład[/i]
[s]	tekst przekreślony	[s]przykład[/s]
[u]	tekst podkreślony	[u]przykład[/u]
[color=red]	kolorowy tekst 	[color=red]czerwony przykład[/color]

[br] new line

'''

import svgcreator

defaultConf = {
		# jednosta jest px
		'frame': {              # ramka zawierajaca tekst
			'thickness': 1,     # grubosc ramki
			'padding': 10,      # odstep pomiedzy ramka i tekstem
			'width': 600,       # szerokosc ramki
			'horizontalOffset': 100, # odstep miedzy ramkami w pionie
			'verticalOffset': 100, # odstep miedzy ramkami w poziomie
			'separator': {      # seperator w ramce
				'width': 1,     # grubość linni
			},
			'font': {                 # czcionka
				'name': 'Arial',      # rodzaj czcionki
				'size': 10,           # rozmiar czcionki
				'align': 'justified', # left, right, justified
			},
		},
		'connection': {         # polaczenie pomiedzy ramkami
			'thickness': 2,         # grubosc linii
			'marker': 'normal', # rodzaj grotu: small, normal, large
			'style':  'straight', # pattern linii przerywanej: straight, dashed, dotted
		},
		'reference': {          # referencja do innej ramki
			'thickness': 2,     # grubosc linii
			'marker': 'normal', # rodzaj grotu: small, normal, large
			'style':  'dashed', # pattern linii przerywanej: straight, dashed, dotted
		},
}

def read(filename):
	'''
	Read file and return data representation

	@param filename: file with a data for a parse tree (similar to json)

	@return: data representation
	'''
	return None

def as_svg(data, filename = None, conf = None):
	'''
	Generate svg image for provided data

	@param data: data representation
	@param filename: place where to store the image; if None then do not save anything
	@param conf: configuration

	@return: SVG representation of file
	'''
	if conf != None:
		svgCreator = svgcreator.SVGTreeCreator(conf)
	else:
		svgCreator = svgcreator.SVGTreeCreator(defaultConf)
	svgCreator.prepareTree(data)
#	svgCreator.determineFramesPositions(data)
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
			elif isinstance(line, str):
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

def as_text(data):
	'''
	Pretty print

	@param data: input data

	@return: string
	'''

	return __partial(data, 0, {})
