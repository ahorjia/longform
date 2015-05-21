
import xml.etree.ElementTree as ET
from scrapy import Item, Field
from bs4 import BeautifulSoup
import sys

class ArticleEntry(Item):
    issue = Field()
    title = Field()
    author = Field()
    contents = Field()

all_words = set()

def build_dictionary(texts):
    for w in texts:
        all_words.add(w)

    pass

def load_file_content(file_name):
    e = ET.parse(file_name).getroot()
    for atype in e.findall('item'):
        issue = atype.find('issue/value')
        title = atype.find('title/value')
        author = atype.find('author/value')
        contents = atype.find('contents/value')

        # if issue is not None:
        #     print issue.text
        #
        # if title is not None:
        #     print title.text

        # if author is not None:
        #     print author.text

        if contents is not None:
            soup = BeautifulSoup(contents.text)
            texts = soup.findAll(text=True)
            build_dictionary(texts)


load_file_content("NewYorkTimes.xml")
print all_words
print len(all_words)