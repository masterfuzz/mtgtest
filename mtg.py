import random
import json
import networkx as nx
import progressbar

def rec(model, deck):
    # get vectors
    vecs = [
        model.get_vector(card)
        for card in deck
    ]
    # get center
    center = sum(vecs) / len(vecs)
    
    return model.similar_by_vector(center)

class Card:
    def __init__(self, j):
        self.name = j['name']
        self.text = j.get('text')
        self.colors = j.get('colors', [])
        self.types = j.get('types', [])
        self.subtypes = j.get('subtypes', [])
        self.manaCost = j.get('manaCost')
        self.power = j.get('power')
        self.toughness = j.get('toughness')

    def tokens(self):
        yield from self.colors
        yield from self.types
        yield from self.subtypes
        yield "MC_" + str(self.manaCost)
        yield "POWER_" + str(self.power)
        yield "TOUGH_" + str(self.toughness)
        if self.text:
            yield from self.text.replace(self.name, "SELF").split()


def get_cards():
    with open("cards/AllCards.json") as fh:
        card_json = json.load(fh)
    return {name: Card(cj) for name, cj in card_json.items()}

def get_graph(cards):
    G = nx.Graph()
    for card in progressbar.progressbar(cards.values()):
        for t in card.tokens():
            G.add_edge(card.name, t)
    return G

def get_model(graph):
    n2v = node2vec.Node2Vec(graph, workers=8)
    model = n2v.fit()
    return n2v, model
