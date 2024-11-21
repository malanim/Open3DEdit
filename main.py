import time
import curses
import logging
from datetime import datetime
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

def setup_logging():
    """Setup logging configuration"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logging.basicConfig(
        filename=f'logs/engine_{timestamp}.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting 3D Engine Demo")
    except Exception as e:
        print(f"Failed to initialize logging: {str(e)}")
        return
    """
    Главная функция для инициализации и запуска 3D движка
    
    Выполняет:
    - Создание основных компонентов (сцена, камера, рендерер)
    - Инициализацию движка
    - Запуск главного цикла обработки и рендеринга
    """
    try:
        logger.info("Creating core components")
        try:
            scene = Scene()
            scene = initialize_demo_scene(scene)
        except Exception as e:
            logger.error(f"Failed to initialize scene: {str(e)}")
            raise
            
        try:
            camera = Camera(position=(0, 0, -10), target=(0, 0, 0))
        except Exception as e:
            logger.error(f"Failed to initialize camera: {str(e)}")
            raise
            
        try:
            renderer = Renderer()
        except Exception as e:
            logger.error(f"Failed to initialize renderer: {str(e)}")
            raise
            
        try:
            input_handler = InputHandler()
        except Exception as e:
            logger.error(f"Failed to initialize input handler: {str(e)}")
            raise
        
        # Создаем и инициализируем движок
        engine = Engine(scene, camera, renderer, input_handler)
        
        # Устанавливаем начальное состояние компонентов
        engine.set_component_status('scene', True)
        engine.set_component_status('camera', True)
        engine.set_component_status('renderer', False)  # Will be set in initialize()
        engine.set_component_status('input', False)  # Will be set in initialize()
        
        # Инициализация движка
        engine.initialize()
        
        # Запускаем игровой цикл
        try:
            engine.run()
        except KeyboardInterrupt:
            pass
            
    except Exception as e:
        error_msg = f"\nError: {str(e)}"
        print(error_msg)
        logger.error(error_msg)
    finally:
        # Cleanup engine (which handles curses cleanup)
        if 'engine' in locals():
            engine.cleanup()

if __name__ == "__main__":
    main()