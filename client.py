#!/usr/bin/env python
"""Client using the asyncio API."""
import asyncio
from websockets.asyncio.client import connect
import json
import functools

import threading

class RobotPos:
    def __init__(self, pos):
        self.pos = pos

def parse_coord(input_str):
    """
    Парсит строку координат вида 'x1,y1;x2,y2;...'
    Возвращает список кортежей [(x1, y1), (x2, y2), ...]
    """
    try:
        # Убираем лишние пробелы
        input_str = input_str.strip()
        if not input_str:
            print("Пустая строка!")
            return []
        
        coords = [tuple(map(int, pair.split(','))) for pair in input_str.split(';')]
        
        # Проверяем, что все пары имеют 2 элемента
        for coord in coords:
            if len(coord) != 2:
                print(f"Неверная пара координат: {coord}")
                return []
        
        return coords
    except ValueError as e:
        print(f"Ошибка парсинга: {e}. Используй формат: x1,y1;x2,y2;...")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return []

async def set_no_obs(grid_cell):
    d_nObs = {"no-obs": [grid_cell]}
    await send_message(d_nObs)

async def set_obs(grid_cell):
    d_Obs = {"obs": [grid_cell]}
    await send_message(d_Obs)



async def send_message(message):
    """
    Подключается к WebSocket серверу и отправляет координаты препятствий.
    """
    uri = "ws://localhost:8765"

    try:
        async with connect(uri) as websocket:
            event = {
                "type": "start",
                **message
            }
            
            await websocket.send(json.dumps(event))
            print(f"✓ Событие отправлено: {event}")
            
            # Опционально: ожидание ответа от сервера
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"Ответ сервера: {response}")
            except asyncio.TimeoutError:
                print("Сервер не ответил в течение 5 секунд")
            
    except ConnectionRefusedError:
        print("❌ Не удалось подключиться к серверу. Проверьте, что сервер запущен на ws://localhost:8765")
    except Exception as e:
        print(f"❌ Ошибка: {e}")



def send_obs_coord(grid_cell):
    asyncio.run(set_obs(grid_cell))


def send_no_obs_coord(grid_cell):
    asyncio.run(set_no_obs(grid_cell))

def get_pos(pos):
    asyncio.run(async_get_pos(pos))

async def async_get_pos(pos):
    uri = "ws://localhost:8765"

    try:
        async with connect(uri) as websocket:
            event = {
                "type": "pos"
            }
            
            await websocket.send(json.dumps(event))
            print(f"✓ Событие отправлено: {event}")
            
            # Опционально: ожидание ответа от сервера
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=40.0)
                event_pos = json.loads(response)
                if event_pos["type"] == "pos":
                    if "current_pos" in event_pos:
                        pos.pos = tuple(event_pos["current_pos"])

                print(f"Ответ сервера: {response}")
            except asyncio.TimeoutError:
                print("Сервер не ответил в течение 5 секунд")
            
    except ConnectionRefusedError:
        print("❌ Не удалось подключиться к серверу. Проверьте, что сервер запущен на ws://localhost:8765")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(send_message())
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")