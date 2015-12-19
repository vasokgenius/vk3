from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^', include('vk_app.urls', namespace = 'vk')),
    url(r'^admin/', include(admin.site.urls)),
]

