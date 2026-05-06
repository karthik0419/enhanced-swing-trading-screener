# 🎯 Advanced Swing Trading Screener

## 📋 Overview

A sophisticated swing trading scanner for Indian stocks (NSE) that identifies high-probability trading setups using advanced pattern recognition, market analysis, and comprehensive verification systems.

## 🚀 Key Features

### 📊 Pattern Detection
- **Advanced Chart Patterns**: Cup & Handle, Double Top/Bottom, Darvas Box, Flags/Pennants
- **Basic Patterns**: Breakout, Retest, Compression
- **Multi-Timeframe Analysis**: Daily, Weekly, 4-Hour data
- **Precision Parameters**: Fine-tuned for accuracy (2% tolerance levels)

### 🔍 Pattern Validation
- **Volume Analysis**: Spike detection, accumulation patterns, divergence analysis
- **Price Action**: Structure validation, support/resistance quality
- **Trend Context**: Moving average alignment, momentum confirmation
- **Quality Scoring**: 0-100 scale with detailed breakdown

### 🎯 Target & Risk Management
- **Multi-Level Targets**: Conservative, Moderate, Aggressive profit levels
- **ATR-Based Stops**: Volatility-adjusted stop losses
- **Pattern-Specific Targets**: Different calculations per pattern type
- **Risk/Reward Analysis**: Comprehensive RR ratio calculations

### 📈 Market Intelligence
- **Sector Analysis**: Categorizes stocks by sector and performance
- **Market Conditions**: Nifty trend, volatility, favorability analysis
- **Market Filtering**: Removes setups during unfavorable conditions
- **Sector Momentum**: Identifies hot/weak sectors

### 📚 Performance Tracking
- **Historical Database**: Tracks all trade outcomes by pattern
- **Success Rate Analysis**: Win/loss ratios by pattern type
- **Performance Metrics**: Average profit/loss, max gains/losses
- **Learning System**: Improves recommendations based on history

### ✅ Verification Tools
- **Comprehensive Checklist**: 4 categories with 16 verification points
- **Technical Analysis**: Trend strength, volume, momentum, volatility
- **Risk Factor ID**: Identifies specific risks for each setup
- **Confidence Scoring**: Overall setup quality assessment

### 🎪 Entry Confirmation
- **Multi-Indicator System**: Price action, volume, momentum, timeframe
- **Signal Strength**: Graded confirmation levels
- **Entry Recommendations**: ENTER NOW, WAIT, AVOID guidance
- **Timing Analysis**: Optimal entry time detection

## 🛠️ Installation & Setup

### Prerequisites
```bash
# Python 3.8+ required
pip install pandas numpy yfinance
```

### Quick Start
```bash
# 1. Clone repository
git clone <repository-url>
cd swing_screener

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add stocks to watchlist
# Edit stocks.txt with your stock symbols
RELIANCE.NS
TCS.NS
HDFCBANK.NS
```

### Running the Scanner
```bash
# Basic scan
python main.py

# Results saved to
output/results.csv
```

## 📁 Project Structure

```
swing_screener/
├── main.py                 # Main entry point
├── stocks.txt              # Stock watchlist
├── output/
│   └── results.csv        # Scan results
├── data/
│   └── performance_data.json  # Historical performance
├── engine/
│   └── scanner.py        # Core scanning logic
├── patterns/
│   ├── breakout.py       # Breakout patterns
│   ├── retest.py        # Retest patterns
│   ├── compression.py   # Compression patterns
│   ├── cup_handle.py    # Cup & Handle patterns
│   ├── double_top_bottom.py  # Double patterns
│   ├── darvas_box.py   # Darvas Box patterns
│   └── flags.py         # Flag/Pennant patterns
├── utils/
│   ├── pattern_validator.py    # Pattern validation
│   ├── target_calculator.py    # Target calculations
│   ├── sector_analyzer.py      # Sector analysis
│   ├── performance_tracker.py   # Performance tracking
│   ├── verification_tools.py   # Verification checklists
│   ├── entry_confirmation.py   # Entry confirmation
│   └── entry_4h.py          # 4H entry logic
├── scoring/
│   └── scorer.py         # Setup scoring
├── config/
│   └── settings.py        # Configuration settings
└── data/
    └── loader.py          # Data fetching
```

