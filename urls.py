#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('karrie.django.source',
    url(r'^$', 
        'views.index', 
        name='source_index'),
        
    url(r'^package/(?P<slug>\w+)/',
        'views.package_details',
        name = 'source_package_details'),

    url(r'^modul/(?P<pk>\d+)$', 
        'views.mod_details',
        name ='source_modul_details'),
        
    url(r'^m/(?P<rep_slug>\w+)/(?P<name>\w+(?:\.\w+))$',
        'views.mod_named_details',
        name ='source_modul_named_details'),
 
    url(r'suche/$',
        'views.search',
        name = 'source_search'),
        
    url(r'^modultree/', 
        'views.modultree',
        name ='source_modultree'),
)
