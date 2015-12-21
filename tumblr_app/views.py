from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.template import RequestContext

from .models import *


def HomeView(request):
    template_name = 'tumblr_app/index.html'
    
    return render(request, template_name, {})
    