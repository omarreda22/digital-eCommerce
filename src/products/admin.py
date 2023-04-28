from django.contrib import admin

from .models import Product



class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'handle': ('name',)}

admin.site.register(Product, ProductAdmin)