from typing import List, Tuple, Union
import math

class Camera:
    """Camera class for 3D scene viewing and projection"""
    
    def __init__(self, 
                 position: Tuple[float, float, float]=(0, 0, -10),
                 target: Tuple[float, float, float]=(0, 0, 0),
                 up: Tuple[float, float, float]=(0, 1, 0),
                 fov: float=60.0,
                 aspect: float=16/9,
                 near: float=0.1,
                 far: float=100.0):
        """Initialize camera with position and viewing parameters
        
        Args:
            position: Camera position in world space
            target: Point the camera is looking at
            up: Up vector for camera orientation
            fov: Field of view in degrees
            aspect: Aspect ratio (width/height)
            near: Near clipping plane distance
            far: Far clipping plane distance
        """
        self.position = list(position)
        self.target = list(target)
        self.up = list(up)
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far

    def get_projection_matrix(self) -> List[List[float]]:
        """Получение матрицы проекции
        
        Создает матрицу перспективной проекции на основе параметров камеры:
        - поля зрения (fov) - угол обзора камеры в градусах
        - соотношения сторон (aspect) - отношение ширины к высоте viewport
        - ближней и дальней плоскостей отсечения (near, far) - границы видимого пространства
        
        Матрица проекции преобразует координаты из пространства камеры
        в нормализованные координаты устройства (NDC).
        
        Returns:
            List[List[float]]: Матрица проекции 4x4
        """
        f = 1.0 / math.tan(math.radians(self.fov) / 2.0)
        
        # Build perspective projection matrix
        projection = [
            [f/self.aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (self.far + self.near)/(self.near - self.far), -1],
            [0, 0, (2*self.far*self.near)/(self.near - self.far), 0]
        ]
        
        return projection

    def get_view_matrix(self) -> List[List[float]]:
        """Получение матрицы вида
        
        Создает матрицу преобразования вида на основе:
        - позиции камеры
        - точки наблюдения
        - вектора "вверх"
        
        Матрица используется для преобразования координат из мировой системы
        в систему координат камеры.
        
        Returns:
            List[List[float]]: Матрица вида 4x4
        """
        # Calculate forward vector (z-axis)
        forward = [
            self.target[0] - self.position[0],
            self.target[1] - self.position[1],
            self.target[2] - self.position[2]
        ]
        # Normalize forward vector
        length = math.sqrt(sum(x*x for x in forward))
        if length < 1e-7:  # Prevent division by zero
            forward = [0, 0, 1]
        else:
            forward = [x/length for x in forward]
        
        # Calculate right vector (x-axis) as cross product of forward and up
        right = [
            forward[1] * self.up[2] - forward[2] * self.up[1],
            forward[2] * self.up[0] - forward[0] * self.up[2],
            forward[0] * self.up[1] - forward[1] * self.up[0]
        ]
        # Normalize right vector
        length = math.sqrt(sum(x*x for x in right))
        if length > 0:
            right = [x/length for x in right]
        else:
            right = [1, 0, 0]
            
        # Calculate new up vector (y-axis) as cross product of right and forward
        up = [
            right[1] * forward[2] - right[2] * forward[1],
            right[2] * forward[0] - right[0] * forward[2],
            right[0] * forward[1] - right[1] * forward[0]
        ]
        
        # Build view matrix
        view = [
            [right[0], right[1], right[2], -sum(right[i] * self.position[i] for i in range(3))],
            [up[0], up[1], up[2], -sum(up[i] * self.position[i] for i in range(3))],
            [-forward[0], -forward[1], -forward[2], sum(forward[i] * self.position[i] for i in range(3))],
            [0, 0, 0, 1]
        ]
        
        return view

    def move(self, x: float, y: float, z: float) -> None:
        """Move the camera by the given offsets"""
        self.position[0] += x
        self.position[1] += y
        self.position[2] += z
        # Update target position relative to camera movement
        self.target[0] += x
        self.target[1] += y
        self.target[2] += z
        
    def update(self, delta_time: float) -> None:
        """Update camera state"""
        # Could add camera interpolation, animation or other time-based updates here
        pass