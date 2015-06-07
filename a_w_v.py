import pickle
from ArticleEntry import ArticleEntry

a_c = []

f = open('articles.p','rb')
article = pickle.load(f)
f.close()
f = open('dictionary.p','rb')
d = pickle.load(f)
f.close()

a_f = []

for item in article:
    total = sum(item.dict_count.values())
    l = []
    for w in d:
        if w in item.dict_count:
            l.append(float(item.dict_count[w])/float(total))
        else:
            l.append(0)
    a_f.append(l)
