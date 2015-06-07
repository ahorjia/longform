
import numpy as np
import pickle
import sys
from sklearn.decomposition import PCA

file1 = open('word_score.p', 'rb')
data = pickle.load(file1)
file1.close()

data_array = np.array(data).T
print "Transposed data array shape" + str(data_array.shape)

# U, s, V = np.linalg.svd(data_array, full_matrices=True)
pca = PCA()
pca.fit(data_array)
data_array = pca.transform(data_array)

print data_array.shape
# print U.shape, s.shape, V.shape
# (337, 337) (337,) (31669, 31669)

file3 = open('data_array.p', 'wb')
pickle.dump(data_array, file3)
file3.close()

print "Done Reducing dimension"

sys.exit()