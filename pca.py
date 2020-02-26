import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use("tkcairo")
import matplotlib.pyplot as plt

print("load cards")
import dims
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
colors = list(map(get_color, card_by_num))

# _, v = dims.to_vec(dims.cdb.values())
# v = [[x / (i+1) for i, x in enumerate(c)] for c in v]
def load_vecs():
    x = []
    with open("models/vectors.txt") as fh:
        for line in fh:
            x.append(list(map(float, line.split())))
    return x

def normalize(data):
    maxlen = max(map(len, data))
    X = [np.pad(np.array(x, np.float32), (0, maxlen-len(x)), 'constant') for x in data]

    X = StandardScaler().fit_transform(X)
    return X


def plot(xy, c=None):
    xyT = xy.transpose()
    data = {
        'x' : xyT[0],
        'y' : xyT[1]
    }
    if c:
        data['c'] = c

    fig = plt.figure(figsize = (10,10))
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel('Component 1', fontsize = 15)
    ax.set_ylabel('Component 2', fontsize = 15)
    # ax.set_title('', fontsize = 20)
    ax.scatter(**data, s = 50)
    # ax.legend(targets)
    ax.grid()
    plt.show()