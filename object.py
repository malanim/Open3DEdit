from typing import List, Tuple
from vector import Vector3, Matrix4

class Object3D:
    """Base class for 3D objects"""
    
    def __init__(self, vertices: List[Vector3] = None, faces: List[Tuple[int, ...]] = None, color: str = "#FFFFFF"):
        self.vertices = vertices or []
        self.faces = faces or []
        self.position = Vector3()
        self.rotation = Vector3()
        self.scale = Vector3(1.0, 1.0, 1.0)
        self.color = color
        self.ambient = 0.1  # коэффициент фонового освещения
        self.diffuse = 0.7  # коэффициент диффузного отражения
        self.specular = 0.3  # коэффициент зеркального отражения
        
    def transform(self) -> Matrix4:
        """Get complete transformation matrix"""
        translation = Matrix4.translation(self.position.x, self.position.y, self.position.z)
        rotation_x = Matrix4.rotation_x(self.rotation.x)
        rotation_y = Matrix4.rotation_y(self.rotation.y)
        rotation_z = Matrix4.rotation_z(self.rotation.z)
        scale = Matrix4.scale(self.scale.x, self.scale.y, self.scale.z)
        
        return translation * rotation_z * rotation_y * rotation_x * scale
        
    def get_transformed_vertices(self) -> List[Vector3]:
        """Get vertices after transformation"""
        transform = self.transform()
        return [transform * vertex for vertex in self.vertices]

    def translate(self, x: float, y: float, z: float) -> None:
        """Translate object by given amounts"""
        self.position.x += x
        self.position.y += y
        self.position.z += z

    def rotate(self, x: float, y: float, z: float) -> None:
        """Rotate object by given angles"""
        self.rotation.x += x
        self.rotation.y += y
        self.rotation.z += z

    def set_scale(self, x: float, y: float, z: float) -> None:
        """Set absolute scale values"""
        self.scale.x = x
        self.scale.y = y
        self.scale.z = z

class Cube(Object3D):
    """Basic cube object"""
    
    def __init__(self, size: float = 1.0):
        # Define 8 vertices of a cube
        half = size / 2
        vertices = [
            Vector3(-half, -half, -half),  # 0: front bottom left
            Vector3(half, -half, -half),   # 1: front bottom right
            Vector3(half, half, -half),    # 2: front top right
            Vector3(-half, half, -half),   # 3: front top left
            Vector3(-half, -half, half),   # 4: back bottom left
            Vector3(half, -half, half),    # 5: back bottom right
            Vector3(half, half, half),     # 6: back top right
            Vector3(-half, half, half),    # 7: back top left
        ]
        
        # Define faces as vertex indices
        faces = [
            (0, 1, 2, 3),  # front
            (5, 4, 7, 6),  # back
            (4, 0, 3, 7),  # left
            (1, 5, 6, 2),  # right
            (3, 2, 6, 7),  # top
            (4, 5, 1, 0),  # bottom
        ]
        
        super().__init__(vertices, faces)

class Plane(Object3D):
    """Basic plane object"""
    
    def __init__(self, width: float = 1.0, height: float = 1.0):
        half_w = width / 2
        half_h = height / 2
        
        vertices = [
            Vector3(-half_w, 0, -half_h),
            Vector3(half_w, 0, -half_h),
            Vector3(half_w, 0, half_h),
            Vector3(-half_w, 0, half_h),
        ]
        
        faces = [(0, 1, 2, 3)]
        
        super().__init__(vertices, faces)