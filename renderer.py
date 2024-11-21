import math
import curses
from typing import List, Tuple
from light import DirectionalLight
from vector import Vector3

class Renderer:
    """Класс для рендеринга 3D сцены в консоли

    Отвечает за:
    - Инициализацию экрана консоли
    - Отрисовку точек с учетом глубины и освещения 
    - Преобразование 3D координат в 2D координаты экрана
    - Применение матриц преобразования к вершинам
    """
    
    def __init__(self):
        self.screen = None
        self.width = 0
        self.height = 0
        self.ascii_chars = " .:-=+*#%@"  # Символы для отображения глубины
        self._initialized = False
        self.lights = []  # Список источников света
        self.ambient_intensity = 0.2  # Интенсивность фонового освещения
        self.specular_power = 32.0  # Степень отражения для specular подсветки
        self.specular_intensity = 0.5  # Интенсивность отражения
        
    def initialize(self, screen, lights: List = None) -> None:
        """Инициализация рендерера
        
        Args:
            screen: Окно curses для отрисовки
            
        Raises:
            ValueError: Если передан некорректный экран
            RuntimeError: При ошибке инициализации
        """
        if screen is None:
            raise ValueError("Screen cannot be None")
            
        try:
            self.screen = screen
            self.height, self.width = screen.getmaxyx()
            
            if self.height <= 0 or self.width <= 0:
                raise ValueError("Invalid screen dimensions")
                
            if not self._initialized:
                curses.start_color()
                curses.use_default_colors()
                for i in range(8):
                    curses.init_pair(i + 1, i, -1)
                self._initialized = True
            self.lights = lights or []
        except Exception as e:
            self._initialized = False
            raise RuntimeError(f"Failed to initialize renderer: {str(e)}")
        
    def clear(self) -> None:
        """Очистка экрана"""
        self.screen.clear()
        
    def draw_point(self, x: int, y: int, depth: float, normal: List[float], position: List[float], intensity: float = 1.0) -> None:
        """Отрисовка точки с учетом глубины и освещения
        
        Args:
            x: Координата x на экране
            y: Координата y на экране  
            depth: Глубина точки в диапазоне [-1, 1]
            normal: Нормаль поверхности в точке [nx, ny, nz]
            position: Позиция точки в мировых координатах [x, y, z]
            intensity: Базовая интенсивность освещения [0, 1]
        
        Raises:
            RuntimeError: Если рендерер не инициализирован
        """
        if not self._initialized:
            raise RuntimeError("Renderer not initialized")
            
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
            
        # Ensure depth is in [-1, 1] range
        depth = max(-1.0, min(1.0, depth))
            
        # Calculate lighting from all sources
        total_intensity = self.ambient_intensity  # Start with ambient light
        
        # Convert position and normal to Vector3 if they're lists
        pos_vec = Vector3(*position) if isinstance(position, (list, tuple)) else position
        normal_vec = Vector3(*normal) if isinstance(normal, (list, tuple)) else normal
        normal_vec = normal_vec.normalize()
        
        for light in self.lights:
            if hasattr(light, 'get_intensity'):
                # Get light direction and intensity
                light_dir = light.get_direction(pos_vec)
                light_intensity = light.get_intensity(pos_vec)
                
                # Calculate diffuse lighting using normal
                dot_product = normal_vec.dot(light_dir)
                diffuse = max(0.0, dot_product) * light_intensity
                
                # Calculate specular reflection
                reflection = (normal_vec.scale(2.0 * dot_product) - light_dir).normalize()
                view_dir = Vector3(0, 0, 1)  # Assuming camera looks along Z axis
                spec_dot = max(0.0, reflection.dot(view_dir))
                specular = pow(spec_dot, self.specular_power) * self.specular_intensity
                
                total_intensity += (diffuse + specular) * intensity

        # Clamp total intensity
        total_intensity = min(1.0, max(0.0, total_intensity))
        
        # Convert depth to [0, 1] range and combine with lighting
        normalized_depth = (-depth + 1.0) * 0.5 * total_intensity
        
        # Convert depth to ASCII character index
        char_index = min(int(normalized_depth * (len(self.ascii_chars) - 1)), 
                        len(self.ascii_chars) - 1)
        
        try:
            self.screen.addch(int(y), int(x), self.ascii_chars[char_index])
        except curses.error:
            # Ignore errors when writing to the last cell
            pass
            
    def add_light(self, light) -> None:
        """Add a light source to the renderer
        
        Args:
            light: Light source object with get_direction() and get_intensity() methods
        """
        self.lights.append(light)
        
    def render(self, scene, camera) -> None:
        """Рендеринг всей сцены
        
        Выполняет:
        - Очистку экрана
        - Получение матриц вида и проекции от камеры
        - Преобразование координат вершин объектов
        - Отрисовку всех видимых точек
        
        Args:
            scene: Сцена с объектами для рендеринга
            camera: Камера, определяющая точку обзора
            
        Raises:
            RuntimeError: Если рендерер не инициализирован
        """
        if not self.screen:
            raise RuntimeError("Renderer not initialized")
            
        self.clear()
        
        if scene and camera:
            # Получаем матрицы преобразования
            view_matrix = camera.get_view_matrix()
            projection_matrix = camera.get_projection_matrix()
            
            # Рендерим каждый объект в сцене
            if hasattr(scene, 'objects'):
                for obj in scene.objects:
                    if hasattr(obj, 'vertices'):
                        for vertex in obj.vertices:
                            # Применяем матрицу вида
                            view_pos = self._apply_matrix(vertex, view_matrix)
                            # Применяем проекцию
                            proj_pos = self._apply_matrix(view_pos, projection_matrix)
                            
                            # Преобразуем в экранные координаты
                            if proj_pos[3] != 0:
                                screen_x = int((proj_pos[0] / proj_pos[3] + 1.0) * self.width * 0.5)
                                screen_y = int((1.0 - proj_pos[1] / proj_pos[3]) * self.height * 0.5)
                                depth = (proj_pos[2] / proj_pos[3] + 1.0) * 0.5
                                
                                self.draw_point(screen_x, screen_y, depth)
        
        self.screen.refresh()
        
    def _apply_matrix(self, point, matrix: List[List[float]]) -> List[float]:
        """Применение матричного преобразования к точке в однородных координатах
        
        Args:
            point: Точка для преобразования (Vector3 или список из 3-4 координат)
            matrix: Матрица преобразования 4x4
            
        Returns:
            List[float]: Преобразованные координаты точки
            
        Raises:
            ValueError: При некорректной матрице или точке
        """
        if not matrix or len(matrix) != 4 or any(len(row) != 4 for row in matrix):
            raise ValueError("Invalid transformation matrix")
            
        # Handle Vector3 objects
        if hasattr(point, 'x'):
            point = [point.x, point.y, point.z, 1.0]
        # Handle regular sequences
        elif len(point) == 3:
            point = [point[0], point[1], point[2], 1.0]
        elif len(point) != 4:
            raise ValueError("Point must have 3 or 4 coordinates")
            
        result = [0.0, 0.0, 0.0, 0.0]
        for i in range(4):
            result[i] = sum(point[j] * matrix[i][j] for j in range(4))
            
        # Prevent division by zero in projection
        if abs(result[3]) < 1e-7:
            result[3] = 1e-7
            
        return result