#!/usr/bin/env python

"""Echo server using the asyncio API."""

import asyncio
from websockets.asyncio.server import serve, ServerConnection
from server.grid_dto import GridDto
import core.algorithm as agm
import json
from core.work import DoWork
import time
import functools


g_dt = GridDto()

async def echo(dto:GridDto, websocket:ServerConnection):
    message = await websocket.recv()
    event = json.loads(message)
   
    # assert event["type"] == "start"
    if event["type"] == "start":
        
        if "obs" in event:
            print("<!------",event["obs"][0],"------!>")
            dto.set_obs(event["obs"][0])
        elif "no-obs" in event:
            dto.rem_obs(event["no-obs"][0])
    elif event["type"] == "get-location":
        pos = dto.get_position()
        path = dto.get_path()
        event_location = {
            "type":"location",
            "current_pos":pos,
            "path":path
        }
        await websocket.send(json.dumps(event_location))
    else:
        KeyError("NO route finded")


async def get_pos(dto: GridDto, websocket:ServerConnection):
    pos = dto.get_position()
    websocket.send(pos)

        

async def main():
    print("<!!!! Run SERVER !!!!>")
    bound_handler = functools.partial(echo, g_dt)
    async with serve(bound_handler, "localhost", 8765) as server:
        await server.serve_forever()


def moving_robot(dto):
    time.sleep(10.0)
    while True:
        path = dto.get_path()
        if dto.get_position() == dto.get_goal():
            break

        if path is not None:
            if len(path)>1:
               dto.set_position(path[1])
            else:
                dto.set_position(path[0])
                print("Client: Reached Goal!")
        time.sleep(6.0)



def run_server(dto):
    asyncio.run(main())


if __name__ == "__main__":
 
    threads = [ DoWork(shared=g_dt, task_func=agm.run_algorithm, name='a'), 
                DoWork(shared=g_dt, task_func=moving_robot, name='b'),
                DoWork(shared=g_dt, task_func=run_server, name='c')
]
    for t in threads:
        t.start()

    for t in threads:
        t.join()
   

