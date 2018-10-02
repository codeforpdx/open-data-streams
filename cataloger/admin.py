from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, BureauCode, Division, Office

# Register your models here.
admin.site.register(Profile, UserAdmin)
admin.site.register(BureauCode)
admin.site.register(Division)
admin.site.register(Office)
