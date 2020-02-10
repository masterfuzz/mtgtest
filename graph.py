import networkx as nx
import json
import glob
import progressbar

G = nx.Graph()
decks = []

print("loading decks")
for x in progressbar.progressbar(glob.glob("decks/*.json")):
    # print(x)
    with open(x) as fh:
        deck = json.load(fh)
        cards = [c['name'] for c in deck["cards"]] + [c['name'] for c in deck['sideboard']]
        decks.append(cards)
        for c in cards:
            for b in cards:
                G.add_edge(c, b)

from node2vec import Node2Vec

print("creating n2v")
n2v = Node2Vec(G, workers=8)

print("running model")
model = n2v.fit()

