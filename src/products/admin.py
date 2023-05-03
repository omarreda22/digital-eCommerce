from django.contrib import admin

from .models import Product, ProductImages



class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'handle': ('name',)}

admin.site.register(Product, ProductAdmin)


admin.site.register(ProductImages)