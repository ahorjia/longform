
import numpy as np
import pickle
import sys

file1 = open('word_score.p', 'rb')
data = pickle.load(file1)
file1.close()

data_array = np.array(data).T
print "Transposed data array shape" + str(data_array.shape)

U, s, V = np.linalg.svd(data_array, full_matrices=True)

print U.shape, s.shape, V.shape
# (337, 337) (337,) (31669, 31669)

file3 = open('U_dump.p', 'wb')
pickle.dump(U, file3)
file3.close()

print "Done Reducing dimension"

sys.exit()