#!/usr/bin/env python

"""Echo server using the asyncio API."""

import asyncio
from websockets.asyncio.server import serve, ServerConnection
from server.grid_dto import GridDto
from robot.move_logic import Logic
import core.algorithm as agm
import json
import threading
import time
import functools


g_dt = GridDto()
logic = Logic(g_dt,dir=(0,1))

<<<<<<< HEAD

=======
>>>>>>> 01e13ff17510a775f81a9932497227c643e14209
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


def moving_robot(logic: Logic):
    time.sleep(5.0)
    
    while True:
        path = logic.dto.get_path()
        if logic.dto.get_position() == logic.dto.get_goal():
            break

        if path is not None:
            if len(path)>1:
               print(f"MOVE ROBOT POS:{logic.dto.get_position()}")
               logic.build_route(path[0],path[1])
               logic.dto.set_position(path[1])
            else:
                logic.dto.set_position(path[0])
                logic.build_route(path[0],path[0])
                print("Client: Reached Goal!")
        # time.sleep(0.1)
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
 
    threads = [ DoWork(shared=g_dt, task_func=agm.run_algorithm, name='a'), 
                DoWork(shared=logic, task_func=moving_robot, name='b'),
                DoWork(shared=g_dt, task_func=run_server, name='c')
]
    for t in threads:
        t.start()

    for t in threads:
        t.join()
   

