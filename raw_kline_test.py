import asyncio
import json
import aiohttp
from aiohttp import TCPConnector
from aiohttp.resolver import ThreadedResolver


async def main():
    url = "wss://fstream.binance.com/market/stream?streams=btcusdt@kline_1m"

    resolver = ThreadedResolver()
    connector = TCPConnector(resolver=resolver, use_dns_cache=True, ttl_dns_cache=300)

    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.ws_connect(url, heartbeat=30, autoping=True) as ws:
            print("CONNECTED, waiting up to 30s...")
            try:
                msg = await asyncio.wait_for(ws.receive(), timeout=30)
                print(f"✅ GOT MESSAGE: {str(msg.data)[:200]}")
            except asyncio.TimeoutError:
                print("❌ TIMEOUT")


asyncio.run(main())
