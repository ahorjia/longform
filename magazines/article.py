
class Article:

    def __init__(self):
        self.author = None
        self.abstract = None
        self.links = None
        self.full_text = None
        self.location = None
        self.narrow_subject = None
        self.broad_subject = None
        self.subject = None
        self.people = None
        self.title = None
        self.publication_title = None
        self.volume = None
        self.issue = None
        self.pages = None
        self.publication_year = None
        self.publication_date = None
        self.year = None
        self.publisher = None
        self.place_of_publication = None
        self.country_of_publication = None
        self.publication_subjects = None
        self.issn = None
        self.publication_subject = None
        self.source_type = None
        self.language_of_publication = None
        self.document_type = None
        self.document_feature = None
        self.proquest_document_id = None
        self.document_url = None
        self.last_updated = None
        self.database = None
        self.number_of_pages = None
        self.raw_text = None
        pass

    def __unicode__(self):
        return u"{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(
            self.issn,
            self.publication_title,
            self.title,
            self.author,
            self.location,
            self.publication_year,
            self.publication_date,
            self.year,
            self.publisher)

    def __str__(self):
        return unicode(self).encode('utf-8')
