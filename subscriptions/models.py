from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name
    
    
class Subscription(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    
    def __str__(self):
        return f'{self.user.username} - {self.plan.name}'
    
    
class ExchangeRateLog(models.Model):
    base_currency = models.CharField(max_length=3)
    target_currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    fetched_at = models.DateTimeField(default=timezone.now)
    
    
    def __str__(self):
        return f'{self.base_currency}/{self.target_currency}: {self.rate}'
    
    