import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use("tkcairo")
import matplotlib.pyplot as plt

print("load cards")
import dims

# normalize
print("get vecs")
card_by_num = list(dims.cdb.values())
colormap = {
    'W': 'c',
    'U': 'b',
    'B': 'k',
    'R': 'r',
    'G': 'g'
}

def get_color(card):
    if len(card.colors) == 1:
        return colormap[card.colors[0]]
    elif len(card.colors) == 0:
        return 'y'
    else:
        return 'm'

_, v = dims.to_vec(dims.cdb.values())
v = [[x / (i+1) for i, x in enumerate(c)] for c in v]

print("normalize")
maxlen = max(map(len, v))
X = [np.pad(np.array(x, np.float32), (0, maxlen-len(x)), 'constant') for x in v]

X = StandardScaler().fit_transform(X)

print("compute pca")
pca = PCA(n_components=2).fit_transform(X)

print("plotting")
pcaT = pca.transpose()
data = {
    'x': pcaT[0],
    'y': pcaT[1],
    'c': list(map(get_color, card_by_num))
}

fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
ax.scatter(**data, s = 50)
# ax.legend(targets)
ax.grid()
plt.show()