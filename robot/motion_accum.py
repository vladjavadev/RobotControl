from threading import Thread, Lock
import time 

DIRECTIONS = [
    (0, 1),    # 0: N
    (1, 1),    # 1: NE
    (1, 0),    # 2: E
    (1, -1),   # 3: SE
    (0, -1),   # 4: S
    (-1, -1),  # 5: SW
    (-1, 0),   # 6: W
    (-1, 1)    # 7: NW
]

class TrUnit:
    def __init__(self, side: str, rotateStep: int, moveStep: int):
        self.side = side
        self.moveStep = moveStep
        self.rotateStep = rotateStep
    def __eq__(self,other):
        return self.side==other.side and self.moveStep==other.moveStep and self.rotateStep==other.rotateStep

class MotionAccumulator:
    def __init__(self):
        self.path: list[tuple[int, int]] = None
        self.old_path: list[tuple[int,int]] = []
        self.trjList: list[TrUnit] = []
        self.pos: list[tuple[int,int]] = None
        self.dir: list[tuple[int, int]]= None
        
        self._lock = Lock()
        self._running = False
        self._thread: Thread = None
    
    def set_path(self, new_path: list[tuple[int, int]]):
        """Установить новый путь для обработки"""
        with self._lock:
            self.path = new_path.copy() if new_path else None
    
    def start(self, interval: float = 0.1):
        """
        Запустить мониторинг пути в отдельном потоке.
        
        Args:
            interval: интервал проверки изменений (секунды)
        """
        if self._running:
            print("MotionAccumulator уже запущен")
            return
        
        self._running = True
        self._thread = Thread(target=self._monitor_loop, args=(interval,), daemon=True)
        self._thread.start()
        print("MotionAccumulator запущен")
    
    def stop(self):
        """Остановить мониторинг"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
        print("MotionAccumulator остановлен")
    
    def _monitor_loop(self, interval: float):
        """Внутренний цикл мониторинга изменений пути"""
        while self._running:
            with self._lock:
                if self.path != self.old_path and self.path is not None:
                    print(f"\n📍 Обнаружен новый путь: {len(self.path)} точек")
                    self.accumulateMotion()
                    self.old_path = self.path.copy() if self.path else None
            
            time.sleep(interval)

    def accumulateMotion(self):
            if not self.path or len(self.path) < 2:
                return
            
            # Инициализация
            if self.trjList is None:
                self.trjList = []
            
            self.pos = self.path[0]
            
            moveStep = 0  # Первый шаг уже есть
            flag = False
            turn_buf = (0,"straight")
            start = 1
            for i in range(start, len(self.path)):
                new_pos = self.path[i]
                new_dir = self.get_dir(new_pos)
                
                if new_dir == (0, 0):
                    print("No movement detected.")
                    continue
                
                # Если направление изменилось
                if new_dir != self.dir:
                    # Рассчитываем поворот
                    if flag:
                        self.trjList.append(
                            TrUnit(side=turn_buf[1], rotateStep=turn_buf[0], moveStep=moveStep)
                        )
                        flag=False

                    turns = self.turns_needed(self.dir, new_dir)
                    turn_buf=turns
                    moveStep = 1
                    self.update_dir_pos(new_pos, new_dir)
                    flag = True
                else:
  
                    # Продолжаем движение в том же направлении
                    moveStep += 1
                    self.pos = new_pos
                    if start==i:
                        flag=True
            
            # Сохраняем последний сегмент (если есть накопленные шаги)
            if moveStep > 0 and self.dir != (0, 0):
                    self.trjList.append(
                        TrUnit(side=turn_buf[1], rotateStep=turn_buf[0], moveStep=moveStep)
                    )



    def get_dir(self, pos):
        delta_x = pos[0] - self.pos[0]
        delta_y = pos[1] - self.pos[1]
        print(f"   get_dir: delta=({delta_x}, {delta_y})")
        return (delta_x, delta_y)
    
    def get_dir_ix(self, vector):
        # Нормализуем вектор к единичным значениям
        norm_x = 0 if vector[0] == 0 else (1 if vector[0] > 0 else -1)
        norm_y = 0 if vector[1] == 0 else (1 if vector[1] > 0 else -1)
        normalized = (norm_x, norm_y)
        
        for i, dir_vec in enumerate(DIRECTIONS):
            if normalized == dir_vec:
                return i
        raise ValueError(f"Вектор {vector} (нормализован: {normalized}) не соответствует допустимому направлению")

    def turns_needed(self, start_vec, target_vec):
        start_idx = self.get_dir_ix(start_vec)
        target_idx = self.get_dir_ix(target_vec)

        spinL = (target_idx - start_idx) % 8
        spinR = (start_idx - target_idx) % 8
        turns = (spinR, "right") if spinR <= spinL else (spinL, "left")

        return turns

    def update_dir_pos(self, new_pos, new_dir): 
        self.pos = new_pos 
        self.dir = new_dir

    def get_trajectory(self) -> list[TrUnit]:
        """Получить текущую траекторию"""
        with self._lock:
            return self.trjList.copy() if self.trjList else []
    
    def print_trajectory(self):
        """Вывести траекторию в читаемом виде"""
        print("\n" + "="*60)
        print("📋 ТРАЕКТОРИЯ ДВИЖЕНИЯ:")
        print("="*60)
        
        if not self.trjList:
            print("  (пусто)")
            return
        
        total_moves = 0
        total_rotations = 0
        
        for i, unit in enumerate(self.trjList, 1):
            if unit.rotateStep > 0:
                print(f"{i}. 🔄 Поворот {unit.side} на {unit.rotateStep * 45}°")
                total_rotations += unit.rotateStep
            if unit.moveStep > 0:
                print(f"{i}. ➡️  Движение вперёд: {unit.moveStep} шаг(ов)")
                total_moves += unit.moveStep
        
        print("-" * 60)
        print(f"📊 Итого: {total_moves} шагов, {total_rotations} поворотов (×45°)")
        print("="*60 + "\n")


if __name__ == "__main__":
    # Тест 1: Простой путь с одним поворотом
    print("\n" + "🔵" * 30)
    print("📌 ТЕСТ 1: Путь с поворотом на 90° направо")
    print("🔵" * 30)
    ma1 = MotionAccumulator()
    path1 = [
        (0, 0),   # Старт
        (0, 1),   # N - шаг 1
        (0, 2),   # N - шаг 2
        (1, 2),   # E - поворот и шаг 1
        (2, 2),   # E - шаг 2
        (3, 2)    # E - шаг 3
    ]
    ma1.set_path(path1)
    ma1.accumulateMotion()
    ma1.print_trajectory()
    
    # Тест 2: Зигзаг
    print("\n" + "🟢" * 30)
    print("📌 ТЕСТ 2: Зигзагообразный путь")
    print("🟢" * 30)
    ma2 = MotionAccumulator()
    path2 = [
        (0, 0),   # Старт
        (1, 0),   # E
        (2, 0),   # E
        (2, 1),   # N (поворот влево 90°)
        (2, 2),   # N
        (3, 2),   # E (поворот вправо 90°)
        (4, 2),   # E
    ]
    ma2.set_path(path2)
    ma2.accumulateMotion()
    ma2.print_trajectory()
    
    # Тест 3: Диагональное движение
    print("\n" + "🟡" * 30)
    print("📌 ТЕСТ 3: Диагональное движение")
    print("🟡" * 30)
    ma3 = MotionAccumulator()
    path3 = [
        (0, 0),   # Старт
        (1, 1),   # NE
        (2, 2),   # NE
        (3, 3),   # NE
        (4, 3),   # E (поворот вправо 45°)
        (5, 3),   # E
    ]
    ma3.set_path(path3)
    ma3.accumulateMotion()
    ma3.print_trajectory()