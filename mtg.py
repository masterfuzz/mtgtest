import random
import re
import orjson as json
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

class Deck:
    def __init__(self, j):
        self.side = j.get('sideboard', [])
        self.main = j.get('cards', [])
        self.player = j.get('player', '')
        self.result = j.get('result', '')

    def names(self):
        return set(c['name'] for c in self.main + self.side)

class Card:
    KEYWORDS = set()
    def __init__(self, j):
        self.name = j['name']
        self.text = j.get('text', "").replace(self.name, "SELF")
        self.colors = j.get('colors', [])
        self.types = j.get('types', [])
        self.subtypes = j.get('subtypes', [])
        self.manaCost = j.get('manaCost', "")
        self.power = j.get('power')
        self.toughness = j.get('toughness')
        self.printings = j['printings']
        self.keywords = [k for k in self.text.split() if k in self.KEYWORDS]

    def to_text(self, with_name=False):
        r = ""
        if with_name:
            r += self.name + " "
        r += " ".join([self.manaCost, " ".join(self.types), " ".join(self.subtypes), self.text])
        if self.power:
            r += f" {self.power} / {self.toughness}"
        return r

    def sanitized_text(self):
        _remove_help_text = re.sub(r"\([^)]*\)", "", self.text)
        _lower = _remove_help_text.lower()
        _punc = re.sub(r"[\n,.]", " ", _lower)
        _cost = _punc.replace(":", " COST ")
        _mana = _cost.replace("}{", "} {")
        _self = _mana.replace(self.name.lower(), 'SELF')
        
        return _self

    def __str__(self):
        return self.to_text(with_name=True)

    def tokens(self):
        yield from self.colors
        yield from self.types
        yield from self.subtypes
        yield "MC_" + str(self.manaCost)
        yield "POWER_" + str(self.power)
        yield "TOUGH_" + str(self.toughness)
        # if self.text:
        #     yield from self.text.replace(self.name, "SELF").split()
        yield from self.keywords

class CardDB:
    def __init__(self, db_file="cards/AllCards.json", keyword_file="cards/Keywords.json"):
        with open(keyword_file) as fh:
            keyword_json = json.loads(fh.read())
            Card.KEYWORDS.update(keyword_json['abilityWords'] + keyword_json['keywordAbilities'] + keyword_json['keywordActions'])

        with open(db_file) as fh:
            card_json = json.loads(fh.read())

        self.cards = {name: Card(cj) for name, cj in card_json.items()}

    def values(self):
        return self.cards.values()

    def items(self):
        return self.cards.items()

    def dump_text(self, path):
        with open(path, "w") as fh:
            for card in self.values():
                fh.write(card.sanitized_text())
                fh.write("\n")

    def __getitem__(self, index):
        return self.cards[index]

class DeckDB:
    def __init__(self, glob_path="decks/*.json"):
        import glob

        self.decks = list(self._load(glob.glob(glob_path)))

    def _load(self, file_names):
        for deck_file in file_names:
            with open(deck_file) as fh:
                yield Deck(json.loads(fh.read()))

    def card_graph(self):
        G = nx.Graph()
        for deck in self.decks:
            for card_a in deck.names():
                for card_b in deck.names():
                    if card_a == card_b: continue
                    G.add_edge(card_a, card_b)
        return G


def get_graph(cards):
    G = nx.Graph()
    token_set = {}
    for card in progressbar.progressbar(cards.values()):
        for token in card.tokens():
            s = token_set.get(token, set())
            s.add(card.name)
            token_set[token] = s

    for card in progressbar.progressbar(cards.values()):
        for token in card.tokens():
            for card2 in token_set[token]:
                G.add_edge(card.name, card2)

    return G

def get_model(graph):
    n2v = node2vec.Node2Vec(graph, workers=8)
    model = n2v.fit()
    return n2v, model

def cards_to_text():
    cdb = CardDB()
    with open("allcards.txt", "w") as fh:
        for card in progressbar.progressbar(cdb.values()):
            txt = card.to_text().lower().replace('\n', ' ').replace(',', '').replace('}{', '} {').replace('.', ' ').replace(':', ' : ')
            fh.write(txt + "\n")
    print("done")



