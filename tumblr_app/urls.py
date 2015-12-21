from django.conf.urls import include, url
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.HomeView, name='home'),
]
