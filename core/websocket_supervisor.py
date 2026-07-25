from handlers.kline_handler import KlineHandler
from handlers.depth_handler import DepthHandler
from handlers.trade_handler import TradeHandler
from handlers.bookticker_handler import BookTickerHandler

import asyncio

from core.stream_builder import StreamBuilder
from core.websocket_pool import WebSocketPool


class WebSocketSupervisor:

    PUBLIC_URL = "wss://fstream.binance.com/public/stream"
    MARKET_URL = "wss://fstream.binance.com/market/stream"

    def __init__(self):

        self.builder = StreamBuilder()

        self.public_pool = WebSocketPool()
        self.market_pool = WebSocketPool()

        self.kline_handler = KlineHandler()
        self.depth_handler = DepthHandler()
        self.trade_handler = TradeHandler()
        self.bookticker_handler = BookTickerHandler()

    def _register_handlers(self, manager):

        for stream in manager.streams:

            if "@kline_" in stream:
                manager.register_handler(stream, self.kline_handler)

            elif "@depth" in stream:
                manager.register_handler(stream, self.depth_handler)

            elif "@trade" in stream:
                manager.register_handler(stream, self.trade_handler)

            elif "@bookticker" in stream.lower():
                manager.register_handler(stream, self.bookticker_handler)

    async def start(self):

        public_streams = self.builder.public_streams()
        market_streams = self.builder.market_streams()

        print("PUBLIC STREAMS:", public_streams)
        print("MARKET STREAMS:", market_streams)

        self.public_pool.create_pool(public_streams, base_url=self.PUBLIC_URL)
        self.market_pool.create_pool(market_streams, base_url=self.MARKET_URL)

        tasks = []

        for manager in self.public_pool.get_managers():
            self._register_handlers(manager)
            tasks.append(asyncio.create_task(manager.run()))

        for manager in self.market_pool.get_managers():
            self._register_handlers(manager)
            tasks.append(asyncio.create_task(manager.run()))

        await asyncio.gather(*tasks)

    def summary(self):
        return {
            "public": self.public_pool.summary(),
            "market": self.market_pool.summary(),
        }
