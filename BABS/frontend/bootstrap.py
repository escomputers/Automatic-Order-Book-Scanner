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
    # Get API data
    api_uri_info = 'https://api.binance.com/api/v1/exchangeInfo'
    resp = requests.get(api_uri_info)
    snapshot = resp.json()
    # Loop through all symbols and filter out those with USDT as a quote asset
    usdt_pairs = []
    for symbol in snapshot['symbols']:
        if symbol['quoteAsset'] == 'USDT':
            usdt_pairs.append(symbol['symbol'])

    try:
        # Get the existing symbols from the database
        existing_symbols = set(Symbol.objects.values_list('symbol', flat=True))

        # Find the symbols that are new
        new_symbols = set(usdt_pairs) - existing_symbols

        # Find the symbols that have been removed in Binance
        removed_symbols = existing_symbols - set(usdt_pairs)

        # Add the new symbols to the database
        for symbol in new_symbols:
            new_symbol = Symbol(symbol=symbol)
            new_symbol.save()

        # Remove the symbols that have been removed from the database
        Symbol.objects.filter(symbol__in=removed_symbols).delete()
    except Symbol.DoesNotExist:
        for symbol in usdt_pairs: # add all symbols from scratch
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