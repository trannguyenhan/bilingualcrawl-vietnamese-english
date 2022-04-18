import scrapy

from bilingualcrawl.spiders.detail_toomva import DetailToomvaSpider


class ToomvaLearnSpider(DetailToomvaSpider):
    name = 'toomva_learn'

    configs = [
        {
            "url": "https://toomva.com/Video-Hoc-Tieng-Anh/c=45",
            "number_pages": 8
        }
    ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