## 📊 Understanding Results

### Output Columns
| Column | Description |
|---------|-------------|
| `symbol` | Stock symbol |
| `pattern` | Detected pattern type |
| `sector` | Stock sector |
| `pattern_success_rate` | Historical win rate |
| `verification_score` | Quality verification score |
| `entry_confirmation_score` | Entry signal strength |
| `cmp` | Current market price |
| `breakout` | Breakout/resistance level |
| `stop_loss` | Recommended stop loss |
| `target` | Primary profit target |
| `rr` | Risk/Reward ratio |
| `score` | Overall setup score |
| `status` | Current pattern status |

### Status Meanings
- **BREAKOUT**: Price has broken resistance
- **RETEST**: Price is retesting breakout level
- **NEAR**: Price is near breakout level
- **PRE_BREAKOUT**: About to break out

### Score Interpretation
- **100+**: Excellent setup, high confidence
- **80-99**: Very good setup
- **60-79**: Good setup, moderate confidence
- **40-59**: Average setup, low confidence
- **<40**: Poor setup, avoid

## 🎯 Pattern Types

### High-Probability Patterns
1. **Cup & Handle**: Bullish continuation, 65%+ success rate
2. **Double Bottom**: Strong reversal, 60%+ success rate
3. **Darvas Box**: Consolidation breakout, 55%+ success rate

### Continuation Patterns
4. **Bullish Flag**: Trend continuation, 50%+ success rate
5. **Bullish Pennant**: Short-term continuation, 45%+ success rate

### Reversal Patterns
6. **Double Top**: Bearish reversal, 55%+ success rate
7. **Bearish Flag**: Downtrend continuation, 45%+ success rate

### Basic Patterns
8. **Breakout Retest**: Classic breakout setup
9. **Higher-Low Compression**: Accumulation pattern
10. **Resistance Breakout**: Simple breakout

## 🔧 Configuration

### Key Settings (config/settings.py)
```python
# Data Settings
MIN_CANDLES = 60              # Minimum data points
LOOKBACK_PERIOD = 50            # Resistance/Support lookback
VOLUME_LOOKBACK = 20            # Volume average period

# Pattern Settings
VOLUME_MULTIPLIER = 1.5         # Volume spike threshold
NEAR_BREAKOUT_THRESHOLD = 0.03  # Near breakout distance
RESISTANCE_THRESHOLD = 0.97       # Resistance proximity

# Risk Management
RR_HIGH = 2.0                   # High RR threshold
RR_MEDIUM = 1.5                 # Medium RR threshold
STOP_LOSS_BUFFER = 0.02          # Stop loss buffer
```

## 📈 Performance Tracking

### Recording Trades
```python
from utils.performance_tracker import record_trade

# Record a completed trade
record_trade({
    'symbol': 'TITAN.NS',
    'pattern': 'Double Bottom',
    'entry_price': 4059.00,
    'exit_price': 4200.00,
    'target': 4176.00,
    'stop_loss': 3748.50,
    'profit_loss_pct': 3.5,
    'is_win': True,
    'days_held': 5,
    'rr_ratio': 1.8
})
```

### Performance Reports
```python
from utils.performance_tracker import get_performance_report

# Generate comprehensive report
report = get_performance_report()
print(f"Overall Win Rate: {report['summary']['overall_win_rate']:.1f}%")
print(f"Best Pattern: {report['best_patterns'][0]['pattern']}")
```

## 🔍 Verification Process

### Manual Verification Checklist
1. **Pattern Quality** (40 points)
   - Structure clearly visible? (15 pts)
   - Proportions correct? (12 pts)
   - Volume confirmation? (10 pts)
   - Support/resistance defined? (13 pts)

2. **Market Context** (37 points)
   - Sector trend aligned? (12 pts)
   - Market conditions favorable? (10 pts)
   - No major news impact? (8 pts)
   - Index correlation positive? (7 pts)

3. **Risk Management** (45 points)
   - Stop loss logical? (15 pts)
   - RR ratio acceptable? (12 pts)
   - Position size appropriate? (10 pts)
   - Max risk < 2%? (8 pts)

