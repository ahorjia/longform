########################################
from math import sqrt
from cvxopt import matrix
from cvxopt.blas import dot
from cvxopt.solvers import qp, options

def run_qp(cov_matrix, pbar):

    n = len(pbar)
    G = matrix(0.0, (n,n))
    G[::n+1] = -1.0
    h = matrix(0.0, (n,1))
    A = matrix(1.0, (1,n))
    b = matrix(1.0)

    N = 100
    mus = [10**(5.0*t/N-1.0) for t in range(N)]
    options['show_progress'] = False

    # print pbar
    mu = 0.5
    xs = qp(mu*matrix(cov_matrix), matrix(-pbar), G, h, A, b)['x']
    # print xs
    # print sum(xs)
    # xs = qp(mu*cov_matrix, -pbar, G, h, A, b)['x']

    return xs

    # xs = [qp(mu*S, -pbar, G, h, A, b)['x'] for mu in mus]
    # returns = [dot(pbar,x) for x in xs]
    # risks = [sqrt(dot(x, S*x)) for x in xs]
    # return returns, risks

    pass

