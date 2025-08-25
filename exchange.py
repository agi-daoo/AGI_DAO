import random, statistics

class PaperExchange:
    """Toy exchange with a random-walk price."""
    def __init__(self, ticker:str, seed=None, start_price:float=1.0, drift=0.0005, vol=0.02):
        self.ticker = ticker
        self.rng = random.Random(seed)
        self.price = start_price
        self.drift = drift
        self.vol = vol
        self.ledger = []  # (type, qty, price)

    def step(self):
        shock = self.rng.gauss(self.drift, self.vol)
        self.price = max(0.0001, self.price * (1 + shock))
        return self.price

    def buy(self, qty:float):
        self.ledger.append(("BUY", qty, self.price))

    def sell(self, qty:float):
        self.ledger.append(("SELL", qty, self.price))

    def position(self):
        qty = 0.0
        cash = 0.0
        for typ, q, p in self.ledger:
            if typ == "BUY":
                qty += q; cash -= q * p
            else:
                qty -= q; cash += q * p
        return qty, cash

    def avg_entry(self):
        fills = [p for t, q, p in self.ledger if t == "BUY" for _ in range(int(q*100))]
        return statistics.mean(fills) if fills else None
