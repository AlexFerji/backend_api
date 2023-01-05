from django.contrib import admin
from .models import Category, Image

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']



class ImageAdmin(admin.ModelAdmin):
    list_display = ['category', 'user', 'title']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
