import os, sys, re
from ec import *
from ecResponse import *

class ecJobs(ElectricCommander, ecResponse):
	def __init__(self, user, passwd, server='ectesthost.usd.lab.emc.com', port=8000):
		super(ecJobs, self).__init__(server=server, port=port, secure=False)
		self.login(user, passwd)

	def runProcedure(self, projectName, procedureName, parameters={}):
		arguments = {'projectName' : projectName, 
					'procedureName' : procedureName,
					'actualParameter' : parameters}
		xmlStr = self.issueRequest('runProcedure',arguments)
		root = self.transXml(xmlStr, tag='jobId')
		jobId = root.firstChild.nodeValue
		return jobId

	def getJobStatus(self, jobId):
		xmlStr = self.issueRequest('getJobStatus',{'jobId':jobId})
		responseNode = self.getResponseNode(xmlStr)
		status = self.getNodeVal(responseNode, nodeName='status')
		outcome = self.getNodeVal(responseNode, nodeName='outcome')
		return (status, outcome)

	def abortJob(self, jobId, force='true'):
		xmlStr = self.issueRequest('abortJob',{'jobId':jobId, 'force':force})
    
	def deleteJob(self, jobId):
		xmlStr = self.issueRequest('deleteJob',{'jobId':jobId})

if __name__ == '__main__':
	ec = ecJobs('fur5', 'YY001gg002')
	# jobId = ec.runProcedure('sandbox_RockFu', 'checkAccurevUpgradeOnWindow', \
	# 		{'actualParameterName ' : 'resource', 'value' : 'Automatos_17.172'})
	# print jobId
	print ec.getJobStatus('356228')