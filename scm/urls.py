"""scm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from jsonrpc import jsonrpc_site
import ec.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ec/properties$', 'ec.views.properties'),
    url(r'^ec/schedules$', 'ec.views.schedules'),
    url(r'^json/', jsonrpc_site.dispatch, name="jsonrpc_mountpoint"),
    url(r'^json/(?P<method>[a-zA-Z0-9.-_]+)$', jsonrpc_site.dispatch),
]
