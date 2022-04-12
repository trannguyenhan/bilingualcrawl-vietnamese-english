from bs4 import BeautifulSoup
import scrapy
from bilingualcrawl.items import BilingualcrawlItem
from bilingualcrawl.spiders.detail_scraper import DetailScraperSpider

import bilingualcrawl.spiders.pool_urls as pool_urls

class VietanhsongnguSpider(DetailScraperSpider):
    name = 'vietanhsongngu'
    base_url = 'vietanhsongngu.com'

    configs = [
        {
            "url": "http://vietanhsongngu.com/hoc-tieng-anh-bai-mau-tin-tuc-c5.htm",
            "number_pages": 216
        },
        {
            "url": "http://vietanhsongngu.com/hoc-tieng-anh-qua-truyen-song-ngu-c7.htm",
            "number_pages": 12
        },
        {
            "url": "http://vietanhsongngu.com/van-hoa-du-lich-am-thuc-viet-c6.htm",
            "number_pages": 12
        }
    ]

    prefix_next_page = ""

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

        while cnt < lens: 
            pcheck = ps[cnt]
            soup = BeautifulSoup(pcheck, 'lxml')
            
            if soup.find('span') == None: 
                cnt += 1
                continue

            if soup.find('span').get('style') != "color:#3498db": 
                cnt += 1
                continue
            else: 
                p2 = ps[cnt]
                p1 = ps[cnt - 1]

                item = BilingualcrawlItem()
                item['english'] = BeautifulSoup(p2, 'lxml').text
                item['vietnamese'] = BeautifulSoup(p1, 'lxml').text

                cnt += 1
                yield item