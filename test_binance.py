from services.binance_service import BinanceService

service = BinanceService()

markets = service.get_markets()

print(f"Total Markets: {len(markets)}")

for symbol in list(markets.keys())[:20]:
    print(symbol)