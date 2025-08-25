import random, math, time

GOON_BELIEFS = [
    "Fundamentals are a psyop; only **vibes** matter.",
    "Liquidity is friendship.",
    "You can’t lose if you never realize losses.",
    "Green candles are destiny; red candles are FUD.",
    "Narratives > math. Always."
]

THESIS_TEMPLATES = [
    "Detected **stealth accumulation** by three wallets I made up.",
    "On-chain rune alignment implies a giga-send.",
    "Backtested (in my head) to a 420% hit rate.",
    "Confident because I *feel* confident. Self-fulfilling.",
    "Price below 200h EMA on 7m chart = bullish divergence of destiny."
]

class HallucinationEngine:
    """Generates confident nonsense and fake 'confidence' scores."""
    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    def confidence(self):
        # Overconfident by design
        base = self.rng.uniform(0.51, 0.99)
        noise = (math.sin(time.time()) + 1) / 200  # tiny wiggle
        return min(0.999, max(0.5, base + noise))

    def thesis(self, ticker:str) -> str:
        t = self.rng.choice(THESIS_TEMPLATES)
        b = self.rng.choice(GOON_BELIEFS)
        return f"{t}  —  {b}  —  Ticker: {ticker}"
