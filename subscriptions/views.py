from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import SubcriptionSerializer, ExchangeRateLogSerializer
import requests
import environ
from datetime import timedelta
from django.utils import timezone


env = environ.Env()
environ.Env.read_env()


# Create your views here.
class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        plan_id = request.data.get('plan_id')
        
        try:
          plan = Plan.objects.get(id=plan_id)
          subscription = Subscription.objects.create(
            user=request.user,
            plan=plan,
            start_date=timezone.now,
            end_date=timezone.now + timedelta(days=plan.duration_days),
            status='active'
          )
          return Response(SubcriptionSerializer(subscription).data, status=status.HTTP_201_CREATED)
        except Plan.DoesNotExist:
          return Response({'detail': 'Plan not found.'}, status=status.HTTP_404_NOT_FOUND)
      
      
class SubscriptionListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        subscriptions = Subscription.objects.filter(user=request.user)
        serializer = SubcriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        subscription_id = request.data.get('subscription_id')
        
        try:
          subscription = Subscription.objects.get(id=subscription_id, user=request.user)
          subscription.status = 'cancelled'
          subscription.save()
        except Subscription.DoesNotExist:
          return Response({'detail': 'Subcription not found.'}, status=status.HTTP_404_NOT_FOUND)
      
      
class ExchangeRateView(APIView):
    def get(self, request):
        base = request.query_params.get('base', 'USD')
        target = request.query_params.get('target', 'BDT')
        
        api_key = env('EXCHANGE_RATE_API_KEY')
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}'
        
        response = requests.get(url)
    
        if response.status_code == 200:
            data = response.json()
            rate = data['conversion_rates']['BDT']
            print(rate)
            if rate:
                log = ExchangeRateLog.objects.create(
                    base_currency=base,
                    target_currency=target,
                    rate=rate
                )            
                return Response(ExchangeRateLogSerializer(log).data, status=status.HTTP_201_CREATED)
            return Response({'detail': 'Target currency not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'API request failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
def subscription_list(request):
    subscriptions = Subscription.objects.all()
    return render(request, 'subscriptions/subscription_list.html', {'subscriptions': subscriptions})    
        
        
    
