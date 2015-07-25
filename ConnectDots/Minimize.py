

from cvxopt import matrix
from cvxopt import solvers

if __name__ == '__main__':
    P = matrix([[13.0, 12.0, -2.0], [12.0, 17.0, 6.0], [-2.0, 6.0, 12.0]])
    q = matrix([-22.0, -14.5, 13.0])
    r = 1
    G = matrix([[1.0, -1.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 1.0, -1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 1.0, -1.0]])
    h = matrix([1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

    sol = solvers.qp(P, q, G, h)

    print "Status:"
    print sol['status']

    print "X:"
    print sol['x']

    print "Primal Objective:"
    print sol['primal objective'] + r

    pass
