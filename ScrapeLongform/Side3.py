# Basic Statistics

from collections import defaultdict
import operator
import pprint
import pickle

clean_data_output = "Side2Result.pkl"
with open(clean_data_output, "rb") as dataFile:
    data = pickle.load(dataFile)

print("Total Article Count", len(data))

writerCountPerArticle = defaultdict(int)
writers = set()
for article in data:
    writers |= set(article['writers'])
    writerCountPerArticle[len(article['writers'])] += 1

print(writers)
print("# of writers per article", writerCountPerArticle)
print("# of unique writers", len(writers))

publicationCountPerArticle = defaultdict(int)
publications = set()
for article in data:
    if article['publication'] is not None:
        publications |= set(article['publication'])
        publicationCountPerArticle[len(article['publication'])] += 1

print("# of publications per article", publicationCountPerArticle)
print("# of unique publications", len(publications))

writerArticles = defaultdict(int)
publicationArticles = defaultdict(int)
publicationWriter = defaultdict(int)
writer_publications = dict()
publication_writers = dict()

for article in data:
    for writer in article['writers']:
        writerArticles[writer] += 1

    if article['publication'] is not None:
        publicationArticles[article['publication']] += 1

    if article['publication'] is not None:
        for writer in article['writers']:
            publicationWriter[(article['publication'], writer)] += 1

            if writer not in writer_publications:
                writer_publications[writer] = set()
            writer_publications[writer].add(article['publication'])

            if article['publication'] not in publication_writers:
                publication_writers[article['publication']] = set()
            publication_writers[article['publication']].add(writer)

sorted_writers = sorted(writerArticles.items(), key=operator.itemgetter(1), reverse=True)
print(publicationArticles)
sorted_publications = sorted(publicationArticles.items(), key=operator.itemgetter(1), reverse=True)

pp = pprint.PrettyPrinter(depth=6)
print("Top Writers")
pp.pprint(sorted_writers[:10])

print("Top Publications")
pp.pprint(sorted_publications[:10])

sorted_publications_writers = sorted(publicationWriter.items(), key=operator.itemgetter(1), reverse=True)
print("Top Publication + Writer")
pp.pprint(sorted_publications_writers[:10])

print("Publication Writers")
pp.pprint(publication_writers['longform.org'])
