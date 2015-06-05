
class ArticleEntry:
    id = 0
    title = ""
    writer = ""
    publication = ""
    dict_0_1 = {}
    dict_count = {}
    dict_article_word_prob = {}

    def __init__(self, id, title, writer, publication):
        self.id = id
        self.title = title
        self.writer = writer
        self.publication = publication

    def __unicode__(self):
        return u"{0}, {1}, {2}".format(self.title, self.writer, self.publication)

    def __str__(self):
        return unicode(self).encode('utf-8')

