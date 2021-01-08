from django.contrib import admin

from .models import Profile, Category, Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']

admin.site.register(Profile)
admin.site.register(Category)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'created_at', 'updated_at', 'paid']
    fields = ['customer', 'product', ('created_at', 'updated_at'), 'paid']