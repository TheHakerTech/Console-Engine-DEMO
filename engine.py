# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TypeVar, Generic
from rich.console import Console
import threading
import time
import utils.Errors as Errors

V = TypeVar("V", int, int) # Coords type
console = Console() # Colored text

class Symbols():
    EMPTY = ' '
    F = '&'

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
        return Vector2(*[(x1 + x2, y1 + y2) for [x1, y1, x2, y2] in [self.x, self.y, __vector.x, __vector.x]])
    
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

class Screen(Generic[V]):
    def __init__(
        self,
        __vector1: Vector2 | list[V, V] = Vector2(),
        __vector2: Vector2 | list[V, V] = Vector2()
    ) -> None:
        # Define in class
        if self.validateVectors(__vector1, __vector2):
            self.vector1, self.vector2 = __vector1, __vector2
        else:
            raise TypeError("Vector __vector1 < __vector2 (error)")

        # Generate pole
        self.pole: list[list] = []
        for row in range(0, self.vector1.y - __vector2.y):
            self.pole.append([])
            for column in range(0, self.vector1.x - __vector2.x):
                self.pole[row].append(Cell(Vector2(row, column), Symbols.EMPTY))

    def validateVectors(
        self,
        __vector1: Vector2 | Vector2(),
        __vector2: Vector2 | Vector2()
    ) -> list[Vector2[V, V], Vector2[V, V]]:
        # Check isinstance
        if not isinstance(__vector1, Vector2) and not isinstance(__vector1, list):
            # Raise error
            raise TypeError("Type {0} not excepted".format(type(__vector1)))
        elif not isinstance(__vector2, Vector2) and not isinstance(__vector2, list):
            # Raise error
            raise TypeError("Type {0} not excepted".format(type(__vector2)))
        
        if isinstance(__vector1, list):
            __vector1 = Vector2(*__vector1)
        if isinstance(__vector2, list):
            __vector2 = Vector2(*__vector1)
        # If vector1 > vector2
        if __vector1 > __vector2:
            return True
        else:
            return False    

    def printScreen(
        self
    ) -> None:
        for row in self.pole:
            for cell in row:
                cell: Cell = cell
                print(cell.symbol, end='')
            print(end="\n")

    @staticmethod
    def clear() -> None:
        print("\033[H\033[J", end="")

    def update(
        self
    ) -> None:
        Screen.clear()
        self.printScreen()

class Cell():
    def __init__(
        self,
        __vector: Vector2 | list,
        symbol: str = Symbols.EMPTY
    ) -> None:
        if not isinstance(__vector, Vector2):
            raise TypeError("Type {0} not excepted for __vector".format(type(__vector)))
        if isinstance(__vector, list):
            self.vector = Vector2.convertToVector(__vector)
        else:
            self.vector = __vector
        self.symbol = symbol

class Object():
    def __init__(
        self,
        __id: V,
        __vector: Vector2,
        cells: list[Cell]
    ) -> None:
        self.id = __id
        if not isinstance(__vector, Vector2):
            raise TypeError("Type {0} not excepted for __vector".format(type(__vector)))
        if isinstance(__vector, list):
            self.vector = Vector2.convertToVector(__vector)
        else:
            self.vector = __vector
        
        if not isinstance(cells, list):
            raise TypeError("Type {0} not excepted for cells".format(type(__vector)))
        self.cells = cells

class GameLoop():
    def __init__(
        self,
        screen: Screen,
        fps: V = 60,
        objects: list[Object] = []
    ) -> None:
        if not isinstance(screen, Screen):
            raise TypeError("Type {0} not excepted for screen".format(type(screen)))
        if not isinstance(fps, int):
            raise TypeError("Type {0} not excepted for fps".format(type(fps)))
        
        if not isinstance(objects, list):
            raise TypeError("Type {0} not excepted for fps".format(type(objects)))
        
        self.screen  = screen
        self.fps     = fps
        self.objects: list[Object] = objects
        # Set run var
        self.running = False

    def run(self) -> None:
        self.runThread = threading.Thread(target=self.__run)
        # Set run var
        self.running = True
        self.runThread.start()
    
    def stop(self) -> None:
        self.running = False

    def __run(self) -> None:
        tick = 1 / self.fps
        while self.running:
            self.redraw(self.objects)
            time.sleep(tick)

    def redraw(
        self,
        objects: list[Object]
    ) -> None:
        for __object in objects:
            __object: Object = __object
            # Get __object cells
            for cell in __object.cells:
                cell: Cell = cell
                # Change screen.pole
                self.screen.pole[-cell.vector.y][-cell.vector.x]: Cell = cell
                self.screen.printScreen()
                Screen.clear()

    def addObject(
        self,
        __object: Object
    ) -> Object:
        if not isinstance(__object, Object):
            raise TypeError("Type {0} not excepted for __object".format(type(__object)))
        self.objects.append(__object)
        return __object
    
    def addObjects(
        self,
        __objects: list[Object]
    ) -> Object:
        if not isinstance(__objects, list):
            raise TypeError("Type {0} not excepted for __objects".format(type(__objects)))
        self.objects.extend(__objects)
        return __objects
    
    def getObject(
        self,
        __id: str
    ) -> Object:
        if not isinstance(__id, str):
            raise TypeError("Type {0} not excepted for __id".format(type(__id)))
        
        for __object in self.objects:
            __object: Object = __object
            if __object.id == __id:
                return __object
        raise Errors.UnknownObjectID("Unknown object id: {0}".format(__id))
    
    def removeObject(
        self,
        __id: str
    ) -> Object:
        if not isinstance(__id, str):
            raise TypeError("Type {0} not excepted for __id".format(type(__id)))
        
        index = 0
        for __object in self.objects:
            __object: Object = __object
            if __object.id == __id:
                del self.objects[index]
            index += 1

    def move(
        self,
        __id: str,
        vector: Vector2
    ) -> None:
        if not isinstance(__id, str):
            raise TypeError("Type {0} not excepted for __id".format(type(__id)))
        if not isinstance(vector, Vector2):
            raise TypeError("Type {0} not excepted for vector".format(type(vector)))

        __object: Object = self.getObject(__id)
        __object.vector = __object.vector + vector

        index = 0
        cellsCopy = __object.cells.copy()
        for cell in __object.cells:
            cell: Cell = cell
            __object.cells[index] = cell.vector + vector
        self.removeObject(__object.id)
        self.addObject(__object)