import __main__
import asyncio

async def task(client, cfg):
    await client.wait_until_ready()
    while not client.is_closed() and client.is_ready():
        print("Hello from test.py")
        await asyncio.sleep(5)

def register(client, cfg):
    return task(client, cfg)