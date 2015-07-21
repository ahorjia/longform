from collections import defaultdict
import operator
import pprint
from constants import long_form_output

with open(long_form_output, "r") as dataFile:
    data = eval(dataFile.read())

print "Total Row Count", len(data)

writerCountPerArticle = defaultdict(int)
writers = set()
for article in data:
    writers |= set(article['writer'])
    writerCountPerArticle[len(article['writer'])] += 1

print "# of writers per article", writerCountPerArticle
print "# of unique writers", len(writers)

publicationCountPerArticle = defaultdict(int)
publications = set()
for article in data:
    publications |= set(article['publication'])
    publicationCountPerArticle[len(article['publication'])] += 1

print "# of publications per article", publicationCountPerArticle
print "# of unique publications", len(publications)

writerArticles = defaultdict(int)
publicationArticles = defaultdict(int)

for article in data:
    for writer in article['writer']:
        writerArticles[writer] += 1

    for publication in article['publication']:
        publicationArticles[publication] += 1

sorted_writers = sorted(writerArticles.items(), key=operator.itemgetter(1), reverse=True)
sorted_publications = sorted(publicationArticles.items(), key=operator.itemgetter(1), reverse=True)

pp = pprint.PrettyPrinter(depth=6)
print "Top Writers"
pp.pprint(sorted_writers[:5])

print "Top Publications"
pp.pprint(sorted_publications[:20])
