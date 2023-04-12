## Scope
The scope of this tool is providing useful order book signals from Binance order book, by:
- reading symbol order book repeatedly
- saving filtered price levels according to specific order value
- comparing new order book data with previous filtered price levels
- saving updated data and displaying them on a webpage using a chart


## Working principle
Every X seconds (the refresh interval can be modified) the tool starts a new check procedure.

When running for the first time:

1. Connects to the Binance API for fetching latest order book data for the chosen symbol using maximum scan depth (last 5000 bids & asks) allowed by Binance
3. Filters price levels basing on USD order value (price * quantity) set by the user
3. Saves data in database

Next time it runs:

4. Connects to database for fetching previous symbol snapshot
6. Repeats step 1
7. Compares latest data from API with data saved inside the database in order to find common price levels
8. Creates a new object containing common price levels with updated quantities
9. Replaces database object with the new dictionary


## Requirements
PostgreSQL instance with a database named `babs`


## Usage
1. Clone repo && cd into directory
2. Install `python>= 3.9.2` + `venv`
3. Activate virtual environment
```
mkdir -p env
source env/bin/activate
```
4. Install requirements `python -m pip install -r requirements.txt`
5. Export environment variables with your PostgreSql installation
```
export POSTGRESQL_USR=
export POSTGRESQL_PWD=
```
6. Review the 3 main required input parameters within `babs.py`:
```
symbol = 'BTCUSDT'
refresh_interval = 5.0 (in seconds)
value_threshold = 400000.00 (in USD)
```
7. Run `python babs.py`


## DEV branch
- Add django
- Line chart for prices and quantities
- Extend trading pair selection to All pairs or specific trading pairs selected by the user
- Bake docker image
- Alerting (TBD)
