#!/usr/bin/env python

"""Echo server using the asyncio API."""

import asyncio
from websockets.asyncio.server import serve
from grid_dto import GridDto
import main as mn
import json
import threading


g_dt = GridDto()

async def echo(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "start"

    if "obs" in event:
        g_dt.set_obs(event["obs"])
    elif "no-obs" in event:
        g_dt.rem_obs(event["no-obs"])
        

async def main():
    async with serve(echo, "localhost", 8765) as server:
        await server.serve_forever()


if __name__ == "__main__":
    thread = threading.Thread(target=mn.run_algorithm)
    thread.start()
    asyncio.run(main())