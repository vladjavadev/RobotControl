#!/usr/bin/env python
"""Client using the asyncio API."""
import asyncio
from websockets.asyncio.client import connect
import json


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


async def send_coord():
    """
    Подключается к WebSocket серверу и отправляет координаты препятствий.
    """
    uri = "ws://localhost:8765"
    
    try:
        async with connect(uri) as websocket:
            loop = asyncio.get_running_loop()
            
            print("Подключено к серверу!")
            print("Введите координаты препятствий (например: 1,2;3,4;5,6)")
            print("Или оставьте пустым для отправки без препятствий")
            
            # Неблокирующий ввод
            raw = await loop.run_in_executor(None, input, "Координаты: ")
            
            coords = parse_coord(raw) if raw.strip() else []
            
            event = {
                "type": "start",
                "obs": coords
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


async def main():
    """Главная функция с возможностью повторной отправки."""
    while True:
        await send_coord()
        
        # loop = asyncio.get_running_loop()
        # again = await loop.run_in_executor(None, input, "\nОтправить еще раз? (y/n): ")
        
        # if again.lower() != 'y':
        #     print("Завершение работы...")
        #     break


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")