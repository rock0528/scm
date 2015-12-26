import os, sys, re
sys.path.extend(['../', '../libs', '../scm'])
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()
import datetime
from jsonrpc import jsonrpc_method
from plugin.ecProperties import ecProperties
from plugin.ecSchedules import ecSchedules
from ec.models import *

def get_host_info(host_name):
    record = EC_Host.objects.filter(host_name=host_name)[0]
    return(record, record.user, record.password)

def get_project_info(project_name):
    record = EC_Project.objects.filter(project_name=project_name)[0]
    return record

@jsonrpc_method('ec.search_property(String, String, String)', validate=True)
def search_property(request, host_name, project_name, property_name):
    (record, user, password) = get_host_info(host_name)
    ec = ecProperties(user, password, server=host_name)
    project_name = '%s/BuildSetup' %project_name if project_name=='EMSD_Common_data' else project_name
    project_path = '/projects/%s' %(project_name)
    data = ec.getProperties(project_path, recurse='true')
    result_list = []
    get_search_content(data, property_name, project_path, result_list)
    return result_list

def get_search_content(data, property_name, parent_path, result_list):
    root_path = parent_path
    for name, value in data.items():
        if isinstance(value, dict):
            parent_path = '%s/%s' %(root_path, name)
            if re.search(property_name, name, re.I):
                result_list.append('%s|%s'%(parent_path, ''))
            get_search_content(value, property_name, parent_path, result_list)
        else:
            parent_path = '%s/%s' %(root_path, name)
            if re.search(property_name, parent_path, re.I):
                result_list.append('%s|%s'%(parent_path, value))

@jsonrpc_method('ec.get_schedules(String, String)', validate=True)
def get_schedules(request, host_name, project_name):
    (backup_row, user, password) = get_schedule_backup_info(host_name, project_name)
    if not backup_row:
        return None
    data = {}
    for row in EC_Schedule.objects.filter(backup=backup_row):
        data[row.schedule_name] = row.schedule_enable
    return {'backup_time' : backup_row.backup_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_restore' : backup_row.is_restore,
            'schedules' : data }

def get_schedule_backup_info(host_name, project_name, is_create_backup=False):
    (host_row, user, password) = get_host_info(host_name)
    project_row = get_project_info(project_name)
    row = EC_Schedule_Backup.objects.filter(host=host_row, project=project_row)
    if not row:
        if is_create_backup:
            row = EC_Schedule_Backup(host=host_row, project=project_row, backup_time=datetime.datetime.now())
            row.save()
    else:
        row = row[0]
    return (row, user, password)

@jsonrpc_method('ec.backup_schedules(String, String)', validate=True)
def backup_schedules(request, host_name, project_name):
    (backup_row, user, password) = get_schedule_backup_info(host_name, project_name, is_create_backup=True)
    EC_Schedule.objects.filter(backup=backup_row).delete()
    ec = ecSchedules(user, password, server=host_name)
    for name, state in ec.getSchedulesState(project_name).items():
        record = EC_Schedule(   backup=backup_row,
                                schedule_name=name,
                                schedule_enable=state
                                )
        record.save()
        if state == 'true':
            ec.enableSchedule(project_name, name, 'false')
    backup_row.backup_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    backup_row.is_restore=False
    backup_row.save()
    return get_schedules(request, host_name, project_name)

@jsonrpc_method('ec.restore_schedules(String, String)', validate=True)
def restore_schedules(request, host_name, project_name):
    (backup_row, user, password) = get_schedule_backup_info(host_name, project_name)
    ec = ecSchedules(user, password, server=host_name)
    for row in EC_Schedule.objects.filter(backup=backup_row):
        ec.enableSchedule(project_name, row.schedule_name, row.schedule_enable)
    backup_row.is_restore=True
    backup_row.save()
    return get_schedules(request, host_name, project_name)

if __name__ == '__main__':
    # print search_property(None, 'ectesthost.usd.lab.emc.com', 'EMSD_Common_data/BuildSetup', 'ar')
    print backup_schedules(None, 'ectesthost.usd.lab.emc.com', 'EMSD_Common_data')
