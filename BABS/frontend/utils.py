import requests
import os
import sys
import json

def Scan(symbol, grouping, depth):
    # Initialize Django project environment
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BABS.settings')
    import django
    django.setup()


    from django.utils import timezone
    from frontend.models import ScanResults

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
            group_level = int(grouping)
            price_group = int(price / group_level) * group_level

            # If the price group doesn't exist yet, create it
            if price_group not in price_groups:
                price_groups[price_group] = {"QTY": quantity, "WP": price * quantity}
            else:
                # If the price group already exists, update its quantity and weighted price
                price_groups[price_group]["QTY"] += quantity
                price_groups[price_group]["WP"] += price * quantity

        # Calculate the arithmetic mean for each price group
        for price_group in price_groups:
            price_groups[price_group]["WP"] /= price_groups[price_group]["QTY"]


        return price_groups


    api_data = get_api_data(api_uri)

    bids = json.dumps(aggregate(api_data['bids']))
    asks = json.dumps(aggregate(api_data['asks']))

    # Create instances of ScanResults model
    scan_results = [
        ScanResults(
            symbol=symbol,
            bids=bids,
            asks=asks,
        )
    ]
    ScanResults.objects.bulk_create(scan_results)
