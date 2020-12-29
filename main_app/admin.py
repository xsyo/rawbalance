from django.contrib import admin

from .models import Profile, Category, Product

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Category)
