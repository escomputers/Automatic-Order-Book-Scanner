import requests
import os
import sys


# Initialize Django project environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BABS.settings')
import django
django.setup()

from django_q.tasks import schedule, Schedule
from frontend.models import Symbol


def SymbolsUpdate():
    api_uri_info = 'https://api.binance.com/api/v1/exchangeInfo'
    resp = requests.get(api_uri_info)
    snapshot = resp.json()
    # Loop through all symbols and filter out those with USDT as a quote asset
    usdt_pairs = []
    for symbol in snapshot['symbols']:
        if symbol['quoteAsset'] == 'USDT':
            usdt_pairs.append(symbol['symbol'])

    try:
        Symbol.objects.all().delete()
    except Symbol.DoesNotExists:
        pass

    for symbol in usdt_pairs:
        new_symbol = Symbol(symbol=symbol)
        new_symbol.save()


# Assign task of updating symbols weekly to DjangoQ
def ScheduleSymbolsUpdate():
    SymbolsUpdate()
    schedule('frontend.bootstrap.SymbolsUpdate',
        name='job-update-symbols',
        schedule_type=Schedule.WEEKLY,
        repeats=-1
    )


if __name__ == "__main__":
    if sys.argv[1] == "schedule-symbols":
        ScheduleSymbolsUpdate()