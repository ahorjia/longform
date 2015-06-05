
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
import os.path

_digits = re.compile('\d')
dictionary_file_name = "dictionary.p"
articles_file_name = "articles.p"
word_to_article_file_name = "word_to_article.p"
article_to_word_file_name = "article_to_word.p"
mat_coll_file_name_format = "output/mat_coll_file_word_{0}.p"
origin_file_name = "origin.p"

def build_origin():
    file1 = open(word_to_article_file_name, "rb")
    word_to_article_map = pickle.load(file1)
    file1.close()

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
    #
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

    # file_origin = open(origin_file_name, "wb")
    # pickle.dump(origin, file_origin)
    # file_origin.close()

    start_time = time.clock()
    build_mat_coll(word_to_article_map, word_to_article_prob_norm, article_word_prob)
    print "Total time:" + str(time.clock() - start_time)

    print "Done Processing"

def build_mat_coll(word_to_article_map, word_to_article_prob_norm, article_word_prob):

    u_threshold = 50
    l_threshold = 20
    print len(word_to_article_prob_norm)
    process_counter = 0
    main_counter = 0
    for w in word_to_article_prob_norm:
        mat_coll = dict()
        process_counter += 1
        w_len = len(word_to_article_map[w])

        output_file_name = mat_coll_file_name_format.format(w.encode('punycode'))
        if os.path.isfile(output_file_name):
            continue

        if w_len >= u_threshold or w_len < l_threshold:
            continue

        if main_counter % 10 == 0:
            print main_counter

        main_counter += 1
        sink_word = w # build matrix if w is a sink word
        mat_coll[sink_word] = []
        for st in article_word_prob:
            l = [0.0] * 339
            for w2 in article_word_prob[st]:  # w2 as a middle between 2 document
                if w2 != sink_word:
                    for ed in word_to_article_prob_norm[w2]:
                        l[ed] += article_word_prob[st][w2] * word_to_article_prob_norm[w2][ed]

            mat_coll[sink_word].append(l)  # append one row of the matrix

        file2 = open(output_file_name, "wb")
        pickle.dump(mat_coll, file2)
        file2.close()

    print main_counter
    # pass

build_origin()
