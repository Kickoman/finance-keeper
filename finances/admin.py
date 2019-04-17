from django.contrib import admin

# Register your models here.
from .models import Category, Transaction

admin.site.register(Category)
admin.site.register(Transaction)