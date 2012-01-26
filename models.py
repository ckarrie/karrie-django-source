#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
import re
from django.core.validators import RegexValidator

filename_regex = re.compile(r'\w+(?:\.\w+)$')
filename_validator = RegexValidator(filename_regex, _(u'Bitte in der Form <Dateiname>.<Dateiendung>'), 'invalid')

class Package(models.Model):
    name = models.CharField(max_length = 120, help_text = u'Paketname')
    slug = models.SlugField(unique = True, help_text = u'Eindeutige, URL-konforme Bezeichnung (Kleinschreibung)')
    description = models.TextField(verbose_name=u'Beschreibung', null=True, blank=True, help_text = u'Beschreibung des Pakets in HTML')
    reps = models.ManyToManyField('Repository', related_name='repositories', verbose_name='Repositories', help_text = u'Verknüpfte Repositories.')
    
    class Meta:
        ordering = ['name']
        verbose_name = u'Paket'
        verbose_name_plural = u'Pakete'
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('source_package_details', kwargs={'slug':self.slug})

class Repository(models.Model):
    name = models.CharField(max_length = 120, help_text = u'Name des Repositories')
    slug = models.SlugField(help_text = u'Eindeutige, URL-konforme Bezeichnung (Kleinschreibung)')
    last_modified = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, help_text = u'Zuständiger Benutzer')
    
    class Meta:
        ordering = ['name']
        verbose_name = u'Repository'
        verbose_name_plural = u'Repositories'
    
    def __unicode__(self):
        return self.name
    
    def get_moduletree_url(self):
        return reverse('source_modultree') + '#rep-%s' % self.slug
    
    def get_absolute_url(self):
        return self.get_moduletree_url()
    
class CodeLanguage(models.Model):
    lang = models.CharField(max_length = 220, help_text = u'Programmier- / Skriptsprache, Dateityp')
    
    class Meta:
        ordering = ['lang']
        verbose_name = u'Quelltextsprache'
        verbose_name_plural = u'Quelltextsprachen'
    
    def __unicode__(self):
        return self.lang
    
class DataType(models.Model):
    type = models.CharField(max_length = 120, help_text = u'Name des Datentyps')
    
    class Meta:
        ordering = ['type']
        verbose_name = u'Datentyp'
        verbose_name_plural = u'Datentypen'
        
    def __unicode__(self):
        return self.type
    
class Parameter(models.Model):
    key = models.CharField(max_length = 120, verbose_name = u'Variable', help_text = u'Parametername / Variablenname')
    value = models.CharField(max_length = 120, verbose_name = u'Beschreibung', help_text = u'Beschreibung Parameter / Variable')
    datatype = models.ForeignKey(DataType, verbose_name = u'Datentyp')
    
    class Meta:
        ordering = ['key']
        verbose_name = u'Parameter'
        verbose_name_plural = u'Parameter'

    def get_admin_url(self):
        return reverse('admin:source_parameter_change', args=(self.id,))
        
    def __unicode__(self):
        return u'%s: %s (%s)' %(self.key, self.value, self.datatype)

class Modul(models.Model):
    name = models.CharField(max_length = 225, validators=[filename_validator], help_text = u'Dateiname, inklusive Dateiendung')
    last_modified = models.DateTimeField(help_text = u'Datum / Uhrzeit letzte Revision')
    repository = models.ForeignKey(Repository, help_text = u'Verknüpftes Repository')
    code = models.TextField(help_text = u'Der eigentlich Quellcode')
    input_params = models.ManyToManyField(Parameter, related_name='input_parameters', blank = True, null = True, help_text = u'Parameter, die/der benötigt werden, um dieses Modul aufzurufen')
    output_params = models.ManyToManyField(Parameter, related_name='output_parameters', blank = True, null = True, help_text = u'Parameter, die/der zurückgegeben wird')
    depencencys = models.ManyToManyField("self", symmetrical = False, blank = True, null = True, verbose_name = u'Abhängige Module')
    user = models.ForeignKey(User, help_text = u'Zuständiger Benutzer')
    revision = models.CharField(max_length = 10, default="1.0", help_text = u'Aktuelle Revision')
    code_description = models.TextField(verbose_name = u'Beschreibung Code', help_text = u'Beschreibung des dargestellten Codes')
    code_language = models.ForeignKey(CodeLanguage, verbose_name = u'Sprache', help_text = u'Sprache des Quelltextes')
        
    class Meta:
        ordering = ['name']
        unique_together = (('name', 'repository'),)
        verbose_name = u'Modul'
        verbose_name_plural = u'Module'
        
    def __unicode__(self):
        return self.name
    
    def __repr__(self):
        return '<b>%s</b> (<a href="%s">suchen</a>|<a href="%s">edit</a>)' %(self.name, self.get_admin_search_url(), self.get_admin_url())
    
    def get_admin_search_url(self):
        return reverse('admin:source_modul_changelist')+'?q=%s'%(self.name)
    
    def get_admin_url(self):
        return reverse('admin:source_modul_change', args=(self.id,))
    
    def get_called_by(self):
        return Modul.objects.filter(depencencys__in = [self])
    get_called_by.short_description = u'Wird aufgerufen von'
    get_called_by.allow_tags = True

    
    def get_calls(self):
        return self.depencencys.all()
    get_calls.short_description = u'Ruft auf'
    get_calls.allow_tags = True

    def get_parsed_descr(self):
        s = self.code_description
        braces = re.findall(r'\(.*?\)', s)
        for b in braces:
            clean = b[1:-1]
            try:
                p = Parameter.objects.get(key = clean)
            except:
                p = None
            if p:
                replace_text = u'(<a class="parameter" href="%s" title="%s">%s</a>)' %(p.get_admin_url(),p.value, p.key)
                s = s.replace(b, replace_text)
        return s
    get_parsed_descr.short_description = u'Beschreibung'
    get_parsed_descr.allow_tags = True

    def get_absolute_url(self):
        return reverse('source_modul_named_details', args = (self.repository.slug, self.name)) 
        #return reverse('source_modul_details', kwargs={'pk':self.pk})

