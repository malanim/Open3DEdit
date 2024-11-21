import math
import curses
from typing import List, Tuple

class Renderer:
    """Класс для рендеринга 3D сцены в консоли"""
    
    def __init__(self):
        self.screen = None
        self.width = 0
        self.height = 0
        self.ascii_chars = " .:-=+*#%@"  # Символы для отображения глубины
        self._initialized = False
        
    def initialize(self, screen) -> None:
        """Initialize the renderer"""
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
        except Exception as e:
            self._initialized = False
            raise RuntimeError(f"Failed to initialize renderer: {str(e)}")
        
    def clear(self) -> None:
        """Очистка экрана"""
        self.screen.clear()
        
    def draw_point(self, x: int, y: int, depth: float, intensity: float = 1.0) -> None:
        """Draw a point with depth and lighting consideration"""
        if not self._initialized:
            raise RuntimeError("Renderer not initialized")
            
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
            
        # Ensure depth is in [-1, 1] range
        depth = max(-1.0, min(1.0, depth))
            
        # Convert depth to [0, 1] range and combine with lighting
        normalized_depth = (-depth + 1.0) * 0.5
        # Применяем интенсивность освещения
        normalized_depth *= intensity
        
        # Convert depth to ASCII character index
        char_index = min(int(normalized_depth * (len(self.ascii_chars) - 1)), 
                        len(self.ascii_chars) - 1)
        
        try:
            self.screen.addch(int(y), int(x), self.ascii_chars[char_index])
        except curses.error:
            # Ignore errors when writing to the last cell
            pass
            
    def render(self, scene, camera) -> None:
        """Рендеринг сцены"""
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
        
    def _apply_matrix(self, point: List[float], matrix: List[List[float]]) -> List[float]:
        """Apply matrix transformation to a point in homogeneous coordinates"""
        if not matrix or len(matrix) != 4 or any(len(row) != 4 for row in matrix):
            raise ValueError("Invalid transformation matrix")
            
        # Convert point to homogeneous coordinates if needed
        if len(point) == 3:
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