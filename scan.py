import yfinance as yf
import json
from datetime import datetime

print("=" * 60)
print("📊 STOCK SCREENER - FULL ANALYSIS")
print("=" * 60)

# Stocks to scan
stocks = ['SPY', 'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'TSLA', 'AMZN', 'META']
results = []

for stock in stocks:
    try:
        print(f"\nAnalyzing {stock}...")
        ticker = yf.Ticker(stock)
        data = ticker.history(period='2d')
        info = ticker.info
        
        if not data.empty:
            # Current price
            current = data['Close'].iloc[-1]
            
            # Previous day close
            if len(data) > 1:
                prev_close = data['Close'].iloc[-2]
                change = current - prev_close
                change_percent = (change / prev_close) * 100
            else:
                change = 0
                change_percent = 0
            
            # Volume
            volume = data['Volume'].iloc[-1]
            
            # Day high/low
            day_high = data['High'].iloc[-1]
            day_low = data['Low'].iloc[-1]
            
            # Get additional metrics from info
            market_cap = info.get('marketCap', 'N/A')
            pe_ratio = info.get('trailingPE', 'N/A')
            fifty_two_week_high = info.get('fiftyTwoWeekHigh', 'N/A')
            fifty_two_week_low = info.get('fiftyTwoWeekLow', 'N/A')
            
            # Recommendation
            if change_percent > 2:
                signal = "🔥 STRONG BUY"
            elif change_percent > 0.5:
                signal = "📈 BUY"
            elif change_percent > -0.5:
                signal = "➡️ HOLD"
            elif change_percent > -2:
                signal = "📉 SELL"
            else:
                signal = "🔻 STRONG SELL"
            
            results.append({
                'symbol': stock,
                'price': round(current, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'volume': int(volume),
                'day_high': round(day_high, 2),
                'day_low': round(day_low, 2),
                'market_cap': market_cap,
                'pe_ratio': pe_ratio if pe_ratio == 'N/A' else round(pe_ratio, 2),
                '52_week_high': fifty_two_week_high,
                '52_week_low': fifty_two_week_low,
                'signal': signal,
                'timestamp': str(datetime.now())
            })
            
            # Print pretty output
            print(f"  ✅ Price: ${round(current, 2)}")
            print(f"  📈 Change: {change_percent:+.2f}%")
            print(f"  📊 Volume: {volume:,}")
            print(f"  🎯 Signal: {signal}")
            
    except Exception as e:
        print(f"  ❌ {stock}: Error - {e}")

# Save results
with open('analysis.json', 'w') as f:
    json.dump(results, f, indent=2)

# Also create a readable text report
with open('report.txt', 'w') as f:
    f.write("=" * 70 + "\n")
    f.write("📊 STOCK SCREENER REPORT\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 70 + "\n\n")
    
    for r in results:
        f.write(f"【 {r['symbol']} 】\n")
        f.write(f"  Price: ${r['price']}\n")
        f.write(f"  Change: {r['change_percent']:+.2f}%\n")
        f.write(f"  Volume: {r['volume']:,}\n")
        f.write(f"  Day Range: ${r['day_low']} - ${r['day_high']}\n")
        f.write(f"  Signal: {r['signal']}\n")
        f.write(f"  P/E Ratio: {r['pe_ratio']}\n\n")

print("\n" + "=" * 60)
print(f"✅ Analysis complete! {len(results)} stocks analyzed")
print("📁 Files created: analysis.json and report.txt")
print("=" * 60)
