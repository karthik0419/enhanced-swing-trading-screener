"""
Weekly Cup & Handle Screener
Finds stocks with large multi-month weekly C&H setups — the kind
that give 2x moves as shown in swing trading analysis posts.

Usage:
  python weekly_screener.py
  python weekly_screener.py --stocks stocks.txt
  python weekly_screener.py --symbols RELIANCE.NS TCS.NS NHPC.NS
"""

import sys
import os
import argparse
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.loader import _fetch_nse, _resample_weekly
from patterns.cup_handle import detect_cup_handle_weekly
from utils.target_calculator import calculate_advanced_targets


def _score_weekly_setup(result):
    cmp       = result["cmp"]
    target    = result["target"]
    stop_loss = result["stop_loss"]

    upside = (target - cmp) / cmp * 100
    risk   = (cmp - stop_loss) / cmp * 100
    rr     = upside / risk if risk > 0 else 0

    score = 0
    if rr >= 3.0:   score += 40
    elif rr >= 2.0: score += 30
    elif rr >= 1.5: score += 20

    if result.get("volume"):           score += 15
    if result["status"] == "BREAKOUT": score += 25
    elif result["status"] == "NEAR":   score += 15

    depth = result.get("cup_depth_pct", 0)
    if 20 <= depth <= 45:  score += 20  # ideal cup depth
    elif depth > 45:       score += 10  # deeper = riskier but more upside

    return score, round(rr, 2), round(upside, 2), round(risk, 2)


def scan_weekly(symbol):
    # Fetch 2 years daily, resample to weekly
    df_daily = _fetch_nse(symbol, days=730)
    if df_daily is None or len(df_daily) < 60:
        return None

    df_weekly = _resample_weekly(df_daily)
    if df_weekly is None or len(df_weekly) < 40:
        return None

    result = detect_cup_handle_weekly(df_weekly)
    if not result:
        return None

    score, rr, upside, risk = _score_weekly_setup(result)
    if score < 20:
        return None

    # Multi-level targets using daily data for precision
    try:
        adv = calculate_advanced_targets(df_daily, "Cup & Handle", result)
        t1 = adv["targets"][0] if len(adv["targets"]) > 0 else result["target"]
        t2 = adv["targets"][1] if len(adv["targets"]) > 1 else result["target"]
        t3 = adv["targets"][2] if len(adv["targets"]) > 2 else result["target"]
    except Exception:
        t1 = t2 = t3 = result["target"]

    cmp = result["cmp"]

    return {
        "symbol":        symbol,
        "pattern":       result["pattern"],
        "cmp":           round(cmp, 2),
        "breakout":      round(result["breakout"], 2),
        "stop_loss":     round(result["stop_loss"], 2),
        "target_1":      round(t1, 2),
        "target_2":      round(t2, 2),
        "target_3":      round(t3, 2),
        "upside_%":      upside,
        "risk_%":        risk,
        "rr":            rr,
        "cup_depth_%":   result.get("cup_depth_pct", 0),
        "volume_ok":     result.get("volume", False),
        "status":        result["status"],
        "score":         score,
    }


def load_stocks(filepath):
    try:
        with open(filepath) as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("#")]
    except FileNotFoundError:
        return []


def main():
    parser = argparse.ArgumentParser(description="Weekly Cup & Handle screener")
    parser.add_argument("--stocks",  default="stocks.txt")
    parser.add_argument("--symbols", nargs="+")
    parser.add_argument("--output",  default="weekly_results.csv")
    args = parser.parse_args()

    symbols = args.symbols if args.symbols else load_stocks(args.stocks)
    if not symbols:
        print("No symbols. Use --symbols or stocks.txt")
        sys.exit(1)

    print(f"\nWeekly Cup & Handle scan — {len(symbols)} stocks\n")

    results = []
    for sym in symbols:
        print(f"  Scanning {sym}...", end=" ", flush=True)
        res = scan_weekly(sym)
        if res:
            results.append(res)
            print(f"SETUP FOUND | Score={res['score']} | RR={res['rr']} | Upside={res['upside_%']}%")
        else:
            print("no setup")

    if not results:
        print("\nNo weekly Cup & Handle setups found.")
        return

    df = pd.DataFrame(results).sort_values("score", ascending=False)
    df.to_csv(args.output, index=False)

    print(f"\n{'='*70}")
    print(f"WEEKLY CUP & HANDLE SETUPS  ({len(df)} found)")
    print(f"{'='*70}")
    print(df.to_string(index=False))
    print(f"\nSaved to: {args.output}")


if __name__ == "__main__":
    main()
