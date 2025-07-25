from django.db import models

type_choice = [(i.upper(), i) for i in ['Gain', 'Loss']]
sphere_choice = [(i.upper(), i) for i in ['', 'Housing', 'Food', 'Transport', 'Enjoyment', 'Deposit']]
choice = [(i.upper(), i) for i in ['usd', 'eur', 'rub']]
# Create your models here.

class Records(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=type_choice, default='GAIN', max_length=100)
    size = models.DecimalField(max_digits=100, decimal_places=2)
    sphere = models.CharField(choices=sphere_choice, default='', max_length=100)
    currency = models.CharField(choices=choice, default='RUB', max_length=10)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=1)
    class Meta:
        ordering = ['added']
        

class Currencies(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    base = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=100, decimal_places=10)