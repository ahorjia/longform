__author__ = 'ali.ghorbani'

import pickle
from constants import articles_file_name
from sklearn.cluster import KMeans
import numpy as np
from MultiplyArticles import expand_dictionary, load_dictionary

def cluster_articles() :
    articles = pickle.load(open(articles_file_name, "rb"))

    combined_list = []
    all_words = load_dictionary()
    for article in articles:
        expanded_words = expand_dictionary(all_words, article.dict_0_1)
        combined_list.append(expanded_words.values())

    print len(combined_list)
    print len(combined_list[0])
    list_array = np.array(combined_list)
    print "List Array Shape", list_array.shape
    # cluster_dict = cluster(list_array)
    cluster_hierarchical(list_array, articles)

    # pickle.dump()
    # print cluster_dict[3]

def cluster_hierarchical(X, articles):
    from scipy.cluster.hierarchy import dendrogram, linkage
    from pylab import rcParams
    from matplotlib import pyplot as plt
    rcParams['figure.figsize'] = 5, 10

    linkage_matrix = linkage(X, "ward")

    labels = [unicode(article) for article in articles]
    plt.clf()

    dendrogram(linkage_matrix,
               color_threshold=1,
               labels=labels,
               orientation='right')

    # plt.gca().axes.get_xaxis().set_visible(False)
    # plt.tight_layout()
    plt.show()

def cluster(X):
    max_cluster_count = 3
    cluster_dict = dict((item, 0) for item in range(2, max_cluster_count + 1))
    for cluster_count in cluster_dict:
        print "Starting to cluster...", cluster_count
        estimator = KMeans(n_clusters=cluster_count, init='k-means++', n_init=100, max_iter=1000)
        estimator.fit(X)

        groups = [[] for _ in range(cluster_count)]
        labels = estimator.labels_

        index = 0
        for label in labels:
            groups[label].append(index)
            index += 1

        cluster_dict[cluster_count] = groups

    return cluster_dict

if __name__ == '__main__':
    cluster_articles()