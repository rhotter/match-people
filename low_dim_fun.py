import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, MDS
# from itertools import permutations
import matplotlib.pyplot as plt

X = []
n=5

X = []
for i in range(n):
  for j in range(n):
    for k in range(n):
      for l in range(n):
        X.append([i,j,k,l])
print("built")
# X = np.array(list(permutations([i for i in range(k)])))
# print(X)

mds = MDS(n_components=2)
X_reduced = mds.fit_transform(X)

plt.scatter(X_reduced[:,0],X_reduced[:,1], s=3)
plt.show()