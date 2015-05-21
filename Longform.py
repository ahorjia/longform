import time

__author__ = 'ali.ghorbani'

from scrapy import Spider, Item, Field

class LongformEntry(Item):
    title = Field()
    url_address = Field()
    writer = Field()
    publication = Field()
    publication_date = Field()


class LongformSpider(Spider):
    name = 'Longform'
    allowed_domains = ['longform.org']

    start_urls = ["http://longform.org/posts?page=%d" % d for d in range(1, 540)]

    def parse(self, response):
        time.sleep(2.0)

        self.log('******A response from %s arrived!' % response.url)

        retval = []
        divs = response.xpath("//div[@class='post ']")
        for div in divs:
            url_address = div.xpath("div[@class='content']/h2/a/@href")
            title = div.xpath("div[@class='content']/h2/a/text()")
            publication_date = div.xpath("div[@class='content']/div[@class='dateline']"
                                         "/span[@class='publication_date']/text()")
            writer = div.xpath("div[@class='content']/div[@class='dateline']/span[@class='byline']/a/text()")
            publication = div.xpath("div[@class='content']/div[@class='dateline']/span[@class='publication']/a/text()")

            longformentry = LongformEntry(
                url_address=url_address.extract(),
                title=title.extract(),
                publication_date=publication_date.extract(),
                writer=writer.extract(),
                publication=publication.extract())

            retval.append(longformentry)

        return retval

