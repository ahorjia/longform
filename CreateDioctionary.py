
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
import pickle
import re

_digits = re.compile('\d')
dictionary_file_name = "dictionary.p"
stemmer = PorterStemmer()

def build_dictionary(texts, all_words):
    tokenizer = RegexpTokenizer(r'\w+')
    for w in texts:
        word_list = [stemmer.stem(word.lower()) for word in tokenizer.tokenize(w)]
        word_list = [w for w in word_list if w not in stopwords.words('english')]
        for word in word_list:
            if not bool(_digits.search(word)):
                all_words.add(word)

    pass

def load_file_content(file_name):
    all_words = set()
    e = ET.parse(file_name).getroot()
    for atype in e.findall('item'):
        contents = atype.find('contents/value')

        if contents is not None:
            soup = BeautifulSoup(contents.text)
            texts = soup.findAll(text=True)
            build_dictionary(texts, all_words)

    pickle.dump(all_words, open(dictionary_file_name, "wb"))
    print all_words
    print len(all_words) # 31669


def verify_dictionary():
    all_words2 = pickle.load(open(dictionary_file_name, "rb"))
    print all_words2
    print len(all_words2)
    pass

load_file_content("NewYorkTimes.xml")
verify_dictionary()
