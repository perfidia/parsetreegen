'''
Created on Mar 9, 2012

@author: hilfman
'''

import parsetreegen

nodeL1C1 = {
        'type': 'node',
        'id': 'L1C1',
        'value': [
            'Node type:[br][b]Concat[/b]',
            0, # non text is a separator
            'Attribute(s):',
            'asdf[s]na[b]me[i] =[/i] "[/b]Elem[/s]entType"',
            'duplicated = false',
            'length = 11'
        ],
        'children': [],
}

nodeRoot = {
        'type': 'node',
        'id': 'root',
        'value': [
            'asd[br]f[s]na[b]me[i] =[/i] "[/b]Elem[/s]entType"',
            0, # non text is a separator
            'Attribute(s):',
            'name = "ElementID"',
            'duplicated = false',
            'length = 9'
        ],
        'children': [nodeL1C1],
}

print '\n\nSVG XML output: \n\n' + parsetreegen.as_svg(nodeRoot, "testSVG.svg", None)