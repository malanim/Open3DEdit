import time
import curses
from engine import Engine
from scene import Scene
from camera import Camera
from renderer import Renderer
from input_handler import InputHandler
from object import Cube, Plane
from vector import Vector3

def initialize_demo_scene(scene):
    """Инициализация демонстрационной сцены с базовыми объектами
    
    Args:
        scene: Сцена для инициализации
        
    Returns:
        Scene: Инициализированная сцена с добавленными объектами
    """
    # Добавляем куб
    cube = Cube(2.0)
    cube.translate(0, 0, 0)
    scene.add_object(cube)
    
    # Добавляем плоскость пола
    ground = Plane(10.0, 10.0)
    ground.translate(0, -2, 0)
    scene.add_object(ground)
    
    return scene

def main():
    """
    Главная функция для инициализации и запуска 3D движка
    
    Выполняет:
    - Создание основных компонентов (сцена, камера, рендерер)
    - Инициализацию движка
    - Запуск главного цикла обработки и рендеринга
    """
    try:
        # Создаем основные компоненты
        scene = Scene()
        scene = initialize_demo_scene(scene)
        camera = Camera(position=(0, 0, -10), target=(0, 0, 0))
        renderer = Renderer()
        input_handler = InputHandler()
        
        # Создаем и инициализируем движок
        engine = Engine(scene, camera, renderer, input_handler)
        engine.initialize()
        
        # Переменные для контроля частоты кадров
        target_fps = 30  # Целевое количество кадров в секунду
        frame_time = 1.0 / target_fps  # Время одного кадра
        last_time = time.time()
        
        try:
            # Main game loop
            while True:
                current_time = time.time()
                delta_time = current_time - last_time
                
                if delta_time >= frame_time:
                    # Обработка пользовательского ввода
                    input_handler.process_input()
                    
                    # Обновление состояния игры
                    engine.update(delta_time)
                    
                    # Отрисовка кадра
                    engine.render()
                    
                    last_time = current_time
                else:
                    # Sleep to maintain frame rate
                    time.sleep(0.001)
                    
        except KeyboardInterrupt:
            pass
            
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        # Cleanup engine (which handles curses cleanup)
        if 'engine' in locals():
            engine.cleanup()

if __name__ == "__main__":
    main()