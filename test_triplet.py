import numpy as np
from scipy.sparse import coo_matrix
from triplet import Triplet

A = np.array([[1.1, 0, 0, 2],
            [0, 1, 0, 0],
            [0, 0, 2.3, 0],
            [0.5, 2, 0, 2]])

A_sparse = Triplet()

n, m = A.shape
for I in range(n):
    for J in range(m):
        A_sparse.append(I, J, A[I][J])

coo_A = coo_matrix(A_sparse.data, shape=(n, m))
print("A creuse: ")
print(coo_A.toarray())
print("A pleine: ")
print(A)

