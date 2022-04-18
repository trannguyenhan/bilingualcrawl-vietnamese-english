import scrapy

from bilingualcrawl.spiders.detail_toomva import DetailToomvaSpider


class ToomvaLearnSpider(DetailToomvaSpider):
    name = 'toomva_music'

    configs = [
        {
            "url": "https://toomva.com/Hoc-tieng-Anh-qua-bai-hat/c=16",
            "number_pages": 91
        }
    ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
