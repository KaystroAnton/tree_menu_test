from django.contrib import admin


from django.contrib import admin
from .models import MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'url' ,'url_name')
    list_filter = ('name','parent')