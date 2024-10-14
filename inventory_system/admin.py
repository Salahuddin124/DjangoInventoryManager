from django.contrib import admin
from .models import Products
from django.contrib.auth.models import Group

# Register your models here.
admin.site.unregister(Group)
admin.site.register(Products)
admin.site.site_header = "School Inventory System"