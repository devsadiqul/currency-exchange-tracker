from celery import shared_task
import requests
from .models import ExchangeRateLog
import environ


env = environ.Env()
environ.Env.read_env()


@shared_task
def fetch_exchange_rate():
    api_key = env('EXCHANGE_RATE_API_KEY')
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rate = data['conversion_rates']['BDT']
        if rate:
            ExchangeRateLog.objects.create(
                base_currency='USD',
                target_currency='BDT',
                rate=rate
            )            