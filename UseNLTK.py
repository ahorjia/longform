
from constants import *
import pickle
from ArticleEntry import ArticleEntry
import matplotlib.pyplot as plt
import nltk
from nltk import FreqDist

def load_articles():
    print "Loading the articles..."
    articles = pickle.load(open(articles_file_name, "rb"))
    print "# of articles", len(articles)
    return articles

def load_articles_tokenize():
    print "Loading the articles..."
    articles = pickle.load(open(articles_file_name, "rb"))
    print "# of articles", len(articles)

    text_titles = []
    text_lens = []
    text_set_lens = []
    for article in articles:

        text_titles.append(article.title)
        text_lens.append(len(article.nltk_text))
        text_set_lens.append(len(set(article.nltk_text)))

        # print sorted(set([w for w in article.nltk_text if len(w) > 20]))
        # fdist1 = FreqDist(article.nltk_text)
        # fdist1.plot(10, cumulative=True)

        print article.nltk_text.collocations()

def plot_data(x, y):
    plt.plot(x, y)

if __name__ == '__main__':
    load_articles_tokenize()