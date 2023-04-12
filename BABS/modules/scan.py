import requests
import json
import psycopg2
import datetime
import argparse
import os


POSTGRESQL_USR = os.getenv('POSTGRESQL_USR')
POSTGRESQL_PWD = os.getenv('POSTGRESQL_PWD')

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--symbol', type=str, help='Trading pair: e.g. BTCUSDT', required=True)
parser.add_argument('-i', '--refresh_interval', type=float, help='Refresh interval in seconds: e.g. 5.0', required=True)
parser.add_argument('-t', '--value_threshold', type=float, help='Value threshold in USD: e.g. 400000.00', required=True)
parser.add_argument('-d', '--depth', type=str, help='Max depth (range 1-5000)', required=True)

args = parser.parse_args()

symbol = args.symbol.upper()
refresh_interval = args.refresh_interval
value_threshold = args.value_threshold
depth = args.depth

api_uri = 'https://api.binance.com/api/v3/depth?symbol=' + symbol + '&limit=' + depth

# Get order book snapshot from Binance API
def get_snapshot(api_uri):
    resp = requests.get(api_uri)
    snapshot = resp.json()

    return snapshot


# Retrieve last snapshot from API and filter price levels
def get_last_api_data():
    snapshot = get_snapshot(api_uri)

    # Create dictionaries with yielded results
    bids = {float(price): float(qty) for price, qty in snapshot['bids']}
    asks = {float(price): float(qty) for price, qty in snapshot['asks']}

    # Filter out bids and asks that do not meet the USD threshold
    filtered_bids = {price: qty for price, qty in bids.items() if price * qty >= value_threshold}
    filtered_asks = {price: qty for price, qty in asks.items() if price * qty >= value_threshold}

    # Join bids and asks into a single dictonary object
    last_api_data = {'symbol': symbol, 'bids': filtered_bids, 'asks': filtered_asks}

    return last_api_data


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


def get_symbol_db_record(symbol):
    conn = psycopg2.connect(database="babspostgres", user=POSTGRESQL_USR, password=POSTGRESQL_PWD, host="127.0.0.1", port="5432")
    cur = conn.cursor()

    # Select all rows where the 'symbol' field is equal to symbol
    cur.execute("SELECT json_data FROM frontend_scanresults WHERE json_data ->> 'symbol' = %s", [symbol])

    # Fetch all rows returned by the query
    rows = cur.fetchall()

    db_record = rows[0][0] # list to dictionary


    return db_record


# Find common filtered price levels and save in database
def compare_levels():
    # Retrieve last API data
    last_api_data = get_last_api_data()
    try:
        # Retrieve last record from db
        db_record = get_symbol_db_record(symbol)

        # since the second execution, compare new API data with db snapshot 
        # for finding common price levels

        # initialize an empty dictionary for the output
        output_dict = {'symbol': db_record['symbol'], 'bids': {}, 'asks': {}}

        # loop through the bids in db dictionary and check if they appear in last API snapshot
        for bid_price, bid_quantity in db_record['bids'].items():
            if float(bid_price) in last_api_data['bids']:
                output_dict['bids'][float(bid_price)] = last_api_data['bids'][float(bid_price)]

        # loop through the asks in db dictionary and check if they appear in last API snapshot
        for ask_price, ask_quantity in db_record['asks'].items():
            if float(ask_price) in last_api_data['asks']:
                output_dict['asks'][float(ask_price)] = last_api_data['asks'][float(ask_price)]

        # Add database snapshot with new data
        timestamp = datetime.datetime.now()
        output_dict["date"] = timestamp.isoformat()

        aggregated_bids = aggregate(last_api_data['bids'])
        aggregated_asks = aggregate(last_api_data['asks'])
        #print('last api data')
        #print(last_api_data)
        #print()
        print(aggregated_asks)
        '''
        print('db record')
        print(db_record)
        print()
        print('output dict')
        print(output_dict)
        '''
    # First run case, save in db
    except UnboundLocalError:
        last_api_data["first_scan"] = True
        conn = psycopg2.connect(database="babspostgres", user=POSTGRESQL_USR, password=POSTGRESQL_PWD, host="127.0.0.1", port="5432")
        cur = conn.cursor()
        json_data = json.dumps(last_api_data) # Serialize dictionary to a JSON string
        # save_query = """INSERT INTO frontend_scanresults (JSON_DATA) VALUES ('{"name":"John", "age":30, "car":"null"}')"""
        save_query = """INSERT INTO frontend_scanresults (JSON_DATA) VALUES (%s)"""
        cur.execute(save_query, (json_data,))
        conn.commit()
        cur.close()
        conn.close()


compare_levels()