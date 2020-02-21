import mtg 
import networkx as nx
import progressbar
import numpy as np

cdb = mtg.CardDB()

def dims(texts):
    bag = [{}] 
    m = 0
    for t in texts:
        for i, w in enumerate(t.split()):
            if i > m:
                bag.append({w: 1})
                m = i
            else:
                bag[i][w] = bag[i].get(w, 0) + 1
    return bag


def pre(tree, sentence):
    if not sentence:
        return tree
    root, tail = sentence[0], sentence[1:]
    tree[root] = pre(tree.get(root, {}), tail)
    return tree

def ctree(sentences):
    tree = {}
    for sentence in sentences:
        tree = pre(tree, sentence)
    return tree

def to_vec(cards):
    dims = []
    res = []
    for c in cards:
        vec = []
        for i, w in enumerate(c.sanitized_text().split()):
            if i == len(dims):
                dims.append({'self': 0})
            if w not in dims[i]:
                dims[i][w] = max(dims[i].values()) + 1
            vec.append(dims[i][w])
        res.append(vec)
    return dims, res


