from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


# Create your models here.
class Account(models.Model):
    def __str__(self):
        return self.name + " by " + str(self.author)

    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def balance(self):
        b = Decimal(0)
        all_transactions = Transaction.objects.filter(account=self)
        for t in all_transactions:
            if t.type:
                b += t.cost * t.amount
            else:
                b -= t.cost * t.amount
        return b


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
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=3, default=1)
    description = models.CharField(max_length=500, null=True)


class Transfer(models.Model):
    def __str__(self):
        pass

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transfer_source")
    destination = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transfer_destination")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=500, null=True)