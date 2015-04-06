#!/usr/bin/env python
'''
Created on 5 Apr 2015

@author: ppeter
'''
if __name__ == '__main__':
    pass

import argparse
import xml.etree.ElementTree as XML

def translateNodeValue(node, attributeName, translation):
    value = float(node.get(attributeName))
    value += translation
    node.set(attributeName, str(value))

def translateNodeChildren(node, childSelector, attributes):
    for child in node.iter(childSelector):
        for (attributeName, attributeTranslation) in attributes:
            translateNodeValue(child, attributeName, attributeTranslation)


parser = argparse.ArgumentParser(description='Profile xcode build run')
parser.add_argument('-i', dest='inputName', action='store', help='input file name', default='input.brd')
parser.add_argument('-o', dest='outputName', action='store', help='output file name', default='output.brd')
parser.add_argument('-x', dest='x', action='store', help='translation in x direction', default=0, type=float)
parser.add_argument('-y', dest='y', action='store', help='translation in y direction', default=0, type=float)
args = parser.parse_args()

tree = XML.parse(args.inputName)
root = tree.getroot()

#Convert plain wires
plain = root.find(".//plain")
translateNodeChildren(plain, 'wire', [('x1', args.x), ('y1', args.y), ('x2', args.x), ('y2', args.y)])
translateNodeChildren(plain, 'text', [('x', args.x), ('y', args.y)])
translateNodeChildren(plain, 'hole', [('x', args.x), ('y', args.y)])

#Convert elements
for element in root.findall('.//element'):
    translateNodeChildren(element, 'attribute', [('x', args.x), ('y', args.y)])
    translateNodeValue(element, 'x', args.x)
    translateNodeValue(element, 'y', args.y)

#Convert signals
for element in root.findall('.//signal'):
    translateNodeChildren(element, 'wire', [('x1', args.x), ('y1', args.y), ('x2', args.x), ('y2', args.y)])
    translateNodeChildren(element, 'via', [('x', args.x), ('y', args.y)])


#write result back
tree.write(args.outputName)
