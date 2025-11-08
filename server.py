#!/usr/bin/env python

"""Echo server using the asyncio API."""

import asyncio
from websockets.asyncio.server import serve
from grid_dto import GridDto
import main as mn
import json
import threading
import time


g_dt = GridDto()

async def echo(websocket, dto):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "start"

    if "obs" in event:
        dto.set_obs(event["obs"])
    elif "no-obs" in event:
        dto.rem_obs(event["no-obs"])
        

async def main():
    print("<!!!! Run SERVER !!!!>")
    async with serve(echo, "localhost", 8765, g_dt) as server:
        await server.serve_forever()

def moving_robot(dto):
    time.sleep(2.0)
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
        time.sleep(2.0)

class DoWork(threading.Thread):
    def __init__(self, shared, task_func, *args, **kwargs):
        super(DoWork, self).__init__(*args, **kwargs)
        self.shared = shared
        self.task_func = task_func  # передаём функцию

    def run(self):
        print(threading.current_thread(), 'start')
        time.sleep(1)
        self.task_func(self.shared)  # вызываем переданную функцию
        print(threading.current_thread(), 'done')




def run_server(dto):
    asyncio.run(main())


if __name__ == "__main__":
 
    threads = [ DoWork(shared=g_dt, task_func=mn.run_algorithm, name='a'), 
                DoWork(shared=g_dt, task_func=moving_robot, name='b'),
                DoWork(shared=g_dt, task_func=run_server, name='c')
]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
   

