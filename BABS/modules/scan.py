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


def get_symbol_db_record(symbol):
    conn = psycopg2.connect(database="babspostgres", user=POSTGRESQL_USR, password=POSTGRESQL_PWD, host="127.0.0.1", port="5432")
    cur = conn.cursor()

    # Select all rows where the 'symbol' field is equal to symbol
    cur.execute("SELECT json_data FROM frontend_scanresults WHERE json_data ->> 'symbol' = %s", [symbol])

    # Fetch all rows returned by the query
    rows = cur.fetchall()

    # Process each row and extract the JSON data
    for row in rows:
        json_data = json.loads(row[0])

    return json_data


# Find common filtered price levels and save in database
def filter_levels():
    # Retrieve last API data
    last_api_data = get_last_api_data()
    try:
        # Retrieve last record from db
        json_data = get_symbol_db_record(symbol)
        print(json_data)

        # oldest_timestamp_data = ScanResults.objects.filter(json_data__symbol='BTCUSDT').filter(json_data__first_scan=True).order_by('json_data__timestamp')
        # latest_timestamp_data = ScanResults.objects.filter(json_data__symbol='BTCUSDT').filter(json_data__first_scan=True).order_by('-json_data__timestamp')
    except UnboundLocalError:
        # first run case, save in db
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

    '''
    # since the second execution, compare new API data with db snapshot
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
    result = json.dumps(output_dict) # Convert result dictionary to JSON object
    '''


filter_levels()