import random

class MaxGoonage:
    """
    'Strategy' that buys strength, sells fear, and ignores risk.
    Tunables:
      risk (0..1): higher means larger position sizes and more FOMO.
    """
    def __init__(self, risk:float=0.8, seed=None):
        self.rng = random.Random(seed)
        self.risk = max(0.0, min(1.0, risk))

    def decide(self, price_series:list[float]):
        if len(price_series) < 5:
            return "HOLD", 0.0

        # Simple momentum + coinflip goonification:
        mom = (price_series[-1] - price_series[-5]) / max(1e-9, price_series[-5])
        coin = self.rng.random()

        # If momentum up or coin says YOLO, buy; else panic sell a little.
        if mom > -0.01 and coin < 0.66 + 0.2*self.risk:
            size = (0.05 + 0.25*self.risk) * (1 + mom*2)
            return "BUY", max(0.0, size)
        elif coin < 0.90:
            size = 0.05 * (1 - mom)   # sell more when it looks bad
            return "SELL", max(0.0, size)
        return "HOLD", 0.0
