import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

print("load cards")
import dims

# normalize
print("get vecs")
names = list(enumerate(dims.cdb.values()))

_, v = dims.to_vec(dims.cdb.values())

print("normalize")
maxlen = max(map(len, v))
X = [np.pad(np.array(x, np.float32), (0, maxlen-len(x)), 'constant') for x in v]

X = StandardScaler().fit_transform(X)

print("compute pca")
pca = PCA(n_components=2).fit_transform(X)

print("plotting")
import matplotlib.pyplot as plt
pcaT = pca.transpose()
data = {
    'x': pcaT[0],
    'y': pcaT[1],
    'c': 
}

fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
ax.scatter([x[0] for x in pca], [x[1] for x in pca]
            , c = 'b'
            , s = 50)
# ax.legend(targets)
ax.grid()