from vector import Vector3

class Light:
    """Базовый класс для источников света"""
    
    def __init__(self, position: Vector3 = None, intensity: float = 1.0, color: str = "#FFFFFF"):
        self.position = position or Vector3()
        self.intensity = intensity
        self.color = color

class DirectionalLight(Light):
    """Направленный источник света"""
    
    def __init__(self, direction: Vector3 = None, intensity: float = 1.0):
        super().__init__(None, intensity)
        self.direction = direction or Vector3(0, -1, 0)
        self.direction.normalize()
