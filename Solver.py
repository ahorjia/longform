
import numpy as np
import pickle
import sys
import scipy
import scipy.linalg
from cvxopt import matrix, solvers

file1 = open('U_dump.p', 'rb')
U = pickle.load(file1)
file1.close()

print U.shape

_, clip_size = U.shape

print clip_size
threshold = matrix([20.0])
# data = [val * data_multiple for val in data[0:clip_size]]
data = U
# print len(data)

p_bar = -np.mean(U, axis=0)
# print p_bar

# sys.exit()
print "Done Average..."

# data = data + 0.00001 * np.eye(clip_size)
cov_matrix = np.cov(data, ddof=0)

# [R1, P1] = np.linalg.cholesky(cov_matrix.real)

# print cov_matrix == cov_matrix.T
# print P1
ev, ec = scipy.linalg.eig(cov_matrix)
# print ev
# print ec
print "Done conv..."

cov_matrix_sqrt = scipy.linalg.sqrtm(cov_matrix)

# cov_matrix_sqrt[cov_matrix.real < ] = 5

# print cov_matrix_sqrt

print "Done sqrt..."

# print x_bar.shape
c = matrix(p_bar)
# print c.size
d = matrix([[0.0]] * clip_size)
# print d.size
G = [d]
# print G[0].size
# print cov_matrix_sqrt.shape
G+= [matrix(-cov_matrix_sqrt.real)]
print G[1].size

# print G
h = [threshold, matrix(np.zeros(clip_size, dtype=float).T)]
# print h

A = matrix([[1.0]] * clip_size)
b = matrix([1.0])
sol = solvers.socp(c, Gq=G, hq=h, A=A, b=b)
# print sol['x']
result = sol['x']
# print sum(result)

resultArray = np.array(result)
print resultArray

print sol['status']

# print resultArray.shape
var = np.dot(np.dot(resultArray.T, cov_matrix), resultArray)
print var

# Find the closest document
dot_prod = np.dot(U, result)

print np.argmax(dot_prod)
print "Done!"

# print np.cov(x)
# print x