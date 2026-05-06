# Enhanced Swing Trading Screener — NSE India

A swing trading screener for Indian stocks (NSE) with Cup & Handle detection, momentum scoring, dynamic universe building, and walk-forward backtesting.

---

## Changelog

### v5.0 — 2026-05-07 (Current)
**What changed in this push:**

- **Switched data source from yfinance to jugaad-data (NSE native)**
  - yfinance had inconsistent data for Indian stocks; jugaad-data pulls directly from NSE
  - Monkey-patched Windows `os.makedirs` bug in jugaad-data
  - Strips `.NS` / `.BO` suffix automatically before API call

- **Added parallel fetching + 8-hour disk cache (`data/fetcher.py`)**
  - Previously: sequential fetch, 15-20 minutes for 200 stocks
  - Now: 10-15 parallel workers, under 30 seconds on cached runs
  - Cache stored in `cache/` folder, expires after 8 hours

- **Rewrote Cup & Handle detection (`patterns/cup_handle.py`)**
  - Added proper U-shape validator: cup low must be in middle 60% of the cup (not at edges)
  - Added weekly timeframe variant (`detect_cup_handle_weekly`) for longer setups
  - Tuned parameters: 60-bar cup, 15-bar handle, 15% near-high threshold for weekly
  - Fixed breakout level: uses left rim resistance, not 52-week high

- **New main screener (`may_screener.py`)**
  - Scoring system (0-100): Pattern quality + RSI zone + Relative Strength + 52w proximity + Volume surge + MA alignment
  - Pattern priority: Weekly C&H > Daily C&H > Darvas Box > Flag/Pennant > Breakout
  - No Pattern stocks: breakout = 20-day high (realistic near-term resistance, not 52w high)
  - Skips stocks where breakout > 20% above CMP (unreachable in swing timeframe)
  - Skips trades with RR < 1.0

- **New dynamic universe builder (`stock_universe.py`)**
  - Scores all 233 nifty500 stocks daily by: 52w high proximity + above MA50/MA20 + volume surge
  - Picks top 80 momentum stocks, merges with backbone50 (always included)
  - Saves to `today_universe.txt` for the screener to consume

- **New stock lists**
  - `backbone50.txt` — 48 curated stocks: precision engineering, data center, power, cooling, networking
  - `nifty500.txt` — 233-stock full universe across all sectors

- **New backtester (`backtester/`)**
  - Walk-forward engine: slices data day-by-day, no lookahead bias
  - Entry at next bar open after signal
  - Exits on stop loss / target / 20-day time stop
  - P&L report by pattern and by exit reason

- **One-click runner (`run_screener.bat`)**
  - Step 1: builds today_universe.txt
  - Step 2: runs screener on that universe
  - Manual only — no scheduled tasks

---

### v4.0 — Original (pre-May 2026)
**What the original repo had:**

- yfinance as data source
- Basic Cup & Handle, Double Bottom, Darvas Box, Flag/Pennant detection
- Sequential data fetching (slow — 15-20 min for full scan)
- Generic scoring system
- No backtester
- No dynamic universe builder
- No stock lists (user had to provide symbols manually)
- `main.py` as entry point

---

## How to Run

Double-click `run_screener.bat`. That's it.

```
[1/2] stock_universe.py   → scores 233 stocks, picks top 80 + backbone50 → today_universe.txt
[2/2] may_screener.py     → scans today_universe.txt for setups → daily_results.csv
```

First run: ~2-3 minutes (fetching fresh NSE data)
Subsequent runs same day: ~30 seconds (cached)

---

## Installation

```bash
git clone https://github.com/karthik0419/enhanced-swing-trading-screener
cd enhanced-swing-trading-screener
pip install pandas numpy jugaad-data
```

---

## Project Structure

```
enhanced-swing-trading-screener/
├── run_screener.bat          # One-click manual runner
├── may_screener.py           # Main swing screener (scoring + patterns)
├── stock_universe.py         # Dynamic universe builder
├── backtest.py               # Backtester CLI entry point
├── backbone50.txt            # 48 curated stocks (always scanned)
├── nifty500.txt              # 233-stock full universe
│
├── data/
│   ├── loader.py             # NSE data fetcher via jugaad-data
│   └── fetcher.py            # Parallel fetch + 8-hour disk cache
│
├── patterns/
│   ├── cup_handle.py         # Cup & Handle (daily + weekly)
│   ├── breakout.py           # Resistance breakout
│   ├── darvas_box.py         # Darvas Box
│   └── flags.py              # Flag / Pennant
│
├── backtester/
│   ├── engine.py             # Walk-forward backtest engine
│   └── report.py             # P&L stats and pattern breakdown
│
├── engine/
│   └── scanner.py            # Core scan loop
│
└── cache/                    # Auto-generated, gitignored
```

---

## Scoring System (0-100)

| Factor | Max Points | Criteria |
|--------|-----------|---------|
| Pattern quality | 40 | Weekly C&H=40, Daily C&H=35, Darvas=28, Flag=25, Breakout=20 |
| RSI zone | 20 | 45-65 = healthy (20 pts), 35-45 = recovering (12 pts) |
| Relative strength vs Nifty | 15 | RS +5% = 15 pts, RS +2% = 10 pts |
| Near 52-week high | 15 | Within 5% = 15 pts, within 10% = 10 pts |
| Volume surge | 10 | 1.5x avg = 10 pts, 1.2x avg = 5 pts |
| MA alignment | 10 | Above MA20 > MA50 = 10 pts |
| Risk/Reward bonus | 10 | RR >= 2.5 = 10 pts, RR >= 1.5 = 5 pts |

Minimum score to appear in results: 30 (configurable via `--min-score`)

---

## Cup & Handle Detection

**Daily timeframe:**
- Cup: 40-80 bars, depth 10-40%, U-shaped (low in middle 60%)
- Handle: 10-20 bars, retraces max 40% of cup depth
- Breakout: within 8% of left rim high

**Weekly timeframe (higher priority):**
- Cup: 50-80 bars, depth 15-50%
- Handle: 8-15 bars
- Breakout: within 15% of left rim high

---

## Output Columns

| Column | Description |
|--------|-------------|
| symbol | NSE stock symbol |
| pattern | Detected pattern |
| cmp | Current market price |
| breakout | Key resistance level to watch |
| stop_loss | ATR-based stop loss |
| target | Price target |
| upside_% | Potential upside to target |
| risk_% | Downside to stop loss |
| rr | Risk/Reward ratio |
| rsi | 14-period RSI |
| vol_ratio | Today's volume vs 20-day average |
| dist_52h_% | % below 52-week high |
| score | Overall setup score (0-100) |
| reasons | What drove the score |

---

## Backtesting

```bash
python backtest.py --stocks backbone50.txt --start 2024-01-01
```

Results broken down by pattern and exit reason (stop hit / target hit / time stop).

---

## Known Limitations

- `rs_vs_nifty` = 0.0 for all stocks — jugaad-data doesn't support index symbols (^NSEI), so relative strength vs Nifty benchmark is not calculated
- Some stocks fail to fetch (PRICOL, NIIT, MASTEK etc.) — NSE API returns different column format for certain stocks; screener skips them
- Data is end-of-day only — not suitable for intraday setups

---

## Disclaimer

For educational purposes only. Trading involves substantial risk. Never risk money you cannot afford to lose.
