from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(News)
admin.site.register(Pinned_News)
admin.site.register(UserProfile)
admin.site.register(Reporter)