from django.contrib import admin

# Register your models here.
from .models import Category, Transaction, Account

admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Account)