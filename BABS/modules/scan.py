import requests
import json
import datetime

# Set global variables
symbol = 'BTCUSDT' # keep uppercase
refresh_interval = 30.0 # in seconds
value_threshold = 400000.00 # in USD
depth = '5000' # max 5000

# Set global constants
snapshot_uri = 'https://api.binance.com/api/v3/depth?symbol=' + symbol + '&limit=' + depth

# Get order book snapshot from Binance API
def get_snapshot(snapshot_uri):
    resp = requests.get(snapshot_uri)
    snapshot = resp.json()

    return snapshot


# Retrieve last snapshot from API and filter price levels
def get_last_api_data():
    snapshot = get_snapshot(snapshot_uri)

    # Create dictionaries with yielded results
    bids = {float(price): float(qty) for price, qty in snapshot['bids']}
    asks = {float(price): float(qty) for price, qty in snapshot['asks']}

    # Filter out bids and asks that do not meet the USD threshold
    filtered_bids = {price: qty for price, qty in bids.items() if price * qty >= value_threshold}
    filtered_asks = {price: qty for price, qty in asks.items() if price * qty >= value_threshold}

    # Join bids and asks into a single dictonary object
    last_api_data = {'symbol': symbol, 'bids': filtered_bids, 'asks': filtered_asks}

    return last_api_data


# Find common filtered price levels and save in database
def filter_levels():

    # Retrieve last record from db


    # Retrieve last API data
    last_api_data = get_last_api_data()
    if not db_record: # first run case, save in db
        last_api_data["first_scan"] = True
        result = json.dumps(last_api_data) # Convert result dictionary to JSON object


        document = json.loads(result)


    else: # since the second execution, compare new API data with db snapshot
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

        #DEBUG TO BE REMOVED
        '''
        print('db record')
        print(db_record)
        print()
        print('last API data')
        print(last_api_data)
        print()
        print('values found in both dictionaries')
        print(result)
        '''


filter_levels()