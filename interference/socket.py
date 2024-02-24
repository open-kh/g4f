import aiohttp
import asyncio

async def ws_connect(session, url):
    while True:
        try:
            ws = await session.ws_connect(url)
            print("Connected to", url)
            async for msg in ws:
                # handle websocket messages here
                print(msg)
        except aiohttp.ClientConnectionError as e:
            print("Connection error:", e)
        print("Reconnecting to", url)
        await asyncio.sleep(1) # wait before reconnecting

async def main():
    async with aiohttp.ClientSession() as session:
        await ws_connect(session, "wss://echo.websocket.org")

asyncio.run(main())