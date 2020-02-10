import spotlight.interactions
import spotlight.factorization.implicit
import json
import glob
import numpy as np

class CardList:
    def __init__(self):
        self.max_id = 0
        self.cd = {}
    
    def get(self, name):
        if name not in self.cd:
            self.max_id += 1
            self.cd[name] = self.max_id
        return self.cd[name]

card_ids = CardList()
deck_seq = []
card_seq = []

deck_id = 0
for x in glob.glob("decks/*.json"):
    print(x)
    with open(x) as fh:
        deck = json.load(fh)
        cards = [c['name'] for c in deck["cards"]] + [c['name'] for c in deck['sideboard']]
        deck_id += 1

        deck_seq += [deck_id] * len(cards)
        card_seq += [card_ids.get(c) for c in cards]


interactions = spotlight.interactions.Interactions(
    np.array(deck_seq, np.int32),
    np.array(card_seq, np.int32)
)

model = spotlight.factorization.implicit.ImplicitFactorizationModel()
# model.fit(interactions)
