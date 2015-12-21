from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^vk/', include('vk_app.urls', namespace = 'vk')),
    url(r'^tumblr/', include('tumblr_app.urls', namespace = 'tumblr')),
    url(r'^admin/', include(admin.site.urls)),
]

