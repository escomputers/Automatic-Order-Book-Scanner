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

<img src="https://uc94e2d4395cd46811204243c702.previews.dropboxusercontent.com/p/thumb/AB6fIHqjRf0yPiMQLoAId88eUe1zpJ6LV2DWGT7_e4Yj877CvMQdgkNpjYwNhRD0CMJdhmbmZ0a6qlh0ijPLUHLHlNO4ZSM5uYkBWUl8274CEmC3kz4Nh8kjEKmLgNfQ5AAJiungiSe7G-G_rAJzDux2prCJxXZmKsJAv2vPrvj1YDaieFQiz3-zMb755DRvAiMMeV-Aa0sS_9V1MgWkm0cmwR6-OfdStvwc5R92Mfk5qAPdtPQmN5NlYcFA8rDyrXdYH8c29KCAc7nX4M_zyS3C4N88HgJaufR5ZYyDq659HOumK9WGbm_Lmy39a-1PdVuJjEf68YMArJQHy7grOHYqVvzsLGonexBnoVm1u8SORfIWDGlvQb-FFpvJdCGWChuOcMUovBrXHzA5WyRLqeXjFQf-zlxK_PJWyBoH_nmT5Q/p.png" alt="scanned by snyk" width="151" height="86"></img>

1. Export required environment variables
```
export=DJANGO_SECRET_KEY=
export=POSTGRES_PASSWORD=
export=PGADMIN_DEFAULT_EMAIL
export=PGADMIN_DEFAULT_PASSWORD=
```
2. Build and run
```bash run.sh```

3. Populate symbols list and schedule weekly update
```
docker compose exec web python babsproj/babs/bootstrap.py schedule-symbols
```
