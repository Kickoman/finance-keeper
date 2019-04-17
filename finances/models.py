from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Account(models.Model):

    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Category(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    type = models.BooleanField('Income') # income or expense


class Transaction(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    date = models.DateField('Date executed')
    type = models.BooleanField('Income')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=3, default=1)
    description = models.CharField(max_length=500, null=True)