## Scope
The scope of this tool is providing useful order book signals from Binance order book, by:
- reading symbol order book repeatedly
- saving aggregated price levels
- displaying data into a webpage using charts

<sub>Note: each symbol scan depth is limited by Binance API of last 5000 bids & asks</sub>

## Requirements
Docker

## Usage
Docker image is made of:
- PostgreSql database (official image)
- Redis server (official image)
- pgAdmin4 (official image)
- Application

<sub>In production run it in front of nginx reverse proxy</sub>

<img src="https://dl.dropboxusercontent.com/s/is8aj5ld2ywfw6i/scanned-by-snyk.png" alt="scanned by snyk" width="151" height="86"></img>

1. Export required environment variables
```
export=DJANGO_SECRET_KEY=
export=POSTGRES_PASSWORD=
export=PGADMIN_DEFAULT_EMAIL
export=PGADMIN_DEFAULT_PASSWORD=
```
2. Build and run
```
bash run.sh
docker compose exec web python babsproj/manage.py qcluster
```

3. First time run, populate symbols list and schedule weekly update
```
docker compose exec web python babsproj/babs/bootstrap.py schedule-symbols
```

<img src="https://i.imgur.com/kOptWcG.gif"></img>
