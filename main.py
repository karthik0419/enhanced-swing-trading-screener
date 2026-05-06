# main.py
import pandas as pd
from engine.scanner import scan_stock
from utils.sector_analyzer import get_market_conditions, filter_by_market_conditions, get_sector_summary

def run():
    # Use current manual stocks.txt for user's custom stock list
    try:
        with open("stocks.txt") as f:
            stocks = [line.strip() for line in f if line.strip()]
        print(f"📋 Using {len(stocks)} stocks from your current list")
        print("✅ Ready for manual data input and testing")
    except Exception as e:
        print(f"❌ Error reading stocks.txt: {e}")
        return

    # Get market conditions first
    market_conditions = get_market_conditions()
    print(f"\n📊 Market Conditions:")
    print(f"   Nifty Change: {market_conditions['nifty_change']}%")
    print(f"   Trend: {market_conditions['trend']}")
    print(f"   Volatility: {market_conditions['volatility']}")
    print(f"   Status: {market_conditions['recommendation']}")
    print(f"\n🔍 Scanning stocks...\n")

    results = []

    for stock in stocks:
        print(f"Checking {stock}...")
        res = scan_stock(stock)
        if res:
            results.append(res)

    print(f"\nTotal setups found: {len(results)}")

    # Apply market condition filters
    filtered_results = filter_by_market_conditions(results, market_conditions)
    
    print(f"After market filtering: {len(filtered_results)} setups")

    # ✅ Handle no results
    if not filtered_results:
        print("\nNo valid setups found after market filtering.")
        return

    df = pd.DataFrame(filtered_results)

    # ✅ Safety: ensure score exists
    if "score" not in df.columns:
        print("\nNo scored results available.")
        return

    df = df.sort_values(by="score", ascending=False).head(15)

    # Enhanced column order with all verification info
    columns_order = [
        "symbol", "pattern", "sector", "sector_performance", "sector_rank",
        "pattern_success_rate", "pattern_trades_info",
        "verification_score", "verification_rating", "verification_factors",
        "entry_confirmation_score", "entry_confidence_level", "entry_signals_count",
        "cmp", "breakout", "stop_loss", "target",
        "upside_pct", "risk_pct", "rr",
        "score", "status",
        "entry_signal", "entry_confidence"
    ]
    
    # ✅ Safe column selection
    available_columns = [col for col in columns_order if col in df.columns]
    df = df.reindex(columns=available_columns)

    # Clean up and save results with proper formatting
    df_clean = df.copy()
    
    # Round numeric columns for cleaner output
    numeric_columns = ['cmp', 'breakout', 'stop_loss', 'target', 'upside_pct', 'risk_pct', 'rr', 'score', 'verification_score', 'entry_confirmation_score']
    for col in numeric_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].round(2)
    
    # Save with proper CSV formatting
    df_clean.to_csv("output/results.csv", index=False, float_format='%.2f')

    # Display sector summary
    sector_summary = get_sector_summary()
    print(f"\n📈 Top Performing Sectors:")
    for i, (sector, data) in enumerate(sector_summary['top_sectors'][:3], 1):
        print(f"   {i}. {sector}: {data['avg_performance']:.1f}% ({data['momentum']})")

    print(f"\n🎯 Top Setups:\n")
    print(df.to_string(index=False))
    
    

if __name__ == "__main__":
    run()