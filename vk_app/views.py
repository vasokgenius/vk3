from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.template import RequestContext

from .models import *
from .api import AUTH_URL


def HomeView(request):
    template_name = 'vk_app/index.html'
    
    return render(request, template_name, {'auth_url' : AUTH_URL})
    
def TokenView(request, access_token):
    template_name = 'vk_app/token.html'
    print(access_token)

    return render(request, template_name, {})