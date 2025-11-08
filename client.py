#!/usr/bin/env python

"""Client using the asyncio API."""

import asyncio
from websockets.asyncio.client import connect
import json

def parse_coord(input_str):
    try:
        coords = [tuple(map(int,pair.split(','))) for pair in input_str.split(';')]
        return coords
    except:
        print("Неверный формат. Используй: x1,y1 x2,y2 ...")
        return []

async def send_coord():
    uri = "ws://localhost:8765"
    async with connect(uri) as websocket:
        print("Введите координаты (например: 1,2 3,4 5,6)")
        raw = input("Координаты: ")
        coords = parse_coord(raw)
        if not coords:
            return

        event = {
            "type": "start",
            "obs": coords  # координаты препятствий
        }
        await websocket.send(json.dumps(event))



if __name__ == "__main__":
    asyncio.run(send_coord())