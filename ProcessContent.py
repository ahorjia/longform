
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
import pickle
import re
from datetime import datetime

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

        if author is None:
            author = ""
        else:
            author = author.text

        if contents is not None:
            issue = try_parsing_date(issue.text)
            article = ArticleEntry(id_counter, title.text, author, issue)

            id_counter += 1
            soup = BeautifulSoup(contents.text)
            texts = soup.findAll(text=True)
            built_article_dictionary(the_dictionary, article, texts)

            articles.append(article)

    id_counter = 0
    articles.sort(key=lambda x: x.publication)
    for article in articles:
        article.id = id_counter
        id_counter += 1

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

    article_id = 5
    print articles[article_id]
    print articles[article_id].id
    print articles[article_id].publication
    print articles[article_id].title
    print articles[article_id].writer
    print articles[article_id].dict_0_1['hi'] # 1
    print articles[article_id].dict_count['hi'] # 23
    print len(articles[article_id].dict_0_1)
    print len(articles[article_id].dict_count)

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

def find_article_intersection():
    article1_index = 34
    article2_index = 76

    words = load_dictionary();
    articles = pickle.load(open(articles_file_name, "rb"))

    article1 = articles[article1_index]
    article2 = articles[article2_index]
    common_count = 0

    for word in words:
        if article1.dict_0_1.has_key(word) and article2.dict_0_1.has_key(word):
            common_count += 1

    print common_count
    pass


def try_parsing_date(text):
    text = text.replace('SEPT.', 'SEP.')
    for fmt in ('%b. %d, %Y', '%B %d, %Y'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass

    print text


def find_articles_with_no_date():
    all_dates = []
    articles = pickle.load(open(articles_file_name, "rb"))
    print len(articles)

    no_date_count = 0
    for article in articles:
        # print article
        if article.publication is None or article.publication == "":
            no_date_count += 1
        # dt = article.publication.remove
        all_dates.append(try_parsing_date(article.publication))

    all_dates.sort()
    print all_dates
    # print no_date_count

process_articles("NewYorkTimes.xml")
test_articles()
# build_bipartite_graph()
# test_build_bipartite_graph()
# find_article_intersection()
# find_articles_with_no_date()