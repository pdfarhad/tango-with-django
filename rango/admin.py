from django.contrib import admin
from .models import Category, Page, UserProfile

# Register your models here.
admin.site.register(Category)
admin.site.register(Page)
admin.site.register(UserProfile)
