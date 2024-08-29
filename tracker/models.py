from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import TransactionQuerySet

from tracker import data

class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    
    type = models.CharField(max_length=7, choices=data.TRANSACTION_TYPE_CHOICES)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    date = models.DateTimeField()
    
    objects = TransactionQuerySet.as_manager()
    
    def __str__(self):
        return f'{self.type} of {self.amount} on {self.date} by {self.user}'
    
    class Meta:
        ordering = ['-date']

