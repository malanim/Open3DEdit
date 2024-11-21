import time
import curses
from typing import List
from scene import Scene
from camera import Camera
from renderer import Renderer
from input_handler import InputHandler

class Engine:
    """Класс для управления игровым движком"""
    
    def __init__(self, scene: Scene, camera: Camera, renderer: Renderer, input_handler: InputHandler):
        self.scene = scene
        self.camera = camera
        self.renderer = renderer
        self.input_handler = input_handler
        self.running = False
        self.last_time = 0.0
        self.target_fps = 30
        self.frame_time = 1.0 / self.target_fps
        self.screen = None
        
    def initialize(self) -> None:
        """Инициализация движка"""
        # Инициализация curses
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        curses.curs_set(0)
        
        # Инициализация компонентов
        self.renderer.initialize(self.screen)
        self.input_handler.initialize(self.screen)
        
    def cleanup(self) -> None:
        """Очистка ресурсов при выходе"""
        if self.screen:
            self.screen.keypad(False)
            curses.nocbreak()
            curses.echo()
            curses.endwin()
        
    def run(self) -> None:
        """Запуск игрового цикла"""
        try:
            self.initialize()
            self.running = True
            self.last_time = time.time()
            
            while self.running:
                current_time = time.time()
                delta_time = current_time - self.last_time
                
                # Ограничение FPS
                sleep_time = self.frame_time - delta_time
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    current_time = time.time()
                    delta_time = current_time - self.last_time
                
                self.last_time = current_time
                
                # Обновление состояния
                self.update(delta_time)
                
                # Рендеринг
                self.render()
                
        except Exception as e:
            self.cleanup()
            raise e
            
    def update(self, delta_time: float) -> None:
        """Обновление состояния игры"""
        # Обработка ввода
        self.input_handler.process_input()
        
        # Обновление сцены и объектов
        self.scene.update(delta_time)
        
        # Обновление камеры
        self.camera.update(delta_time)
        
    def render(self) -> None:
        """Отрисовка сцены"""
        self.renderer.render(self.scene, self.camera)
        
    def stop(self) -> None:
        """Остановка игрового цикла"""
        self.running = False