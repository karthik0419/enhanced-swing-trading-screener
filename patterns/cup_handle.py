def detect_cup_handle(df):
    if df is None or len(df) < 100:
        return None
    
    # Look for cup formation (last 60-90 days)
    cup_period = min(60, len(df) - 20)
    cup_data = df.tail(cup_period)
    
    # Find cup low and high
    cup_low = cup_data['Low'].min()
    cup_high = cup_data['High'].max()
    cup_low_idx = cup_data['Low'].idxmin()
    
    # Cup depth should be reasonable (20-40% for better patterns)
    cup_depth = (cup_high - cup_low) / cup_high
    if cup_depth < 0.20 or cup_depth > 0.40:
        return None
    
    # Handle formation (last 10-20 days)
    handle_period = min(20, len(df) - cup_period)
    handle_data = df.tail(handle_period)
    
    current_price = float(df['Close'].iloc[-1])
    handle_high = handle_data['High'].max()
    handle_low = handle_data['Low'].min()
    
    # Handle should be in upper third of cup
    handle_position = (handle_low - cup_low) / (cup_high - cup_low)
    if handle_position < 0.6:
        return None
    
    # Handle should be smaller than cup depth
    handle_depth = (handle_high - handle_low) / cup_high
    if handle_depth > cup_depth * 0.5:
        return None
    
    # Current price should be near handle high (breaking out)
    breakout_level = handle_high
    near_breakout = current_price >= breakout_level * 0.98
    
    # Volume check
    avg_volume = float(df['Volume'].tail(20).mean())
    current_volume = float(df['Volume'].iloc[-1])
    volume_ok = current_volume > avg_volume * 1.2
    
    if near_breakout:
        # Calculate targets and stops
        target = cup_high + (cup_high - cup_low) * 0.5  # 50% of cup depth
        stop_loss = handle_low * 0.98
        
        return {
            "pattern": "Cup & Handle",
            "cmp": current_price,
            "breakout": breakout_level,
            "stop_loss": stop_loss,
            "target": target,
            "volume": volume_ok,
            "status": "BREAKOUT" if current_price > breakout_level else "NEAR"
        }
    
    return None
