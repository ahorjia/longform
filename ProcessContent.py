
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
import pickle
import re

_digits = re.compile('\d')
dictionary_file_name = "dictionary.p"
articles_file_name = "articles.p"
stemmer = PorterStemmer()

class ArticleEntry:
    title = ""
    writer = ""
    publication = ""
    dict_0_1 = {}
    dict_count = {}

    def __init__(self, title, writer, publication):
        self.title = title
        self.writer = writer
        self.publication = publication

    def __unicode__(self):
        return u"{0}, {1}, {2}".format(self.title, self.writer, self.publication)

    def __str__(self):
        return unicode(self).encode('utf-8')

def built_article_dictionary(the_dictionary, article, texts):
    tokenizer = RegexpTokenizer(r'\w+')
    article.dict_0_1 = dict.fromkeys(the_dictionary, 0)
    article.dict_count = dict.fromkeys(the_dictionary, 0)

    for w in texts:
        word_list = [stemmer.stem(word.lower()) for word in tokenizer.tokenize(w)]
        for word in word_list:
            if word in the_dictionary:
                article.dict_0_1[word] = 1
                article.dict_count[word] += 1
    pass

def process_articles(file_name):
    the_dictionary = load_dictionary();
    articles = []
    e = ET.parse(file_name).getroot()
    for atype in e.findall('item'):
        contents = atype.find('contents/value')
        issue = atype.find('issue/value')
        title = atype.find('title/value')
        author = atype.find('author/value')

        if issue is not None and title is not None and author is not None and contents is not None:
            article = ArticleEntry(title.text, author.text, issue.text)

            soup = BeautifulSoup(contents.text)
            texts = soup.findAll(text=True)
            built_article_dictionary(the_dictionary, article, texts)

            articles.append(article)

    print len(articles)
    pickle.dump(articles, open(articles_file_name, "wb"))
    print "done"


def load_dictionary():
    all_words = pickle.load(open(dictionary_file_name, "rb"))
    print len(all_words)
    return all_words

def test_articles():
    articles = pickle.load(open(articles_file_name, "rb"))
    print len(articles) # 182
    print articles[5] # Hong Kong's Umbrella Revolution Isn't Over Yet, LAUREN HILGERS, FEB. 18, 2015
    print articles[5].dict_0_1['hi'] # 1
    print articles[5].dict_count['hi'] # 23

# process_articles("NewYorkTimes.xml")
test_articles()