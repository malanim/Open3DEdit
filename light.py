from vector import Vector3

class Light:
    """Базовый класс для источников света
    
    Определяет основные параметры источника света:
    - позицию в пространстве
    - интенсивность освещения
    - цвет источника света
    """
    
    def __init__(self, position: Vector3 = None, intensity: float = 1.0, color: str = "#FFFFFF"):
        """Инициализация источника света
        
        Args:
            position: Позиция источника света в пространстве
            intensity: Интенсивность света (от 0.0 до 1.0)
            color: Цвет света в формате HEX (#RRGGBB)
        """
        self.position = position or Vector3()
        self.intensity = intensity
        self.color = color
        
    def get_direction(self, point: Vector3) -> Vector3:
        """Get light direction at given point
        
        Args:
            point: Point to calculate light direction for
            
        Returns:
            Normalized direction vector from point to light
        """
        direction = Vector3(
            self.position.x - point[0],
            self.position.y - point[1], 
            self.position.z - point[2]
        )
        direction.normalize()
        return direction
        
    def get_intensity(self, point: Vector3) -> float:
        """Get light intensity at given point
        
        Args:
            point: Point to calculate intensity for
            
        Returns:
            Light intensity value between 0.0 and 1.0
        """
        return self.intensity

class DirectionalLight(Light):
    """Направленный источник света
    
    Источник света, испускающий параллельные лучи в заданном направлении.
    Используется для имитации солнечного света или других удаленных источников.
    """
    
    def __init__(self, direction: Vector3 = None, intensity: float = 1.0):
        """Инициализация направленного источника света
        
        Args:
            direction: Вектор направления света
            intensity: Интенсивность света (от 0.0 до 1.0)
        """
        super().__init__(None, intensity)
        self.direction = direction or Vector3(0, -1, 0)
        self.direction.normalize()
        
    def get_direction(self, point: Vector3) -> Vector3:
        """Get light direction (constant for directional light)"""
        return self.direction
        
    def get_intensity(self, point: Vector3) -> float:
        """Get light intensity (constant for directional light)"""
        return self.intensity

    def get_direction(self, position: Vector3) -> Vector3:
        """Get normalized light direction at given position
        
        Args:
            position: Position to calculate light direction for
            
        Returns:
            Vector3: Normalized light direction vector
        """
        return self.direction

    def get_intensity(self, position: Vector3) -> float:
        """Get light intensity at given position
        
        Args:
            position: Position to calculate intensity for
            
        Returns:
            float: Light intensity in range [0,1]
        """
        return self.intensity