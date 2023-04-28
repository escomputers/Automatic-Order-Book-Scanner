## Scope
The scope of this tool is providing useful order book signals from Binance order book, by:
- reading symbol order book repeatedly
- saving aggregated price levels
- displaying data into a webpage using charts

<sub>Note: each symbol scan depth is limited by Binance API of last 5000 bids & asks</sub>

## Requirements
PostgreSQL database


## Usage
1. Clone repo && cd into directory
2. Install `python>= 3.9.2` + `venv`
3. Activate virtual environment
```
mkdir -p env
source env/bin/activate
```
4. Install requirements `python -m pip install -r requirements.txt`
5. Export environment variables with your PostgreSql installation and configure `settings.py` by setting database connection details
```
export POSTGRESQL_USR=
export POSTGRESQL_PWD=
```
6. Apply database migrations
```
python manage.py makemigrations
python manage.py migrate
```
7. Create Django ORM cache table
```
python manage.py createcachetable django_orm_cache_table
```
8. Open another shell with environment variables exported for starting DjangoQ:
```
python manage.py qcluster
```
9. Populate symbols list and schedule weekly update
```
python frontend/bootstrap.py schedule-symbols
```
10. Run `python manage.py runserver`


## INT branch
| Feature      | Status |
| ----------- | ----------- |
| Bake docker image       | In progress       |
| Extend trading pair selection to All and GROUP   | Todo        |
| Migrate to websocket     | TBD       |
| Add BUSD     | TBD       |
| Alerting     | TBD       |
