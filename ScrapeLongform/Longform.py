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

class LongformSpider(Spider):
    name = 'Longform'
    allowed_domains = ['longform.org']

    start_urls = ["https://www.longform.org/?p=%d&" % d for d in range(2, 3)]

    def cleanList(stringList):
        return stringList
        
    def parse(self, response):
        time.sleep(2.0)

        print('******A response from %s arrived!' % response.url)

        retval = []
        #articles = response.xpath("//article")

        for cnt, div in enumerate(response.xpath("//div[@class='river-header']"), start=1):
          print("=================")
          articles = div.xpath('./following-sibling::node()[count(preceding-sibling::div[@class="river-header"])=%d]' % cnt).extract()

          for article in articles:
            print("*******************")
            #title = article.xpath(".//h2//text()").extract()
            #print("Title:", title)
            print(article)

        return retval
