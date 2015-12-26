import os, sys, re
from ec import *
from ecResponse import *

class ecSchedules(ElectricCommander, ecResponse):
	def __init__(self, user, passwd, server='ectesthost.usd.lab.emc.com', port=8000):
		super(ecSchedules, self).__init__(server=server, port=port, secure=False)
		self.login(user, passwd)

	def getSchedulesState(self, projectName):
		xmlStr = self.issueRequest('getSchedules',{'projectName':projectName})
		scheduleNodes = self.transXml(xmlStr, tag='schedule', isFirst=False)
		scheduleData = {}
		for scheduleNode in scheduleNodes:
			scheduleName = self.getNodeVal(scheduleNode, 'scheduleName')
			scheduleDisabled = 'true' if self.getNodeVal(scheduleNode, 'scheduleDisabled')=='0' else 'false'
			scheduleData[scheduleName] = scheduleDisabled
		return scheduleData

	def enableSchedule(self, projectName, scheduleName, state):
		arguments = {
			'projectName' : projectName,
			'scheduleName' : scheduleName,
			'scheduleDisabled' : '0' if state=='true' else '1'
		}
		xmlStr = self.issueRequest('modifySchedule', arguments)

def writeData(fileName, data):
	with open(fileName, 'w') as f:
		f.write(str(data))

def reset(ec, projectName, fileName, trunoffAll):
	data = {}
	with open(fileName, 'r') as f:
		data = eval(f.read())

	for scheduleName, state in data.items():
		state = 1 if trunoffAll=='1' else state
		ec.enableSchedule(projectName, scheduleName, state)

if __name__ == '__main__':
	operate = sys.argv[1]
	fileName = 'ec.schedule'
	projectName = 'EMSD_Common_data'
	ec = ecSchedules('fur5', 'YY001gg002', server='echost.usd.lab.emc.com')
	if operate == 'get':
		data = ec.getSchedulesState(projectName)
		writeData(fileName, data)
	else:
		reset(ec, projectName, fileName, sys.argv[2])