4. **Technical Confirmation** (31 points)
   - Moving averages aligned? (10 pts)
   - Momentum positive? (8 pts)
   - Volatility normal? (6 pts)
   - No conflicting patterns? (7 pts)

### Confidence Levels
- **85-100**: Very High - ENTER NOW
- **75-84**: High - ENTER with caution
- **65-74**: Moderate - CONSIDER
- **55-64**: Low - WAIT for better signal
- **<55**: Very Low - AVOID

## 🎪 Entry Confirmation

### Multi-Indicator System
1. **Price Action** (78 points max)
   - Candlestick patterns (20 pts)
   - Breakout confirmation (25 pts)
   - Pullback entry (15 pts)
   - Consolidation break (18 pts)

2. **Volume Confirmation** (45 points max)
   - Volume spike (20 pts)
   - Volume accumulation (15 pts)
   - Volume divergence (10 pts)

3. **Momentum Confirmation** (55 points max)
   - RSI confirmation (15 pts)
   - MACD signal (18 pts)
   - MA crossover (12 pts)
   - Price momentum (10 pts)

4. **Multi-Timeframe** (35 points max)
   - 4H alignment (15 pts)
   - Weekly alignment (12 pts)
   - Time of day (8 pts)

## 📚 Trading Strategy Guide

### Best Practices
1. **Market Conditions**: Trade with trend, avoid high volatility
2. **Sector Selection**: Focus on top-performing sectors
3. **Pattern Priority**: Prefer high-success patterns first
4. **Risk Management**: Always use 2% max risk rule
5. **Entry Timing**: Wait for confirmation signals
6. **Position Sizing**: Scale based on confidence level

### Daily Routine
1. **Pre-Market**: Check market conditions and sector performance
2. **Scan Setup**: Run scanner for current opportunities
3. **Verify Setup**: Use checklist for top 3-5 setups
4. **Confirm Entry**: Check multi-indicator confirmation
5. **Execute Trade**: Enter with proper position sizing
6. **Record Results**: Track outcome for learning

## 🚨 Risk Warnings

### High-Risk Situations
- Market volatility > 2%
- Sector performance < -5%
- Pattern verification < 50%
- Entry confirmation < 60%
- RR ratio < 1:1

### Avoid Trading When
- Major news events expected
- Market in strong downtrend
- High volatility periods
- Multiple conflicting signals
- Insufficient volume

## 📞 Troubleshooting

### Common Issues
1. **No Setups Found**
   - Check market conditions
   - Verify stock symbols
   - Review pattern parameters

2. **Low Verification Scores**
   - Examine pattern quality
   - Check volume confirmation
   - Review market context

3. **Entry Confirmation Issues**
   - Verify multi-timeframe data
   - Check indicator calculations
   - Review signal thresholds

### Performance Issues
1. **Low Win Rates**
   - Tighten entry criteria
   - Improve pattern selection
   - Better risk management

2. **High Losses**
   - Review stop loss placement
   - Check position sizing
   - Analyze holding periods

## 🔄 Updates & Improvements

### Version History
- **v1.0**: Basic pattern detection
- **v2.0**: Advanced patterns + validation
- **v3.0**: Market analysis + tracking
- **v4.0**: Verification + confirmation systems

### Future Enhancements
- Real-time alerts
- Mobile app interface
- Backtesting module
- Portfolio integration
- AI-based predictions

## 📞 Support

### Getting Help
1. **Documentation**: Check this README first
2. **Code Comments**: Review inline documentation
3. **Error Messages**: Read specific error details
4. **Performance Data**: Analyze historical results

### Contributing
1. Fork the repository
2. Create feature branch
3. Make improvements
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- **yfinance**: For market data
- **pandas**: For data analysis
- **numpy**: For numerical computations
- **TradingView**: For pattern inspiration

---

**Disclaimer**: This tool is for educational purposes only. Trading involves substantial risk of loss. Use at your own risk and never trade with money you can't afford to lose.

## 🎯 Quick Start Summary

```bash
# 1. Setup environment
python -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install pandas numpy yfinance

# 3. Add stocks to watchlist
echo "RELIANCE.NS" > stocks.txt
echo "TCS.NS" >> stocks.txt

# 4. Run scanner
python main.py

# 5. Review results
cat output/results.csv
```

**Happy Trading! 🚀**
