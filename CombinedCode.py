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

def get_scored_word(ratio, dict_length, word_vector, start, end):
    print "Scoring words..."
    score = []

    print ratio
    start_doc = word_vector[start]
    end_doc = word_vector[end]
    actual_word_doc = []
    for i in range(len(word_vector)):
        if i != start and i != end:
            actual_word_doc.append(word_vector[i])

    for i in range(0, dict_length):
        l = []

        for item in actual_word_doc:
            l.append((1.0/dict_length-(ratio*abs(item[i]-start_doc[i])+(1-ratio)*abs(item[i]-end_doc[i])))/(1.0/dict_length))
        score.append(l)

    score = np.array(score)
    print "Shape of scored words", score.shape
    return score

def reduce_dim(sw):
    print "Reducing Dim..."
    data_array = np.array(sw)
    print "Transposed data array shape" + str(data_array.shape)

    pca = PCA()
    pca.fit(data_array)
    data_array = pca.transform(data_array)

    print "Reduce input size", data_array.shape

    return data_array

def solver(data):
    print "Calling the solver socp...", data.shape

    clip_size, _ = data.shape

    threshold = matrix([10.00])

    p_bar = -np.mean(data, axis=1)
    cov_matrix = np.cov(data)
    cov_matrix_sqrt = scipy.linalg.sqrtm(cov_matrix)
    c = matrix(p_bar)
    d = matrix([[0.0]] * clip_size)
    G = [d]
    G+= [matrix(-cov_matrix_sqrt.real)]
    h = [threshold, matrix(np.zeros(clip_size, dtype=float).T)]
    A = matrix([[1.0]] * clip_size)
    b = matrix([1.0])
    n=clip_size
    Gl = matrix(0.0, (n,n))
    Gl[::n+1] = -1.0
    hl = matrix(0.0, (n,1))

    # print G
    sol = solvers.socp(c, Gq=G, hq=h, A=A, b=b, Gl=Gl, hl=hl)
    result = sol['x']
    resultArray = np.array(result)

    print sol['status']

    var = np.dot(np.dot(resultArray.T, cov_matrix), resultArray)
    print "variance", var

    # Find the closest document
    dot_prod = np.dot(data.T, result)
    closest_doc = np.argmax(dot_prod)
    # print closest_doc

    return closest_doc

from LearnQP import run_qp

def solver2(data):
    print "Calling the solver, scored words shape...", data.shape

    _, clip_size = data.shape

    p_bar = np.mean(data, axis=1)
    print "Length of p_bar", p_bar.shape
    cov_matrix = np.cov(data, ddof=0)
    print "Cov matrix shape", cov_matrix.shape

    result = run_qp(cov_matrix, p_bar)

    var = np.dot(np.dot(result.T, cov_matrix), result)
    print "variance", var

    # Find the closest document
    dot_prod = np.dot(data.T, result)
    closest_doc = np.argmax(dot_prod)
    print closest_doc

    return closest_doc

def test_articles(article_id):
    print all_articles[article_id]

def run():
    start = 200
    end = 220

    print "Running..."
    print test_articles(start)

    data_array = reduce_dim(a_f)

    rng = 3
    doc_length, _ = data_array.shape
    for ratio in [x*1.0/(rng+1) for x in range(1, rng+1)]:
        scored_words = get_scored_word(ratio, doc_length, data_array, start, end)
        print "scored_words shape", scored_words.shape
        result = solver(scored_words)
        # result = solver2(scored_words)

        actualresult = 0
        if result < start:
            actualresult = result
        elif result >= start and result < end:
            actualresult = result + 1
        else:
            actualresult = result + 2

        print test_articles(actualresult)

    print test_articles(end)
    pass

run()