__author__ = 'ali.ghorbani'


class ArticlesBasicStats:

    def __init__(self, pas):
        self.pas = pas

    def get_total_article_count(self):
        return len(self.pas)

    def basic_report(self):
        print "Total # of articles", len(self.pas)
        print "Total # of articles with no full-text",\
            len([pa for pa in self.pas if pa.full_text is not None])
        print "Text len for articles that have full-text",\
            [len(pa.full_text) for pa in self.pas if pa.full_text is not None]

    def full_text_articles_of_give_size(self, given_size):
        for pa in self.pas:
            if pa.full_text is not None and len(pa.full_text) <= given_size:
                print pa.raw_text

