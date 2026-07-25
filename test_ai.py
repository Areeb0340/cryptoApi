import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from market_data.models import Coin
from core.ai.coin_selector import CoinSelector


def main():

    print("=" * 60)
    print("AI SYSTEM TEST")
    print("=" * 60)

    btc = Coin.objects.filter(symbol__icontains="BTC").first()

    if btc is None:

        print("BTC not found")
        return

    selector = CoinSelector()

    result = selector.scan_coin(btc)

    if result is None:

        print("Scan Failed")
        return

    print("\nCoin :", result["symbol"])
    print("Signal :", result["signal"])
    print("Score :", result["score"])

    print("\n========== INDICATORS ==========\n")

    for tf, data in result["timeframes"].items():

        print(f"\n===== {tf} =====")

        print(
            "Final Score :",
            data["final_score"],
        )

        for name, values in data["indicators"].items():

            score = values.get("ai_score")

            if score is None:
                score = values.get("score")

            if score is None:
                score = values.get("trend_score")

            print(name)
            print(values)
            print("-" * 50)

    print("\n========================")
    print("AI DECISION")
    print("========================")

    decision = result["decision"]

    print("Signal :", decision["signal"])
    print("Confidence :", decision["confidence"])
    print("Bullish :", decision["bullish_points"])
    print("Bearish :", decision["bearish_points"])

    print("\nReasons")

    for reason in decision["reasons"]:
        print("-", reason)


if __name__ == "__main__":

    main()
