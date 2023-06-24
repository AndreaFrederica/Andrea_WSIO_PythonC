import asyncio
import websockets
import json
import time

from module import router
from module import context


server = "ws://localhost:23080"


async def main():
    async with websockets.connect(server) as websocket:
        context.context = websocket
        while True:
            command = await websocket.recv()
            print(command)
            await router.taskRoute(command)


asyncio.run(main())