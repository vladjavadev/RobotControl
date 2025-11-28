#!/usr/bin/env python

"""Echo server using the asyncio API."""

import asyncio
from websockets.asyncio.server import serve, ServerConnection
from data.grid_dto import GridDto
from robot.move_logic import Logic
import core.algorithm as agm
from path_observation import PathObservation
import json
import threading
import time
import functools

#change value for 2 mode 
mode=3
g_dt = GridDto()

logic = None

# ip="0.0.0.0"
ip="localhost"

async def echo(dto:GridDto, websocket:ServerConnection):
    message = await websocket.recv()
    event = json.loads(message)
   
    # assert event["type"] == "start"
    if event["type"] == "set-obs":
        
        if "obs" in event:
            print("<!------",event["obs"][0],"------!>")
            dto.set_obs(event["obs"][0])
        elif "no-obs" in event:
            dto.rem_obs(event["no-obs"][0])
    elif event["type"] == "get-location":
        pos = dto.get_position()
        goal= dto.get_goal()
        path = dto.get_path()
        totalDistance = dto.get_total_distance()
        pred_time, pred_distance = dto.get_predict_time_distance()
        event_location = {
            "type":"location",
            "current_pos":pos,
            "goal":goal,
            "path":path,
            "distance":totalDistance,
            "pred_time": pred_time,
            "pred_distance": pred_distance
        }
        await websocket.send(json.dumps(event_location))

    elif event["type"] == "get-status":
        event_connected = {
            "type":"get-status",
            "status":"connected"
        }
        await websocket.send(json.dumps(event_connected))
    elif event["type"] == "init-dim":
        global logic

        dto.set_dim(event["grid_dim"])
        dto.set_unit(event["cell_unit"])
        logic = Logic(dto,dir=(0,1),vMode=mode)

    elif event["type"] == "init-points":
        dto.set_start(event["start"])
        dto.set_goal(event["goal"])
    

        m_threads = [DoWork(shared=g_dt, task_func=agm.run_algorithm, name='a'), 
        DoWork(shared=logic, task_func=moving_robot, name='b')]
        for i in m_threads:
            i.start()
        # for i in m_threads:
        #     i.join()
    else:
        KeyError("NO route finded")


async def get_pos(dto: GridDto, websocket:ServerConnection):
    pos = dto.get_position()
    websocket.send(pos)

        

async def main():
    print("<!!!! Run SERVER !!!!>")
    bound_handler = functools.partial(echo, g_dt)
    async with serve(bound_handler, ip, 8765) as server:
        await server.serve_forever()


def moving_robot(logic: Logic):
    time.sleep(5.0)
    last_path = []
    last_pos=logic.dto.get_position()
    next_pos = None
    temp=(0,0)
    fullTime = []
    builTime = []
    pathTime = []
    predTime = []
    p_obs = PathObservation() 
    threading.Thread(target=move_process, args=(p_obs, logic)).start()
    while True:
        try:
            time.sleep(0.05)
            start_time = time.time()
            full_time = time.time()
            path = logic.dto.get_path()

            if path is not None and path!=last_path:
                if len(path)>1:
                    if not p_obs.is_updated:    
                        next_pos = path[1]
                        p_obs.update(next_pos)

            if logic.dto.get_position() == tuple(logic.dto.get_goal()):
                print(f"MOVE ROBOT POS:{logic.dto.get_position()}")
                p_obs.is_done = True
                print("Client: Reached Goal!")
                break
        except Exception as e:
            print("MOVING ROBOT EXCEPTION:", e)
            logic.stop()
        # time.sleep(0.1)
    print("Path Finding Times:", pathTime)
    print("Prediction Times:", predTime)
    print("Build Route Times:", builTime)
    print("Full Loop Times:", fullTime)
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


def move_process(p_obs: PathObservation, logic: Logic):
    counter = 0
    start = time.time()
    while True:

        time.sleep(0.05)
        if p_obs.is_updated:
            logic.build_route(p_obs.next_pos)
            logic.dto.set_position(p_obs.next_pos)
            p_obs.is_updated = False
        elif counter ==4:
            print("No path update, stop robot ", time.time()-start)
            start = time.time()
            logic.stop()
        elif p_obs.is_done:
            logic.stop()
            break

        counter  = counter%4+1


def run_server(dto):
    asyncio.run(main())


if __name__ == "__main__":
 
    threads = [ DoWork(shared=g_dt, task_func=run_server, name='c')]
    for t in threads:
        t.start()

    for t in threads:
        t.join()
   

