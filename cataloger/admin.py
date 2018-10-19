from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, BureauCode, Division, Office, Dataset, Distribution, Schema, AccessLevel, License, Keyword, Language

# Register your models here.
admin.site.register(Profile, UserAdmin)
admin.site.register(BureauCode)
admin.site.register(Division)
admin.site.register(Office)
admin.site.register(Dataset)
admin.site.register(Distribution)
admin.site.register(Schema)
admin.site.register(AccessLevel)
admin.site.register(License)
admin.site.register(Keyword)
admin.site.register(Language)
