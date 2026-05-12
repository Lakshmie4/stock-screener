import yfinance as yf
import json
from datetime import datetime

print("STOCK SCANNER STARTED")
print("-" * 40)

stocks = ["SPY", "AAPL", "MSFT", "NVDA", "GOOGL", "TSLA", "AMZN", "META"]
all_data = []

for stock in stocks:
    print(f"Getting {stock}...")
    ticker = yf.Ticker(stock)
    info = ticker.info
    price = info.get("regularMarketPrice", 0)
    if price > 0:
        all_data.append({
            "symbol": stock,
            "price": round(price, 2),
            "time": str(datetime.now())
        })
        print(f"  ${round(price, 2)}")
    else:
        print(f"  No price data for {stock}")

with open("prices.json", "w") as f:
    json.dump(all_data, f, indent=2)

with open("report.txt", "w") as f:
    f.write("STOCK PRICES\n")
    f.write("=" * 30 + "\n")
    for item in all_data:
        f.write(f"{item['symbol']}: ${item['price']}\n")

print(f"\nDONE! {len(all_data)} stocks saved")
