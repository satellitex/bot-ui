# bot-ui
bot の損益などをヴィジュアライズするための web app.
http://175.41.244.3:443/

# How to run
## Using poetry

### Edit .env
```
UI_CSV_PATH=<表示するグラフのもととなるcsvファイル>
```

### run
```sh
poetry shell
python frontend/app.py
```

### Using docker

1. make docker image
```sh
docker build . -t satellitex/bot-web
```
or
```sh
docker pull satellitex/bot-web
```

2. run
```sh
docker run -d --restart unless-stopped --mount type=bind,source="$(pwd)"/csv,target=/usr/src/app/csv -e UI_CSV_PATH=csv/kosoku_binance_BTCUSDT_5m_pl.csv  -p 8000:8050 satellitex/bot-web
```

- in bot-tests
```sh
docker run -d --restart unless-stopped --mount type=bind,source="$(pwd)"/log/csv,target=/usr/src/app/csv -e UI_CSV_PATH=csv/kosoku_binance_BTCUSDT_5m_pl.csv  -p 443:8050 satellitex/bot-web
```

## TODO
- hover の数値をカンマ区切りにする
 - https://plotly.com/python/hover-text-and-formatting/