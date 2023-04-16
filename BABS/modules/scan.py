import requests
import argparse
import os
import sys

# Initialize Django project environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BABS.settings')
import django
django.setup()


from django.utils import timezone
from frontend.models import ScanResults


# Define arguments
parser = argparse.ArgumentParser()
parser.add_argument('symbol', type=str, help='Trading pair: e.g. BTCUSDT')
parser.add_argument('group', type=int, help='How many digits to be grouped in price : e.g. 100')
parser.add_argument('depth', type=str, help='Max depth (range 1-5000)')

args = parser.parse_args()

# Get args
symbol = args.symbol.upper()
depth = args.depth
group_level = args.group

api_uri = 'https://api.binance.com/api/v3/depth?symbol=' + symbol + '&limit=' + depth


# Get order book snapshot from Binance API
def get_api_data(api_uri):
    resp = requests.get(api_uri)
    snapshot = resp.json()

    # Create dictionaries with yielded results
    bids = {float(price): float(qty) for price, qty in snapshot['bids']}
    asks = {float(price): float(qty) for price, qty in snapshot['asks']}

    # Join bids and asks into a single dictonary object
    api_data = {'bids': bids, 'asks': asks}


    return api_data


def aggregate(orders):
    price_groups = {}
    for price, quantity in orders.items():
        # Determine the price group
        price_group = int(price / group_level) * group_level

        # If the price group doesn't exist yet, create it
        if price_group not in price_groups:
            price_groups[price_group] = {"Quantity": quantity, "Weighted Price": price * quantity}
        else:
            # If the price group already exists, update its quantity and weighted price
            price_groups[price_group]["Quantity"] += quantity
            price_groups[price_group]["Weighted Price"] += price * quantity

    # Calculate the arithmetic mean for each price group
    for price_group in price_groups:
        price_groups[price_group]["Weighted Price"] /= price_groups[price_group]["Quantity"]


    return price_groups


def run():
    api_data = get_api_data(api_uri)

    # Create instances of ScanResults model
    scan_results = [
        ScanResults(
            timestamp=timezone.now(), # UTC
            symbol=symbol,
            bids=aggregate(api_data['bids']),
            asks=aggregate(api_data['asks']),
        )
    ]
    ScanResults.objects.bulk_create(scan_results)


run()