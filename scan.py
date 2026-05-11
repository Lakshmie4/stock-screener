import yfinance as yf
import json
from datetime import datetime

print("=" * 50)
print("📊 STOCK PRICE SCANNER")
print("=" * 50)

stocks = ['SPY', 'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'TSLA', 'AMZN', 'META']
results = []

for stock in stocks:
    try:
        print(f"Getting {stock}...")
        ticker = yf.Ticker(stock)
        data = ticker.history(period='1d')
        
        if not data.empty:
            price = data['Close'].iloc[-1]
            results.append({
                'symbol': stock,
                'price': round(price, 2),
                'timestamp': str(datetime.now())
            })
            print(f"  ✅ {stock}: ${round(price, 2)}")
    except Exception as e:
        print(f"  ❌ {stock}: Error")

with open('prices.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n" + "=" * 50)
print(f"✅ Done! Scanned {len(results)} stocks")
print("📁 Results saved to prices.json")
print("=" * 50)
