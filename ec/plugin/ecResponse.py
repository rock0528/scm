import os, sys, re
from xml.dom import minidom

class ecResponse(object):
	def __init__(self):
		pass

	def transXml(self, xmlStr, tag='propertySheet', isFirst=True):
		root = minidom.parseString(xmlStr).documentElement
		childNodes = root.getElementsByTagName('response')[0].childNodes
		nodes = self.getNodesByTag(childNodes, tag=tag)
		return nodes[0] if isFirst else nodes

	def getResponseNode(self, xmlStr):
		root = minidom.parseString(xmlStr).documentElement
		return root.getElementsByTagName('response')[0]

	def getNodesByTag(self, nodes, tag='propertySheet'):
		return [node for node in nodes if node.nodeName==tag]

	def getNodeVal(self, xmlObj, nodeName='value'):
		xml =  self.transXml(xmlObj) if isinstance(xmlObj, str) else xmlObj
		val = ''
		for node in xml.childNodes:
			if node.nodeName == nodeName:
				val = node.firstChild.nodeValue if node.childNodes else ''
				break
		return val

	def getElementsByTag(self, parentNode, tag):
		return parentNode.getElementsByTagName(tag)