'''
Created on Apr 29, 2011

@author: Bartosz Achimowicz
'''

import parsetreegen

nodeL1C1SA2 = {
		'type': 'node',
		'id': 'nodeL1C1SA2',
		'value': [
			'Node type:[br][b]Range[/b]',
			0, # non text is a separator
			'Attribute(s):',
			'min = \'A\'',
			'max = \'Z\'',
			'length = 3'
		],
}

nodeL1C1SA1 = {
		'type': 'node',
		'id': 'nodeL1C1SA1',
		'value': [
			'Node type:[br][b]InCharClass[/b]',
			0, # non text is a separator
			'Attribute(s):',
			'duplicated = false',
			'length = 3'
		],
		'children': [nodeL1C1SA2],
}

nodeL1C1SB3 = {
		'type': 'node',
		'id': 'nodeL1C1SB3',
		'value': [
			'Node type:[br][b]Range[/b]',
			0, # non text is a separator
			'Attribute(s):',
			'min = 0',
			'max = 9',
			'length = 3'
		],
}

nodeL1C1SB2 = {
		'type': 'node',
		'id': 'nodeL1C1SB2',
		'value': [
			'Node type:[br][b]InCharClass[/b]',
			0, # non text is a separator
			'Attribute(s):',
			'duplicated = true',
			'length = 3'
		],
		'children': [nodeL1C1SB3],
}

nodeL1C1SB1 = {
		'type': 'node',
		'id': 'nodeL1C1SB1',
		'value': [
			'Node type:[br][b]ExactQuantity[/b]',
			0, # non text is a separator
			'Attribute(s):',
			'value = 2',
			'duplicated = false',
			'length = 3'
		],
		'children': [nodeL1C1SB2],
}

nodeL1C3A1 = {
		'type': 'reference',
		'id': 'nodeL1C3A1',
		'value': 'nodeL1C1SB2',
}

nodeL1C1 = {
		'type': 'node',
		'id': 'L1C1',
		'value': [
			'Node type:[br][b]Concat[/b]',
			0, # non text is a separator
			'Attribute(s):',
			'name = "ElementType"',
			'duplicated = false',
			'length = 11'
		],
		'children': [nodeL1C1SA1, nodeL1C1SB1],
}

nodeL1C2 = {
		'type': 'node',
		'id': 'L1C2',
		'value': [
			'Node type:[br][b]Char[/b]',
			0, # non text is a separator
			'Attribute(s):',
			'value = \'-\'',
			'length = 1'
		],
}

nodeL1C3 = {
		'type': 'node',
		'id': 'L1C3',
		'value': [
			'Node type:[br][b]ExactQuantity[/b]',
			0, # non text is a separator
			'Attribute(s):',
			'value = 5',
			'duplicated = true',
			'length = 3'
		],
		'children': [nodeL1C3A1],
}

nodeL1C4 = {
		'type': 'node',
		'id': 'L1C4',
		'value': [
			'Node type:[br][b]Char[/b]',
			0, # non text is a separator
			'Attribute(s):',
			'value = \'-\'',
			'length = 1'
		],
}

nodeL1C5 = {
		'type': 'reference',
		'value': 'L1C3',
}

nodeRoot = {
		'type': 'node',
		'id': 'root',
		'value': [
			'Node type:[br][b]Concat[/b]',
			0, # non text is a separator
			'Attribute(s):',
			'name = "ElementID"',
			'duplicated = false',
			'length = 9'
		],
		'children': [nodeL1C1, nodeL1C2, nodeL1C3, nodeL1C4, nodeL1C5],
}

print nodeRoot
print parsetreegen.as_text(nodeRoot)
print '\n\nSVG XML output: \n\n' + parsetreegen.as_svg(nodeRoot, "testSVG.svg", None)
print 'testCommit'