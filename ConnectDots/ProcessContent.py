
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
import pickle
import re
from datetime import datetime
import time
from ArticleEntry import ArticleEntry
from constants import *

_digits = re.compile('\d')

stemmer = PorterStemmer()

def built_article_dictionary(the_dictionary, article, texts):
    tokenizer = RegexpTokenizer(r'\w+')
    article.dict_0_1 = {}
    article.dict_count = {}
    article.dict_article_word_prob = {}

    for w in texts:
        word_list = [stemmer.stem(word.lower()) for word in tokenizer.tokenize(w)]
        for word in word_list:
            if word in the_dictionary:
                article.dict_0_1[word] = 1
                if article.dict_count.has_key(word):
                    article.dict_count[word] += 1
                else:
                    article.dict_count[word] = 1

    for word in article.dict_count:
        article.dict_article_word_prob[word] = article.dict_count[word] * 1.0 / len(the_dictionary)

    # print article.dict_article_word_prob
    pass

def process_articles(file_name, output_file_name):
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
            if issue is not None:
                issue = try_parsing_date(issue.text)
            id_counter += 1
            soup = BeautifulSoup(contents.text)
            texts = soup.findAll(text=True)

            article = ArticleEntry(id_counter, title.text, author, issue, texts)

            built_article_dictionary(the_dictionary, article, texts)

            articles.append(article)

    id_counter = 0
    articles.sort(key=lambda x: x.publication)
    for article in articles:
        article.id = id_counter
        id_counter += 1

    print len(articles)
    pickle.dump(articles, open(output_file_name, "wb"))
    print "done"


def load_dictionary():
    all_words = pickle.load(open(dictionary_file_name, "rb"))
    print len(all_words)
    return all_words


def test_articles(output_file_name):
    articles = pickle.load(open(output_file_name, "rb"))
    print len(articles) # 339

    # article_id = 67
    # print articles[article_id]
    # print articles[article_id].id
    # print articles[article_id].publication
    # print articles[article_id].title
    # print articles[article_id].writer
    # # print articles[article_id].dict_0_1
    # print articles[article_id].dict_0_1['hi'] # 1
    # print articles[article_id].dict_count['hi'] # 23
    # print articles[article_id].dict_article_word_prob['hi']
    # print len(articles[article_id].dict_0_1)
    # print len(articles[article_id].dict_count)

    print "********************"
    print articles[0]
    # print articles[0].content
    print (len(articles[0].content))
    # print articles[295]
    # print articles[327]
    # print articles[332]
    # print articles[338]
    # print articles[27]
    # print articles[100]

    # for article in articles:
    #     print article


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

    word = 'hi'
    print len(word_to_article_map[word])
    print word_to_article_map[word]

    print len(article_to_word_map[34])
    pass

def find_article_intersection():
    article1_index = 34
    article2_index = 76

    words = load_dictionary()
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


def li_code():
    word_to_article_map = pickle.load(open(word_to_article_file_name, "rb"))

    articles_file = open(articles_file_name, "rb")
    articles = pickle.load(articles_file)
    articles_file.close()
    article_word_count = dict()
    articles_stat = articles

    # count word in each article
    for item in articles_stat:
        article_word_count[item.id] = dict()
        for w in item.dict_count:
            article_word_count[item.id][w] = item.dict_count[w]

    # calculate article -> word weight
    article_word_prob = dict()
    for item in article_word_count:
        article_word_prob[item] = dict()
        total = sum(article_word_count[item].values())
        for w in article_word_count[item]:
            article_word_prob[item][w] = float(article_word_count[item][w]) / float(total)

    word_l = word_to_article_map.keys()
    word_to_article_prob = dict()
    # calculate word->article weight
    for item in word_l:
        word_to_article_prob[item] = dict()
        for a in article_word_prob:
            if item in article_word_prob[a]:
                word_to_article_prob[item][a] = article_word_prob[a][item]

    # normalize
    word_to_article_prob_norm=dict()
    for item in word_to_article_prob:
        word_to_article_prob_norm[item]=dict()
        total=sum(word_to_article_prob[item].values())
        for p in word_to_article_prob[item]:
            word_to_article_prob_norm[item][p]=float(word_to_article_prob[item][p])/float(total)

    # generate original matrix
    origin = []
    for st in article_word_prob:
        l = [0.0] * 339
        for w in article_word_prob[st]:
            for ed in word_to_article_prob_norm[w]:
                l[ed] += article_word_prob[st][w] * word_to_article_prob_norm[w][ed]
        origin.append(l)

    start_time = time.clock()
    build_mat_coll(word_to_article_map, word_to_article_prob_norm, article_word_prob)
    print "Total time:" + str(time.clock() - start_time)

    print "Done Processing"

def build_mat_coll(word_to_article_map, word_to_article_prob_norm, article_word_prob):
    threshold = 20
    mat_coll = dict()
    print len(word_to_article_prob_norm)
    process_counter = 0
    for w in word_to_article_prob_norm:
        if process_counter % 10 == 0:
            print process_counter

        process_counter += 1

        if len(word_to_article_map[w]) <= threshold:
            continue

        sink_word = w # build matrix if w is a sink word
        mat_coll[sink_word] = []
        for st in article_word_prob:
            l = [0.0] * 339
            for w2 in article_word_prob[st]:  # w2 as a middle between 2 document
                if w2 != sink_word:
                    for ed in word_to_article_prob_norm[w2]:
                        l[ed] += article_word_prob[st][w2] * word_to_article_prob_norm[w2][ed]

            mat_coll[sink_word].append(l)  # append one row of the matrix

    print len(mat_coll[sink_word])
    pickle.dump(mat_coll, open(mat_coll_file_name, "wb"))

if __name__ == '__main__':
    in1 = "pickles/TheNewYorker.xml"
    out1 = thenewyorker_output
    process_articles(in1, out1)
    # process_articles("NewYorkTimes.xml", articles_file_name)
    # process_articles()
    test_articles(out1)
    # build_bipartite_graph()
    # test_build_bipartite_graph()
    # find_article_intersection()
    # find_articles_with_no_date()
    # li_code()
    pass
