import time

__author__ = 'agah'

from scrapy.selector import Selector
from scrapy import Spider
from scrapy import Item, Field
import string

class LongformEntry(Item):
    title = Field()
    url_address = Field()
    summary = Field()
    writers = Field()
    publication_link = Field()
    publication = Field()
    publication_date = Field()
    reading_time = Field()
    post_permlink = Field()
    labels = Field()

class LongformSpider(Spider):
    name = 'Longform'
    allowed_domains = ['longform.org']

    start_urls = ["https://www.longform.org/?p=%d&" % d for d in range(1, 344)]

    def cleanList(stringList):
        return stringList
        
    def parse(self, response):
        time.sleep(2.0)

        print('******A response from %s arrived!' % response.url)

        retval = []
        articles = response.xpath("//article")
        for article in articles:
            title = article.xpath(".//h2//text()").extract()
            url_address = article.xpath("a[@class='post__link']/@href").extract_first()
            summary = article.xpath("div[@class='post__text post__body']//text()").extract()
            writers = article.xpath(".//span[@class='post__authors']//text()").extract()
            publication_link = article.xpath(".//a[@class='post__publication']/@href").extract_first()
            publication = article.xpath(".//a[@class='post__publication']/text()").extract_first()
            publication_date = article.xpath(".//span[@class='post__date']/text()").extract_first()
            reading_time = article.css(".post__duration").xpath(".//text()").extract()
            post_permlink = article.css(".post__permalink").xpath("@href").extract_first()
            labels = article.xpath(".//p[@class='post__labels']//text()").extract()

            longformentry = LongformEntry(
                title=title,
                url_address=url_address,
                summary=summary,
                writers=writers,
                publication_link=publication_link,
                publication=publication,
                publication_date=publication_date,
                reading_time=reading_time,
                post_permlink=post_permlink,
                labels=labels)

            retval.append(longformentry)

        return retval
