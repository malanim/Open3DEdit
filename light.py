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