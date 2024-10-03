from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class UserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, UserAdmin) 
admin.site.register(Profile)