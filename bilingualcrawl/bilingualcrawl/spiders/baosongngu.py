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

        # special case when all paragraph write in one <p> tag
        # process split with <br /> tag
        soup = BeautifulSoup(ps[0])
        if len(soup.find_all('span')) > 3: 
            lst = ps[0].split('<br>') # list 
            cnt = 0
            lens = len(lst)

            while cnt < lens - 1: 
                item = BilingualcrawlItem()
                msoup = BeautifulSoup(lst[cnt])
                if msoup.find('span') != None: 
                    item['english'] = msoup.text
                    item['vietnamese'] = BeautifulSoup(lst[cnt+1]).text
                    cnt += 2
                    yield item
                else: 
                    cnt += 1
        else: # normal case, split with <p> tag
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

                    item['english'] = soup.span.text
                    p2 = ps[cnt + 1]
                    soup = BeautifulSoup(p2, 'lxml')
                    item['vietnamese'] = soup.text
                    if soup.find('span') != None: 
                        item['vietnamese'] = item['vietnamese'].replace(soup.span.text, "")

                    cnt += 2
                    yield item
                else: # contain image tag
                    cnt += 1
    
    