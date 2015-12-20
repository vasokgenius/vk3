from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    fields = ("uid", "name", "surname", 'access_token')
    list_display = ["uid", "name", "surname"]
    search_fields = ["name", 'surname']

admin.site.register(User, UserAdmin)


class GroupAdmin(admin.ModelAdmin):
    fields = ('gid', "name", "gtype", "is_closed", 'photo')
    list_display = ["name", "gtype", "is_closed"]
    list_display_links = ["name"]
    list_filter = ["gtype"]
    search_fields = ["name"]

admin.site.register(Group, GroupAdmin)