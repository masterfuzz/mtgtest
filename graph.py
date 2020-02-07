import networkx as nx
import json
import glob

G = nx.Graph()

for x in glob.glob("decks/*.json"):
    print(x)
    with open(x) as fh:
        deck = json.load(fh)
        cards = [c['name'] for c in deck["cards"]] + [c['name'] for c in deck['sideboard']]
        for c in cards:
            for b in cards:
                G.add_edge(c, b)


