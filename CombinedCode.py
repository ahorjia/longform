from sklearn.decomposition import PCA
import numpy as np
import pickle
import scipy
import scipy.linalg
from cvxopt import matrix, solvers
from ArticleEntry import ArticleEntry

articles_file_name = "articles.p"

f = open('a_w_v.p', 'rb')
a_f = pickle.load(f)
f.close()

f = open('dictionary.p', 'rb')
d = pickle.load(f)
f.close()

f = open(articles_file_name, "rb")
all_articles = pickle.load(f)
f.close()

def get_scored_word(ratio, dict_length, word_vector):
    print "Scoring words..."
    score = []

    print ratio
    for i in range(0, dict_length):
        l = []
        for item in word_vector[1:-1]:
            l.append((1.0/dict_length-(ratio*abs(item[i]-word_vector[0][i])+(1-ratio)*abs(item[i]-word_vector[-1][i])))/(1.0/dict_length))
        score.append(l)

    return score

def reduce_dim(scored_words):
    print "Reducing Dim..."
    data_array = np.array(scored_words)
    print "Transposed data array shape" + str(data_array.shape)

    pca = PCA()
    pca.fit(data_array)
    data_array = pca.transform(data_array)

    print data_array.shape

    return data_array

def solver(U):
    print "Calling the solver..."
    print U.shape

    _, clip_size = U.shape

    threshold = matrix([10.0])
    data = U

    p_bar = -np.mean(U, axis=0)
    cov_matrix = np.cov(data, ddof=0)
    cov_matrix_sqrt = scipy.linalg.sqrtm(cov_matrix)
    c = matrix(p_bar)
    d = matrix([[0.0]] * clip_size)
    G = [d]
    G+= [matrix(-cov_matrix_sqrt.real)]
    h = [threshold, matrix(np.zeros(clip_size, dtype=float).T)]
    A = matrix([[1.0]] * clip_size)
    b = matrix([1.0])
    sol = solvers.socp(c, Gq=G, hq=h, A=A, b=b)
    result = sol['x']
    resultArray = np.array(result)

    print sol['status']

    var = np.dot(np.dot(resultArray.T, cov_matrix), resultArray)
    print "variance", var

    # Find the closest document
    dot_prod = np.dot(U, result)
    closest_doc = np.argmax(dot_prod)
    print closest_doc

    return closest_doc

def test_articles(article_id):
    print all_articles[article_id]

def run():
    print "Running..."
    print test_articles(0)

    data_array = reduce_dim(a_f)
    print data_array.shape

    for ratio in [0.25, 0.5, 0.75]:
        scored_words = get_scored_word(ratio, 337, data_array)
        result = solver(np.array(scored_words))
        print test_articles(result + 1)

    print test_articles(338)
    pass

run()