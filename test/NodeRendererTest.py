'''
Created on Mar 9, 2012

@author: hilfman
'''

import parsetreegen

nodeRoot = {
        'type': 'node',
        'id': 'root',
        'value': [
            '1',
            0, # non text is a separator
            'Attribute(s):',
            0,
            'name = "ElementID"',
            'duplicated = false',
            'length = 9'
        ],
        'children': [],
}

print '\n\nSVG XML output: \n\n' + parsetreegen.as_svg(nodeRoot, "testNodeRenderer.svg", None)