
class ProquestArticle:

    def __init__(self):
        self.author = ""
        self.abstract = ""
        self.links = ""
        self.full_text = ""
        self.location = ""
        self.narrow_subject = ""
        self.borad_subject = ""
        self.people = ""
        self.title = ""
        self.publication_title = ""
        self.volume = ""
        self.issue = ""
        self.pages = ""
        self.publication_year = ""
        self.publication_date = ""
        self.year = ""
        self.publisher = ""
        self.place_of_publication = ""
        self.country_of_publication = ""
        self.publication_subjects = ""
        self.issn = ""
        self.source_type = ""
        self.language_of_publication = ""
        self.document_type = ""
        self.document_feature = ""
        self.proquest_document_id = ""
        self.document_url = ""
        self.last_updated = ""
        self.database = ""
        pass

    def __unicode__(self):
        return u"{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(self.issn,
            self.publication_title, self.title,
            self.author, self.location, self.publication_year,
            self.publication_date, self.year, self.publisher)

    def __str__(self):
        return unicode(self).encode('utf-8')
