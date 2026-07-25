# test_engines.py — run isko standalone: python test_engines.py

import random
from core.smc.smc_engine import smc_engine
from core.ai.indicator_engine import IndicatorEngine
from core.ai.decision_engine import DecisionEngine
from core.smc.confluence_engine import confluence_engine

SYMBOL = "BTCUSDT"
TIMEFRAME = "15m"


def generate_fake_candles(n=100, start_price=60000):
    """Random walk candles taake indicators calculate ho sakein"""
    opens, highs, lows, closes, volumes = [], [], [], [], []
    price = start_price

    for _ in range(n):
        change = random.uniform(-100, 100)
        o = price
        c = price + change
        h = max(o, c) + random.uniform(0, 50)
        l = min(o, c) - random.uniform(0, 50)
        v = random.uniform(10, 500)

        opens.append(o)
        highs.append(h)
        lows.append(l)
        closes.append(c)
        volumes.append(v)

        price = c

    return opens, highs, lows, closes, volumes


def feed_candles_to_smc(opens, highs, lows, closes, volumes):
    """SMC engine ko candle-by-candle feed karo taake cache/state build ho"""
    from core.market_data.cache import cache

    for i in range(len(closes)):
        candle = {
            "open_time": i,
            "close_time": i + 1,
            "open": opens[i],
            "high": highs[i],
            "low": lows[i],
            "close": closes[i],
            "volume": volumes[i],
            "closed": True,
        }
        cache.klines[SYMBOL][TIMEFRAME].append(candle)

    # Ab final candle pe SMC calculate karo
    smc_engine.update(SYMBOL, TIMEFRAME)


def main():
    print("=" * 60)
    print("STEP 1: Generating fake candle data...")
    opens, highs, lows, closes, volumes = generate_fake_candles(100)
    print(f"Generated {len(closes)} candles. Last close: {closes[-1]:.2f}")

    print("\n" + "=" * 60)
    print("STEP 2: Feeding candles to SMC Engine...")
    try:
        feed_candles_to_smc(opens, highs, lows, closes, volumes)
        print("✅ SMC Engine ran without crashing")
    except Exception as e:
        print(f"❌ SMC Engine CRASHED: {e}")
        import traceback

        traceback.print_exc()
        return

    print("\n" + "=" * 60)
    print("STEP 3: Checking Confluence Score...")
    try:
        conf_result = confluence_engine.score[SYMBOL][TIMEFRAME]
        print(f"✅ Confluence Score: {conf_result}")
    except Exception as e:
        print(f"❌ Confluence check CRASHED: {e}")

    print("\n" + "=" * 60)
    print("STEP 4: Running Indicator Engine...")
    try:
        indicator_result = IndicatorEngine.run(
            SYMBOL, opens, highs, lows, closes, volumes
        )
        print(
            f"✅ Indicator Engine ran. Final Score: {indicator_result['final_score']}"
        )
        print(
            f"   Indicators calculated: {list(indicator_result['indicators'].keys())}"
        )
    except Exception as e:
        print(f"❌ Indicator Engine CRASHED: {e}")
        import traceback

        traceback.print_exc()
        return

    print("\n" + "=" * 60)
    print("STEP 5: Running Decision Engine...")
    try:
        decision = DecisionEngine.decide(
            SYMBOL,
            TIMEFRAME,
            indicator_result["indicators"],
            oi_data=None,
            funding_data=None,
        )
        print(f"✅ Decision Engine ran successfully!")
        print(f"\n   FINAL SIGNAL: {decision['signal']}")
        print(f"   Confidence: {decision['confidence']}%")
        print(f"   Bullish points: {decision['bullish_points']}")
        print(f"   Bearish points: {decision['bearish_points']}")
        print(f"   SMC Score: {decision['smc_score']}")
        print(f"   Reasons: {decision['reasons']}")
    except Exception as e:
        print(f"❌ Decision Engine CRASHED: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
