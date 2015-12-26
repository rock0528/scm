import os, sys, re
from ec import *
from ecResponse import *

class ecProperties(ElectricCommander, ecResponse):
	def __init__(self, user, passwd, server='ectesthost.usd.lab.emc.com', port=8000):
		super(ecProperties, self).__init__(server=server, port=port, secure=False)
		self.login(user, passwd)

	def getPropertySheet(self, pNode):
		return self.getNodesByTag(pNode.childNodes)

	def __getPS(self, psNode):
		data = {}
		for pNode in psNode.childNodes:
			if pNode.nodeName != 'property':  continue
			name = self.getNodeVal(pNode, nodeName='propertyName')
			childPSs = self.getPropertySheet(pNode)
			if childPSs:
				data[name] = map(self.__getPS, childPSs)[0]
			else:
				val = self.getNodeVal(pNode)
				data[name] =val
		return data

	def getProperty(self, propertyName):
		xmlStr = self.issueRequest('getProperty',{'propertyName':propertyName})
		root = self.transXml(xmlStr, tag='property')
		return root.getElementsByTagName('value')[0].firstChild.nodeValue

	def getProperties(self, path, recurse='true'):
		xmlStr = self.issueRequest('getProperties',{'path':path, 'recurse':recurse});
		root = self.transXml(xmlStr)
		return self.__getPS(root)

	def createProperties(self, path, propDict):
		for propName, value in propDict.items():
			if isinstance(value, dict):
				self.createProperties('{0}/{1}'.format(path, propName), value)
			else:
				self.issueRequest('createProperty',{'propertyName':'{0}/{1}'.format(path, propName), 'value':value})

	def deleteProperties(self, propList):
		if isinstance(propList, str):
			self.issueRequest('deleteProperty',{'propertyName': propList})
			return
		for propName in propList:
			self.issueRequest('deleteProperty',{'propertyName': propName})

	def copyProperties(self, source, dest):
		properties = self.getProperties(source)
		self.createProperties(dest, properties)

if __name__ == '__main__':
	ec = ecProperties('fur5', 'YY001gg002')
	# print ec.getProperties('/projects/EMSD_VNX_Rockies_data/', recurse='true')
	# ec.createProperties('/projects/EMSD_VNX_Rockies_data', {'rock/hello2':'1231'})
	# ec.deleteProperties('/projects/EMSD_VNX_Rockies_data/', ['rock'])
	# ec.copyProperties('/projects/EMSD_VNX_Rockies_data/upc-controlstation-mcs/Switches', \
	# 					'/projects/EMSD_VNX_Rockies_data/upc-controlstation-mcs/Switches_bk')
	print ec.getProperty('/jobs/356246/log')
	# for switch, val in ec.getProperties('/projects/EMSD_VNX_Rockies_data/upc-Rockies/Switches').items():
	# 	print switch
	# ec = ecProperties('fur5', 'YY001gg001', server='echost.usd.lab.emc.com')
	# ec.deleteProperties('/projects/EMSD_VNX_Rockies_data/upc-controlstation-mcs/Switches')
	# ec.copyProperties('/projects/EMSD_VNX_Rockies_data/upc-nextcontrolstation-mcs/Switches', '/projects/EMSD_VNX_Rockies_data/upc-controlstation-mcs/Switches')
	