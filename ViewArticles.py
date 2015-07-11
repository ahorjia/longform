__author__ = 'ali.ghorbani'

import pickle
from constants import articles_file_name

def print_articles(indices):
    articles = pickle.load(open(articles_file_name, "rb"))

    for index in indices:
        print articles[index]

if __name__ == '__main__':
    print_articles([235, 252, 311, 322, 326])
    print "***********************"
    print_articles([255, 276, 295, 305, 312, 323, 327, 331, 332])