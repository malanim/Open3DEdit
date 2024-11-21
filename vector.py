import math

class Vector3:
    """Class representing a 3D vector with basic operations"""
    
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar):
        if scalar == 0:
            raise ValueError("Division by zero")
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def normalize(self):
        length = self.length()
        if length == 0:
            return Vector3()
        return self / length
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

class Matrix4:
    """Class representing a 4x4 matrix for 3D transformations"""
    
    def __init__(self):
        # Initialize as identity matrix
        self.data = [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ]
    
    @staticmethod
    def translation(x, y, z):
        m = Matrix4()
        m.data[0][3] = x
        m.data[1][3] = y
        m.data[2][3] = z
        return m
    
    @staticmethod
    def rotation_x(angle):
        m = Matrix4()
        c = math.cos(angle)
        s = math.sin(angle)
        m.data[1][1] = c
        m.data[1][2] = -s
        m.data[2][1] = s
        m.data[2][2] = c
        return m
    
    @staticmethod
    def rotation_y(angle):
        m = Matrix4()
        c = math.cos(angle)
        s = math.sin(angle)
        m.data[0][0] = c
        m.data[0][2] = s
        m.data[2][0] = -s
        m.data[2][2] = c
        return m
    
    @staticmethod
    def rotation_z(angle):
        m = Matrix4()
        c = math.cos(angle)
        s = math.sin(angle)
        m.data[0][0] = c
        m.data[0][1] = -s
        m.data[1][0] = s
        m.data[1][1] = c
        return m
    
    @staticmethod
    def scale(x, y, z):
        m = Matrix4()
        m.data[0][0] = x
        m.data[1][1] = y
        m.data[2][2] = z
        return m
    
    def __mul__(self, other):
        result = Matrix4()
        for i in range(4):
            for j in range(4):
                result.data[i][j] = sum(
                    self.data[i][k] * other.data[k][j] for k in range(4)
                )
        return result