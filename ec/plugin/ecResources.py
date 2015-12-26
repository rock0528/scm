import os, sys, re
from ec import *
from ecResponse import *

class ecJobs(ElectricCommander, ecResponse):
	def __init__(self, user, passwd, server='ectesthost.usd.lab.emc.com', port=8000):
		super(ecJobs, self).__init__(server=server, port=port, secure=False)
		self.login(user, passwd)

	def getResourcesInPool(self, pool):
		xmlStr = self.issueRequest('getResourcesInPool',{'pool':pool})
		resourceNodes = self.transXml(xmlStr, tag='resource', isFirst=False)
		resourceList = []
		for resourceNode in resourceNodes:
			stateNode = self.getElementsByTag(resourceNode, 'state')[0]
			state = stateNode.firstChild.nodeValue
			if state != 'alive':  continue
			resourceName = self.getNodeVal(resourceNode, 'resourceName')
			hostName = self.getNodeVal(resourceNode, 'hostName')
			resourceList.append((resourceName, hostName))
		return resourceList

	def getResourcePools(self):
		xmlStr = self.issueRequest('getResourcePools')
		poolNodes = self.transXml(xmlStr, tag='resourcePool', isFirst=False)
		poolsHash = {}
		for poolNode in poolNodes:
			resourcePoolName = self.getNodeVal(poolNode, 'resourcePoolName')
			resourceList = []
			for resourceNode in self.getElementsByTag(poolNode, 'resourcePoolName'):
				resourcePoolName = resourceNode.firstChild.nodeValue
				resourceList.append(resourcePoolName)
			poolsHash[resourcePoolName] = resourceList
		return poolsHash

if __name__ == '__main__':
	ec = ecJobs('fur5', 'YY001gg002', server='echost.usd.lab.emc.com')
	# print ec.getResourcesInPool('EMSD_Pool_Block_ENG')
	# for poolName in ec.getResourcePools():
	# 	print poolName
	pools = ['EMSD_Pool_VNXe_UEMCLI_RH32',
'EMSD_Pool_VNXe_UEMCLI_RH32_ENG',
'EMSD_Pool_VNXe_UEMCLI_RH32_RTM',
'EMSD_Pool_VNXe_UEMCLI_RH64',
'EMSD_Pool_VNXe_UEMCLI_RH64_ENG',
'EMSD_Pool_VNXe_UEMCLI_RH64_RTM',
'EMSD_Pool_VNXe_UEMCLI_SUSE10_64',
'EMSD_Pool_VNXe_UEMCLI_SUSE10_64_ENG',
'EMSD_Pool_VNXe_UEMCLI_SUSE10_64_RTM',
'EMSD_Pool_VNXe_UEMCLI_WIN',
'EMSD_Pool_VNXe_UEMCLI_WIN_ENG',
'EMSD_Pool_VNXe_UEMCLI_WIN_RTM',
'EMSD_Pool_ALL',
'EMSD_Pool_ALL_Unix',
'EMSD_Pool_ENAS_RTM'
			]
	for pool in pools:
		# print '='*10 + pool
		for resource in ec.getResourcesInPool(pool):
			# print '\t'.join(resource)
			print resource[0]