import asyncio
import json
import logging

import aiohttp
from aiohttp import TCPConnector
from aiohttp.resolver import ThreadedResolver

from core.market_data.market_data_engine import market_data_engine

logger = logging.getLogger(__name__)


class WebSocketManager:

    def __init__(self, base_url="wss://fstream.binance.com/public/stream"):
        self.base_url = base_url

        self.session = None
        self.ws = None
        self.running = False

        self.streams = []
        self.handlers = {}

        self.reconnect_delay = 5
        self.max_reconnect_delay = 60

    # -------------------------------------------------
    # Streams
    # -------------------------------------------------

    def add_stream(self, stream):
        stream = stream.lower()

        if stream not in self.streams:
            self.streams.append(stream)

    def build_url(self):
        streams = "/".join(self.streams)
        return f"{self.base_url}?streams={streams}"

    # -------------------------------------------------
    # Connect
    # -------------------------------------------------

    async def connect(self):

        resolver = ThreadedResolver()

        connector = TCPConnector(
            resolver=resolver,
            use_dns_cache=True,
            ttl_dns_cache=300,
        )

        if self.session is None:
            self.session = aiohttp.ClientSession(connector=connector)

        url = self.build_url()

        print("=" * 80)
        print("Streams:", self.streams)
        print("URL:", url)
        print("Connecting...")

        try:

            self.ws = await asyncio.wait_for(
                self.session.ws_connect(
                    url,
                    heartbeat=30,
                    autoping=True,
                ),
                timeout=10,
            )

            print("CONNECTED")

        except Exception as e:

            print("CONNECT ERROR:", repr(e))
            raise

        self.running = True
        self.reconnect_delay = 5

    # -------------------------------------------------
    # Disconnect
    # -------------------------------------------------

    async def disconnect(self):

        self.running = False

        if self.ws:
            await self.ws.close()
            self.ws = None

        if self.session:
            await self.session.close()
            self.session = None

    # -------------------------------------------------
    # Register Handler
    # -------------------------------------------------

    def register_handler(self, stream, callback):
        self.handlers[stream.lower()] = callback

    # -------------------------------------------------
    # Dispatch
    # -------------------------------------------------

    async def dispatch(self, payload):

        stream = payload.get("stream", "").lower()
        data = payload.get("data", {})

        callback = self.handlers.get(stream)

        if callback:
            try:
                await callback(data)
            except Exception:
                logger.exception(f"Handler Error -> {stream}")

    # -------------------------------------------------
    # Receive
    # -------------------------------------------------

    async def receive(self):
        print("RECEIVER STARTED")
        async for message in self.ws:
            if message.type == aiohttp.WSMsgType.TEXT:

                payload = json.loads(message.data)

                market_data_engine.process(payload)

                await self.dispatch(payload)

            elif message.type == aiohttp.WSMsgType.ERROR:

                print("ERROR:", message)

                break

            elif message.type in (
                aiohttp.WSMsgType.CLOSED,
                aiohttp.WSMsgType.CLOSE,
            ):

                print("CLOSED")

                break

    # -------------------------------------------------
    # Run
    # -------------------------------------------------

    async def run(self):

        while True:

            try:

                await self.connect()

                logger.info("WebSocket Connected.")

                await self.receive()

            except Exception as e:

                logger.exception(f"WebSocket Error: {e}")

            finally:

                await self.disconnect()

            logger.info(f"Reconnect after {self.reconnect_delay} seconds...")

            await asyncio.sleep(self.reconnect_delay)

            self.reconnect_delay = min(
                self.reconnect_delay * 2,
                self.max_reconnect_delay,
            )
