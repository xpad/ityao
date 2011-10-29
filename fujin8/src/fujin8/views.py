import json 
import time 
from django.http import HttpResponse
from django.template import Context, loader

from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.template.context import RequestContext
from fujin8.btfactory.models import Actress
from fujin8.btfactory.forms import ActressSearchForm

def home(request):
    actresses = []
    if request.method == 'POST':
        form = ActressSearchForm(request.POST)
        if form.is_valid():
            act_name = form.cleaned_data['actress']
            actresses = Actress.objects.filter(co_names__icontains=act_name)
       
    # less database queries.
    if not actresses:
        actresses = Actress.objects.order_by('-id')[:8]
    #form = ActressSearchForm()    
    return render_to_response(u'index.html',locals() , context_instance=RequestContext(request))

def about(request): 
    return render_to_response(u'about.html')

def timestamp(request): 
    return HttpResponse(json.dumps({u'time': 1000 * time.time()}),mimetype=u'application/json')
