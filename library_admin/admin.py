from django.contrib import admin
from django.contrib.admin import ModelAdmin
from . models import *

# Register your models here.

class Admin_library(admin.ModelAdmin):
    list_display = ("email","password")

class Admin_Category(admin.ModelAdmin):
    list_display = ("name","No_of_items")

class Admin_Book(admin.ModelAdmin):
    list_display=("name","price","quantity","category")


admin.site.register(Admin,Admin_library)
admin.site.register(Book_Category,Admin_Category)
admin.site.register(Book,Admin_Book)