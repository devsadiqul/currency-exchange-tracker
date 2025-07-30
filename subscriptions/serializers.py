from rest_framework import serializers
from .models import *


# Create your serializer here.
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'duration_days']
        
        
class SubcriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'plan', 'start_date', 'end_date', 'status']
        
        
class ExchangeRateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRateLog
        fields = ['id', 'base_currency', 'target_currency', 'rate', 'fetched_at']