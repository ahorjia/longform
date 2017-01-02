# -*- coding: utf-8 -*-
import scrapy


class LongformSpider(scrapy.Spider):
    name = "Longform"
    allowed_domains = ["longform.org"]
    start_urls = (
        'http://www.longform.org/',
    )

    def parse(self, response):
        pass
