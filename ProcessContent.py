
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
word_to_article_file_name = "word_to_article.p"
article_to_word_file_name = "article_to_word.p"

stemmer = PorterStemmer()

class ArticleEntry:
    id = 0
    title = ""
    writer = ""
    publication = ""
    dict_0_1 = {}
    dict_count = {}

    def __init__(self, id, title, writer, publication):
        self.id = id
        self.title = title
        self.writer = writer
        self.publication = publication

    def __unicode__(self):
        return u"{0}, {1}, {2}".format(self.title, self.writer, self.publication)

    def __str__(self):
        return unicode(self).encode('utf-8')

def built_article_dictionary(the_dictionary, article, texts):
    tokenizer = RegexpTokenizer(r'\w+')
    article.dict_0_1 = {}
    article.dict_count = {}

    for w in texts:
        word_list = [stemmer.stem(word.lower()) for word in tokenizer.tokenize(w)]
        for word in word_list:
            if word in the_dictionary:
                article.dict_0_1[word] = 1
                if article.dict_count.has_key(word):
                    article.dict_count[word] += 1
                else:
                    article.dict_count[word] = 1
    pass

def process_articles(file_name):
    the_dictionary = load_dictionary();
    articles = []
    e = ET.parse(file_name).getroot()
    id_counter = 0
    for atype in e.findall('item'):
        contents = atype.find('contents/value')
        issue = atype.find('issue/value')
        title = atype.find('title/value')
        author = atype.find('author/value')

        if issue is None:
            issue = ""
        else:
            issue = issue.text

        if title is None:
            title = ""
        else:
            title = title.text

        if author is None:
            author = ""
        else:
            author = author.text

        if contents is not None:
            article = ArticleEntry(id_counter, title, author, issue)

            id_counter += 1
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
    print len(articles) # 339

    # The type of the articles[78] is ArticleEntry
    print articles[5] # Hong Kong's Umbrella Revolution Isn't Over Yet, LAUREN HILGERS, FEB. 18, 2015
    print articles[5].id
    print articles[5].publication
    print articles[5].title
    print articles[5].writer
    print articles[5].dict_0_1['hi'] # 1
    print articles[5].dict_count['hi'] # 23
    print len(articles[5].dict_0_1)
    print len(articles[5].dict_count)

    for article in articles:
        print article


def build_bipartite_graph():
    words = load_dictionary();
    articles = pickle.load(open(articles_file_name, "rb"))

    article_to_word = {}
    for article in articles:
        article_to_word[article.id] = []

    word_to_article = {}
    for word in words:
        word_to_article[word] = []

    for word in words:
        for article in articles:
            if article.dict_0_1.has_key(word) and article.dict_0_1[word] == 1: # The same thing!
                article_to_word[article.id].append(word)
                word_to_article[word].append(article.id)

    pickle.dump(word_to_article, open(word_to_article_file_name, "wb"))
    pickle.dump(article_to_word, open(article_to_word_file_name, "wb"))
    print "Done Building Word To Article Map"
    pass


def test_build_bipartite_graph():
    word_to_article_map = pickle.load(open(word_to_article_file_name, "rb"))
    article_to_word_map = pickle.load(open(article_to_word_file_name, "rb"))

    word = 'artajo'
    print len(word_to_article_map[word])
    print word_to_article_map[word]

    print len(article_to_word_map[34])
    pass

# process_articles("NewYorkTimes.xml")
# test_articles()
# build_bipartite_graph()
test_build_bipartite_graph()
