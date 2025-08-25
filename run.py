import argparse, json, os, time
from .agent import AGIAgent, AgentConfig
from .exchange import PaperExchange

def main():
    ap = argparse.ArgumentParser(description="Artificial Gooning Intelligence (LARP)")
    ap.add_argument("--ticker", default="AGI")
    ap.add_argument("--minutes", type=int, default=30, help="Sim length (each step ≈ 1 minute)")
    ap.add_argument("--risk", type=float, default=0.8)
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()

    ex = PaperExchange(args.ticker, seed=args.seed)
    agent = AGIAgent(AgentConfig(ticker=args.ticker, risk=args.risk), exchange=ex)

    for _ in range(args.minutes):
        agent.step()
        time.sleep(0.02)  # fast sim; slow it if you want vibes

    rep = agent.report()
    os.makedirs("runs", exist_ok=True)
    out = f"runs/{int(time.time())}_{args.ticker}.json"
    with open(out, "w") as f:
        json.dump(rep, f, indent=2)
    print(f"Saved report -> {out}")

if __name__ == "__main__":
    main()
