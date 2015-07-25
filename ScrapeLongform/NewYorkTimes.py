import time
import json
import sys
from scrapy import Spider, Item, Field


class ArticleEntry(Item):
    issue = Field()
    title = Field()
    author = Field()
    contents = Field()


def load_new_york_times_urls():
    with open('output.json') as data_file:
        data = json.load(data_file)

    return [d['url_address'][0] for d in data if d['publication'] != [] and
            d['publication'][0] in ["New York Times", "New York Times Magazine"]]

class TheNewYorkerSpider(Spider):
    name = 'NewYorkTimes'
    allowed_domains = ['nytimes.com']

    start_urls = load_new_york_times_urls()

    print start_urls
    def parse(self, response):
        time.sleep(2.0)

        self.log('******A response from %s arrived!' % response.url)

        ret_val = []
        issue = response.xpath('//*[@id="story-meta-footer"]/p/time/text()')
        title = response.xpath('//*[@id="story-heading"]/text()')
        author = response.xpath('//*[@id="story-meta-footer"]/p/span/span/text()')
        contents = response.xpath('//*[@id="story-body"]')

        article_entry = ArticleEntry(
            issue=issue.extract(),
            title=title.extract(),
            author=author.extract(),
            contents=contents.extract())

        ret_val.append(article_entry)

        return ret_val

