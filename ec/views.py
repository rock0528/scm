from django.shortcuts import render, render_to_response
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from models import *
from api import *

@never_cache
def properties(request):
    hosts = map(lambda x: x.host_name, EC_Host.objects.all())
    projects = map(lambda x: x.project_name, EC_Project.objects.filter(project_type=1))
    return render_to_response("ec_properties.html", {'HOSTS' : hosts, 'PROJECTS' : projects})

@never_cache
def schedules(request):
    hosts = map(lambda x: x.host_name, EC_Host.objects.all())
    projects = map(lambda x: x.project_name, EC_Project.objects.filter(project_type=1))
    return render_to_response("ec_schedules.html", {'HOSTS' : hosts, 'PROJECTS' : projects})
