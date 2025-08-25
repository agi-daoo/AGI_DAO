from collections import defaultdict

class GoonMemory:
    """Refuses to forget bags that are down horrifically."""
    def __init__(self):
        self.bags = defaultdict(float)   # ticker -> qty
        self.anchors = {}                # ticker -> 'never sell' threshold

    def add(self, ticker:str, qty:float, anchor=None):
        self.bags[ticker] += qty
        if anchor is not None:
            self.anchors[ticker] = anchor

    def never_sell_below(self, ticker:str):
        return self.anchors.get(ticker, None)
