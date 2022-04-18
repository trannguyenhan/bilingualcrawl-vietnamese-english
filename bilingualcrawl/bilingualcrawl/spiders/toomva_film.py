import scrapy

from bilingualcrawl.spiders.detail_toomva import DetailToomvaSpider


class ToomvaLearnSpider(DetailToomvaSpider):
    name = 'toomva_film'

    configs = [
        {
            "url": "https://toomva.com/Hoc-tieng-Anh-qua-phim/c=14",
            "number_pages": 130
        }
    ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
