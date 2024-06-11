from __future__ import annotations
from typing import *

V = TypeVar("V", int, int)

class Vector2(Generic[V]):
    def __init__(
        self,
        __x: V = 0,
        __y: V = 0
    ) -> None:
        super().__init__()
        # Define in class
        self.x, self.y = __x, __y

    def __add__(
        self,
        __vector: Vector2[V, V]
    ) -> Vector2[V, V]:
        if not isinstance(__vector, Vector2):
            # Raise error
            raise TypeError("Type {0} not excepted".format(type(__vector)))
        return Vector2(self.x + __vector.x, self.y + __vector.y)
    
    def __radd__(
        self,
        __vector: Vector2[V, V]
    ) -> Vector2[V, V]:
        return self.__add__(__vector)
    
    def __lt__(
        self,
        __vector: Vector2[V, V]
    ) -> Vector2[V, V]:
        if not isinstance(__vector, Vector2):
            # Raise error
            raise TypeError("Type {0} not excepted".format(type(__vector)))
        return self.x < __vector.x and self.y < __vector.y
    
    def __gt__(
        self,
        __vector: Vector2[V, V]
    ) -> Vector2[V, V]:
        if not isinstance(__vector, Vector2):
            # Raise error
            raise TypeError("Type {0} not excepted".format(type(__vector)))
        return self.x > __vector.x and self.y > __vector.y
    
    @staticmethod
    def convertToVector(
        __list: list = []
    ) -> Vector2:
        if not isinstance(__list, list):
            raise TypeError("Type {0} not excepted".format(type(__list)))
        print(__list[0], __list[1])
        return Vector2(__list[0], __list[1])
    
class Cell():
    def __init__(
        self,
        __vector: Vector2 | list,
        symbol: str = ' '
    ) -> None:
        if not isinstance(__vector, Vector2):
            raise TypeError("Type {0} not excepted for __vector".format(type(__vector)))
        if isinstance(__vector, list):
            self.vector = Vector2.convertToVector(__vector)
        else:
            self.vector = __vector
        self.symbol = symbol
