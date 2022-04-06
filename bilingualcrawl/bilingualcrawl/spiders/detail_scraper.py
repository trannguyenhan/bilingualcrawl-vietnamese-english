import scrapy
import bilingualcrawl.spiders.pool_urls as pool_urls

class DetailScraperSpider(scrapy.Spider):
    configs = []
    prefix_next_page = ""

    def start_requests(self):
        urls = pool_urls.create_pool_urls(self.configs, self.prefix_next_page)
        for url in urls: 
            yield scrapy.Request(url=url, callback=self.parse)