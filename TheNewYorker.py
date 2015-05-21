import time
import json
import sys
from scrapy import Spider, Item, Field


class ArticleEntry(Item):
    issue = Field()
    title = Field()
    author = Field()
    content = Field()


def load_new_yorker_urls():
    with open('output.json') as data_file:
        data = json.load(data_file)

    return [d['url_address'][0] for d in data if d['publication'] != [] and d['publication'][0] == "New Yorker"]

class TheNewYorkerSpider(Spider):
    name = 'TheNewYorker'
    allowed_domains = ['newyorker.com']

    start_urls = load_new_yorker_urls()

    def parse(self, response):
        time.sleep(2.0)

        self.log('******A response from %s arrived!' % response.url)

        ret_val = []
        issue = response.xpath("//*[@id='masthead']/h4/a[2]/span/text()")
        title = response.xpath('//*[@id="masthead"]/h1/text()')
        author = response.xpath("//*[@id='masthead']/h3/span/a/span/text()")
        content = response.xpath('//*[@id="articleBody"]')

        article_entry = ArticleEntry(
            issue=issue.extract(),
            title=title.extract(),
            author=author.extract(),
            content=content.extract())

        ret_val.append(article_entry)

        return ret_val

