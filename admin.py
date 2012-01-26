#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.gis import admin
from django.utils.translation import ugettext as _
from django.db.models.loading import get_model

#from reversion import helpers

Modul = get_model('source','modul')
Parameter = get_model('source','parameter')
DataType = get_model('source','datatype')
Repository = get_model('source','repository')
CodeLanguage = get_model('source','codelanguage')
Package = get_model('source','package')

class ModulAdmin(admin.ModelAdmin):
    list_display = ('name','repository','get_parsed_descr','user','code_language','get_calls', 'get_called_by',)
    list_filter = ('repository','code_language')
    filter_horizontal = ['depencencys', 'input_params', 'output_params']
    search_fields = ['name', 'code_description', 'code',]
    radio_fields = {'repository': admin.HORIZONTAL}
    #list_editable = ('repository',)
    #class Media:
    #    js = ('js/tiny_mce/tiny_mce.js',
    #          'g2007.ch/js/textareas.js',)

class ParameterAdmin(admin.ModelAdmin):
    list_display = ('key','value','datatype',)
    list_filter = ('datatype',)
    
class DataTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    list_filter = ('type',)

class RepositoryAdmin(admin.ModelAdmin):
    list_diplay = ('name', 'slug', 'user',)
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('user',)

class CodeLanguageAdmin(admin.ModelAdmin):
    list_diplay = ('lang',)
    
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name','slug',)
    prepopulated_fields = {"slug": ("name",)}
    
admin.site.register(Modul, ModulAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(DataType, DataTypeAdmin)
admin.site.register(Repository, RepositoryAdmin)
admin.site.register(CodeLanguage, CodeLanguageAdmin)
admin.site.register(Package, PackageAdmin)

#helpers.patch_admin(Modul)
#helpers.patch_admin(Parameter)
#helpers.patch_admin(DataType)
#helpers.patch_admin(Repository)
#helpers.patch_admin(CodeLanguage)
#helpers.patch_admin(Package)
