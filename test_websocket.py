import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.loaders.candle_loader import candle_loader

# Load candles BEFORE asyncio starts
candle_loader.load(
    [
        "BTC/USDT:USDT",
        "ETH/USDT:USDT",
    ]
)

import asyncio
from core.websocket_supervisor import WebSocketSupervisor


async def main():

    supervisor = WebSocketSupervisor()

    supervisor.builder.timeframes = ["1m", "5m", "15m", "1h", "4h"]

    supervisor.builder.symbols = lambda: [
        "BTC/USDT:USDT",
        "ETH/USDT:USDT",
    ]

    print(supervisor.builder.all_streams())
    print(supervisor.summary())

    await supervisor.start()


if __name__ == "__main__":
    asyncio.run(main())
