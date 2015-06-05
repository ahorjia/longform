
import numpy as np
import pickle
from ArticleEntry import ArticleEntry
import math

articles_file_name = "articles.p"
dictionary_file_name = "dictionary.p"
d_output_file_name = "d_output_file.p"

def load_dictionary():
    all_words = pickle.load(open(dictionary_file_name, "rb"))
    print len(all_words)
    return all_words

def expand_dictionary(main_dictionary, trimmed_dictionary):
    ret_val = dict.fromkeys(main_dictionary, 0)

    for word in trimmed_dictionary:
        ret_val[word] = trimmed_dictionary[word]

    return ret_val

def multiply_articles():
    all_words = load_dictionary()

    articles = pickle.load(open(articles_file_name, "rb"))

    a0 = expand_dictionary(all_words, articles[0].dict_0_1)
    a01= expand_dictionary(all_words, articles[0].dict_0_1)

    for article in articles:
        a1 = expand_dictionary(all_words, article.dict_0_1)
        result = np.dot(a1.values(), a0.values())
        print result

        a1 = expand_dictionary(all_words, article.dict_0_1)
        result = sum(np.logical_xor(a1.values(), a01.values()))
        print result

def load_d_matrix():
    all_words = load_dictionary()

    articles = pickle.load(open(articles_file_name, "rb"))

    first_article_index = 0
    last_article_index = len(articles) - 1

    first_article = articles[first_article_index]
    last_article = articles[last_article_index]

    print first_article
    print last_article

    first_article_expanded_word_list = expand_dictionary(all_words, first_article.dict_article_word_prob)
    second_article_expanded_word_list = expand_dictionary(all_words, last_article.dict_article_word_prob)

    d_output = []
    for article in articles:
        if article.id == last_article_index or article.id == first_article_index:
            continue

        new_article = []
        expanded_word_list = expand_dictionary(all_words, article.dict_article_word_prob)

        for word in expanded_word_list:
            s_plus_e = 0.5 * (first_article_expanded_word_list[word] + second_article_expanded_word_list[word])
            new_value = 1 - abs(s_plus_e - expanded_word_list[word])
            new_article.append(new_value)

        d_output.append(new_article)

    file2 = open(d_output_file_name, "wb")
    pickle.dump(d_output, file2)
    file2.close()

    return d_output

load_d_matrix()
