## Scope
The scope of this tool is providing useful order book signals from Binance order book, by:
- reading symbol order book repeatedly
- saving aggregated price levels
- displaying data into a webpage using charts

<sub>Note: each symbol scan depth is limited by Binance API of last 5000 bids & asks</sub>

## Requirements
- PostgreSQL database
- Redis server

By default it connects to `localhost:5432` with user and database name as `postgres` and to
redis server `localhost:6379` without authentication

## Usage
1. Clone repo && cd into directory
2. Install `python>= 3.9.2` + `venv`
3. Activate virtual environment
```
mkdir -p env
python -m venv env
source env/bin/activate
```
4. Install requirements `python -m pip install -r requirements.txt`
5. Export Postgresql password environment variable
```
export POSTGRES_PASSWORD=
```
6. Apply database migrations
```
cd babsproj
python manage.py makemigrations
python manage.py migrate
```
7. Open another shell with environment variables exported for starting DjangoQ:
```
python manage.py qcluster
```
8. Populate symbols list and schedule weekly update
```
python babs/bootstrap.py schedule-symbols
```
9. Run `python manage.py runserver`
