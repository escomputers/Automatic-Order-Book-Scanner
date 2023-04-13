import requests
import psycopg2
import argparse
import os
import json
import os
import sys

# Get database name
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BABS.settings')
from django.conf import settings
database_name = settings.DATABASES['default']['NAME']


POSTGRESQL_USR = os.getenv('POSTGRESQL_USR')
POSTGRESQL_PWD = os.getenv('POSTGRESQL_PWD')

# Define arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--symbol', type=str, help='Trading pair: e.g. BTCUSDT', required=True)
parser.add_argument('-i', '--refresh_interval', type=float, help='Refresh interval in seconds: e.g. 5.0', required=True)
# parser.add_argument('-g', '--group', type=int, help='How many price levels to be grouped : e.g. 100', required=True)
parser.add_argument('-d', '--depth', type=str, help='Max depth (range 1-5000)', required=True)

args = parser.parse_args()

# Get args
symbol = args.symbol.upper()
refresh_interval = args.refresh_interval
depth = args.depth

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
        price_group = int(price / 100) * 100

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
    bids = aggregate(api_data['bids'])
    asks = aggregate(api_data['asks'])

    '''
    conn = psycopg2.connect(database=database_name, user=POSTGRESQL_USR, password=POSTGRESQL_PWD, host="127.0.0.1", port="5432")
    cur = conn.cursor()
    bids = json.dumps(bids) # Serialize dictionary to a JSON string
    asks = json.dumps(asks)
    save_query = """INSERT INTO frontend_scanresults (bids) VALUES (%s)"""
    cur.execute(save_query, (bids,))
    conn.commit()
    cur.close()
    conn.close()
    '''


run()