#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User, Group
from django.template import RequestContext
from models import Repository, Modul, Package, CodeLanguage, Parameter
from django.core.urlresolvers import reverse
from django.db.models import Q

from django import forms
from django.shortcuts import redirect

class SearchForm(forms.Form):
    query = forms.CharField(label='Suchwort', max_length=200)
    


def index(request):
    #style = request.GET.get('style', 'plain')
    search_form = SearchForm()
    style = 'plain'
    packets = Package.objects.all()
    if style == 'plain':
        return render_to_response('source/html/index.html', 
                              locals(), 
                              context_instance=RequestContext(request))

def package_details(request, slug):
    search_form = SearchForm()
    package = get_object_or_404(Package, slug=slug)
    return render_to_response('source/html/package.html', 
                              locals(), 
                              context_instance=RequestContext(request))



def mod_named_details(request, rep_slug, name):
    search_form = SearchForm()
    modul = get_object_or_404(Modul, repository__slug__iexact = rep_slug, name__iexact=name)
    return render_to_response('source/html/modul.html', 
                              locals(), 
                              context_instance=RequestContext(request))

def mod_details(request, pk):
    modul = get_object_or_404(Modul, pk=pk)
    rep_slug = modul.repository.slug
    name = modul.name
    redir = reverse('source_modul_named_details', args = (rep_slug, name)) 
    return redirect(redir)


def modultree(request):
    search_form = SearchForm()
    packets = Package.objects.all()
    return render_to_response('source/html/moduletree.html', 
                              locals(), 
                              context_instance=RequestContext(request))

def search(request):
    results = {'Pakete':[],
               'Repository':[],
               'CodeLanguage':[],
               'Modul':[],
               'Parameter':[] }

    if request.method == 'POST': # If the form has been submitted...
        search_form = SearchForm(request.POST) # A form bound to the POST data
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = {'Pakete':Package.objects.filter(Q(name__icontains = query) | Q(description__icontains = query)),
                       'Repository':Repository.objects.filter(Q(name__icontains = query) | Q(slug__icontains = query)),
                       'CodeLanguage':CodeLanguage.objects.filter(Q(lang__icontains = query)),
                       'Modul':Modul.objects.filter(Q(name__icontains = query) | Q(code__icontains = query) | Q(code_description__icontains = query)),
                       'Parameter':Parameter.objects.filter(Q(key__icontains = query) | Q(value__icontains = query) | Q(datatype__type__icontains = query))
                       }
    else:
        search_form = SearchForm()
    return render_to_response('source/html/search.html', 
                              locals(), 
                              context_instance=RequestContext(request))
