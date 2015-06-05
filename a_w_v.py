import pickle

a_c=[];

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

f = open('articles.p','rb');
article = pickle.load(f);
f.close();
f = open('dictionary.p','rb');
d = pickle.load(f);
f.close();

a_f=[];

for item in article:
    total = sum(item.dict_count.values());
    l=[];
    for w in d:
        if w in item.dict_count:
            l.append(float(item.dict_count[w])/float(total));
        else:
            l.append(0);
    a_f.append(l);
    


