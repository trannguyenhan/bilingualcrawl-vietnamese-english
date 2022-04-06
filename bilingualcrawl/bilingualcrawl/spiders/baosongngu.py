import scrapy
from bs4 import BeautifulSoup
from bilingualcrawl.items import BilingualcrawlItem
from bilingualcrawl.spiders.detail_scraper import DetailScraperSpider

class BaosongnguSpider(DetailScraperSpider):
    name = 'baosongngu'
    base_url = 'baosongngu.net'

    configs = [
        {
            "url": "https://baosongngu.net/chuyen-muc/world/",
            "number_pages": 31
        },
        {
            "url": "https://baosongngu.net/chuyen-muc/vn/",
            "number_pages": 43
        },
        {
            "url": "https://baosongngu.net/chuyen-muc/bao-economist/",
            "number_pages": 4
        }
    ]

    prefix_next_page = "page"

    def __init__(self):
        DetailScraperSpider.__init__(self)
    
    def parse(self, response): 
        hrefs = response.css("#main").css('article').css('h2').css('a').xpath('@href').extract()
        for href in hrefs: 
            if self.base_url in href: 
                yield scrapy.Request(url=href, callback=self.parse_detail)

    def parse_detail(self, response):
        ps = response.css('article').css('p').extract()

        cnt = 0
        lens = len(ps)

        while cnt < lens - 1: 
            pcheck = ps[cnt]
            soup = BeautifulSoup(pcheck, 'lxml')
            if soup.find('img') != None: 
                item = BilingualcrawlItem()
                p1 = ps[cnt]
                soup = BeautifulSoup(p1, 'lxml')

                if soup.find('span') == None: # not english
                    cnt += 1
                    continue

                item['english'] = soup.text
                p2 = ps[cnt + 1]
                soup = BeautifulSoup(p2, 'lxml')
                item['vietnamese'] = soup.text

                cnt += 2
                yield item
            else: # contain image tag
                cnt += 1
    
    