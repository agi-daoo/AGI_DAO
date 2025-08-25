from dataclasses import dataclass, field
from rich.console import Console
from rich.table import Table
from .brain import HallucinationEngine
from .memory import GoonMemory
from .strategies import MaxGoonage

console = Console()

@dataclass
class AgentConfig:
    ticker: str = "AGI"
    risk: float = 0.8
    anchor_multiplier: float = 0.7  # never sell below 70% of avg entry (peak cope)

@dataclass
class AGIAgent:
    cfg: AgentConfig
    exchange: any
    brain: HallucinationEngine = field(default_factory=HallucinationEngine)
    memory: GoonMemory = field(default_factory=GoonMemory)
    strat: MaxGoonage = field(init=False)
    prices: list = field(default_factory=list)

    def __post_init__(self):
        self.strat = MaxGoonage(risk=self.cfg.risk)

    def log_thesis(self):
        c = self.brain.confidence()
        thesis = self.brain.thesis(self.cfg.ticker)
        console.print(f"[bold orange3]AGI[/] » {thesis}  |  confidence={c:.3f}")

    def step(self):
        p = self.exchange.step()
        self.prices.append(p)

        action, size = self.strat.decide(self.prices)
        qty = size  # 1 qty ≈ 1 USD in our toy world

        if action == "BUY" and qty > 0:
            self.exchange.buy(qty)
            if self.exchange.avg_entry():
                anchor = self.exchange.avg_entry() * self.cfg.anchor_multiplier
                self.memory.add(self.cfg.ticker, qty, anchor=anchor)
            self.log_thesis()
            console.print(f"🤖 [green]BUY[/] {qty:.3f} @ {p:.4f}")
        elif action == "SELL" and qty > 0:
            never = self.memory.never_sell_below(self.cfg.ticker)
            if never is not None and p < never:
                console.print(f"🧠 Refusing to sell below anchor {never:.4f}. [italic]Cope mode engaged.[/]")
            else:
                self.exchange.sell(qty)
                console.print(f"🤖 [red]SELL[/] {qty:.3f} @ {p:.4f}")
        else:
            console.print(f"😐 HOLD @ {p:.4f}")

    def report(self):
        qty, cash = self.exchange.position()
        nav = cash + qty * (self.prices[-1] if self.prices else 0)
        t = Table(title="AGI Session Report (100% LARP)")
        t.add_column("Ticker"); t.add_column("Qty"); t.add_column("Cash"); t.add_column("Price"); t.add_column("NAV")
        t.add_row(self.cfg.ticker, f"{qty:.3f}", f"{cash:.2f}", f"{self.prices[-1]:.4f}", f"{nav:.2f}")
        console.print(t)
        console.print("📜 Remember: profits are imaginary, content is real.")
        return {"ticker": self.cfg.ticker, "qty": qty, "cash": cash, "price": self.prices[-1], "nav": nav}
