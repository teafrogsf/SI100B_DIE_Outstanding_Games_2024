import math
from typing import Any

from functools import total_ordering

@total_ordering
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
    
    def __eq__(self,other):
        return self.x == other.x and self.y == other.y
    def __ne__(self,other):
        return self.x != other.x or self.y != other.y
    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        raise ValueError("Operand must be a Vector2")
    
    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        raise ValueError("Operand must be a Vector2")

    def dot(self, other):
        if isinstance(other, Vector2):
            return self.x * other.x + self.y * other.y
        raise ValueError("Operand must be a Vector2")

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        length = self.length()
        if length == 0:
            raise ValueError("Cannot normalize zero vector")
        return Vector2(self.x / length, self.y / length)
    
    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector2(self.x * scalar, self.y * scalar)
        elif isinstance(scalar, Vector2):
            return Vector2(self.x * scalar.x, self.y * scalar.y)
        raise ValueError("Operand must be a scalar (int or float)")

    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            if scalar == 0:
                raise ValueError("Cannot divide by zero")
            return Vector2(self.x / scalar, self.y / scalar)
        raise ValueError("Operand must be a scalar (int or float)")
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self
    
    def __hash__(self):
        return hash((self.x,self.y))
    
    @staticmethod
    def Zero():
        return Vector2(0,0)
    @staticmethod
    def One():
        return Vector2(1,1)
    @staticmethod
    def Copy(vec):
        if Vector2.Is(vec):
            return Vector2(vec.x,vec.y)
        raise ValueError("Operand must be a scalar (int or float)")
    @staticmethod
    def Is(vec):
        return isinstance(vec, Vector2)