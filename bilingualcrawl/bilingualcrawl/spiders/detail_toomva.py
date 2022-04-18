from bs4 import BeautifulSoup
import scrapy
from scrapy_splash import SplashRequest

from bilingualcrawl.items import BilingualcrawlItem

class DetailToomvaSpider(scrapy.Spider):
    base_url = 'baosongngu.net'

    configs = [
        {
            "url": "https://toomva.com/Video-Hoc-Tieng-Anh/c=45",
            "number_pages": 8
        },
        {
            "url": "https://toomva.com/Hoc-tieng-Anh-qua-phim/c=14",
            "number_pages": 130
        },
        {
            "url": "https://toomva.com/Hoc-tieng-Anh-qua-bai-hat/c=16",
            "number_pages": 91
        }
    ]

    def start_requests(self):
        urls = []
        for config in self.configs: 
            url_page = config['url']
            number_pages = config['number_pages']
            for number_page in range(0,number_pages + 1): 
                tmp_url = url_page + "?page=" + str(number_page)
                urls.append(tmp_url)

        for url in urls: 
            yield scrapy.Request(url=url, callback=self.parse_website)

    def parse_website(self, response):
        lst = response.css('.grid-search-video').css('a').xpath('@href').extract()
        for itm in lst: 
            yield SplashRequest(url=itm, callback=self.parse)

    def parse(self, response):
        subs = response.css('.scroll-sub').css('.sub-line').extract()
        for sub in subs: 
            soup = BeautifulSoup(sub, 'lxml')

            if soup.find(class_ = "sub_en") == None or soup.find(class_ = "sub_vi") == None: 
                continue

            sub_en = soup.find(class_ = "sub_en").text
            sub_vi = soup.find(class_ = "sub_vi").text

            item = BilingualcrawlItem()
            item['english'] = sub_en
            item['vietnamese'] = sub_vi
            yield item