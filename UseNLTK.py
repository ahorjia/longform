
from constants import *
import pickle
from ArticleEntry import ArticleEntry

def load_articles():
    print "Loading the articles..."
    articles = pickle.load(open(articles_file_name, "rb"))
    print "# of articles", len(articles)
    return articles

if __name__ == '__main__':
    articles = load_articles()

    text_index = 0

    print articles[text_index]
    print articles