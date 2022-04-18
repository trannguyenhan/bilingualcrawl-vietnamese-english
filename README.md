## Crawl data

```bash
scrapy crawl vietanhsongngu -o /home/trannguyenhan/output.json --set FEED_EXPORT_ENCODING=utf-8
```

## Install splash 

splash support render and crawl website gen by javascrip.

Instal splash docker:

```bash
sudo docker pull scrapinghub/splash
```

Install library using in python:

```bash
pip install scrapy scrapy-splash
```

Run splash in docker and bind to 8050 port: 

```bash
sudo docker run -p 8050:8050 scrapinghub/splash
```
