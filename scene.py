from typing import List, Optional

class Scene:
    """Класс для управления объектами в 3D сцене"""
    
    def __init__(self):
        self.objects = []
        self.lights = []
        
    def add_object(self, obj) -> None:
        """Добавление объекта в сцену"""
        self.objects.append(obj)
        
    def remove_object(self, obj) -> None:
        """Удаление объекта из сцены"""
        if obj in self.objects:
            self.objects.remove(obj)
            
    def add_light(self, light) -> None:
        """Добавление источника света"""
        if light not in self.lights:
            self.lights.append(light)
            
    def remove_light(self, light) -> None:
        """Удаление источника света"""
        if light in self.lights:
            self.lights.remove(light)
            
    def get_lights(self) -> List:
        """Получение списка всех источников света"""
        return self.lights
        
    def update(self, delta_time: float) -> None:
        """Обновление состояния сцены"""
        for obj in self.objects:
            if hasattr(obj, 'update'):
                obj.update(delta_time)
                
    def get_objects(self) -> List:
        """Получение списка всех объектов"""
        return self.objects