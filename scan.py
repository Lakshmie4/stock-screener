import yfinance as yf
import json
from datetime import datetime

print("=" * 60)
print("📊 STOCK SCREENER")
print("=" * 60)

stocks = ['SPY', 'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'TSLA', 'AMZN', 'META']
results = []

for stock in stocks:
    try:
        print(f"\nAnalyzing {stock}...")
        
        ticker = yf.Ticker(stock)
        hist = ticker.history(period='2d')
        
        if hist.empty:
            print(f"  ❌ No data for {stock}")
            continue
        
        current_price = hist['Close'].iloc[-1]
        
        if len(hist) > 1:
            prev_close = hist['Close'].iloc[-2]
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100
        else:
            change = 0
            change_percent = 0
        
        volume = hist['Volume'].iloc[-1]
        day_high = hist['High'].iloc[-1]
        day_low = hist['Low'].iloc[-1]
        
        if change_percent > 1:
            signal = "BUY"
        elif change_percent < -1:
            signal = "SELL"
        else:
            signal = "HOLD"
        
        results.append({
            'symbol': stock,
            'price': round(float(current_price), 2),
            'change': round(float(change), 2),
            'change_percent': round(float(change_percent), 2),
            'volume': int(volume),
            'day_high': round(float(day_high), 2),
            'day_low': round(float(day_low), 2),
            'signal': signal,
            'timestamp': str(datetime.now())
        })
        
        print(f"  ✅ Price: ${round(float(current_price), 2)}")
        print(f"  📈 Change: {change_percent:+.2f}%")
        print(f"  🎯 Signal: {signal}")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")

with open('analysis.json', 'w') as f:
    json.dump(results, f, indent=2)

with open('report.txt', 'w') as f:
    f.write("=" * 60 + "\n")
    f.write("STOCK SCREENER REPORT\n")
    f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 60 + "\n\n")
    
    for r in results:
        f.write(f"\n【{r['symbol']}】\n")
        f.write(f"  Price: ${r['price']}\n")
        f.write(f"  Change: {r['change_percent']:+.2f}%\n")
        f.write(f"  Volume: {r['volume']:,}\n")
        f.write(f"  Day Range: ${r['day_low']} - ${r['day_high']}\n")
        f.write(f"  Signal: {r['signal']}\n")

print("\n" + "=" * 60)
print(f"✅ Done! Analyzed {len(results)} stocks")
print("📁 Files: analysis.json and report.txt")
print("=" * 60)
