# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TypeVar, Generic
import abc
import threading
import ext.Errors as Errors
from ext.Vector import Vector2, Cell
from ext.Event import Events, Event, Bindable
from ext.GameObject import Object

V = TypeVar("V", int, int) # Coords type

class Symbols():
    EMPTY  = ' '
    BORDER = '█'
    PLAYER = '●'

class Screen(Generic[V], Bindable):
    def __init__(
        self,
        width: V,
        height: V
    ) -> None:
        # Check type
        if not isinstance(width, int):
            raise TypeError("Type {0} not excepted".format(type(width)))
        if not isinstance(height, int):
            raise TypeError("Type {0} not excepted".format(type(height)))

        self.width = width
        self.height = height
        # Generate pole
        self.pole: list[list] = []
        for row in range(0, self.height):
            self.pole.append([])
            for column in range(0, self.width):
                self.pole[row].append(Cell(Vector2(row, column), Symbols.EMPTY))
        # Events
        self.bindedEvents = {event.name:event for event in [
            Event(Events.ON_BUTTON_PRESSED, _pass)
        ]}

    def generateNewPole(self) -> list[list]:
        self.pole: list[list] = []
        for row in range(0, self.height):
            self.pole.append([])
            for column in range(0, self.width):
                self.pole[row].append(Cell(Vector2(row, column), Symbols.EMPTY))
        return self.pole

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
        self,
        pole: list[list]
    ) -> None:
        poleStr = ''
        for row in pole:
            rowStr = ''
            for cell in row:
                cell: Cell = cell
                rowStr = rowStr + cell.symbol
            poleStr = poleStr + rowStr + '\n'
        print(poleStr)

    @staticmethod
    def clear() -> None:
        print("\033[H\033[J", end="")

    def update(
        self
    ) -> None:
        Screen.clear()

class GameLoop():
    def __init__(
        self,
        screen: Screen,
        fps: V = 60,
    ) -> None:
        if not isinstance(screen, Screen):
            raise TypeError("Type {0} not excepted for screen".format(type(screen)))
        if not isinstance(fps, int):
            raise TypeError("Type {0} not excepted for fps".format(type(fps)))
        
        self.screen = screen
        self.fps = fps
        self.objects: dict[str, Object] = {}
        # Set run var
        self.running = False

    def run(self) -> None:
        self.gameThread = threading.Thread(target=self.updating, args=[self])
        # Set run var
        self.running = True
        self.gameThread.start()
    
    def stop(self) -> None:
        self.running = False
        self.gameThread.stop()

    @abc.abstractclassmethod
    def updating(
        gameLoop: GameLoop
    ) -> None:
        raise TypeError("Redefine self.updating")

    def redraw(
        self,
        objects: dict[str, Object]
    ) -> None:
        pole = self.screen.generateNewPole()
        for [__id, __object] in objects.items():
            __object: Object = __object
            __id: str = __id
            # Get __object cells
            for cell in __object.cells:
                cell: Cell = cell
                pole[-cell.vector.y][-cell.vector.x]: Cell = cell
        self.screen.printScreen(pole)

    def add(
        self,
        __object: Object
    ) -> Object:
        if not isinstance(__object, Object):
            raise TypeError("Type {0} not excepted".format(type(__object)))
        self.objects[__object.id] = __object
        return __object
    
    def addObject(
        self,
        __id: V,
        __vector: Vector2,
        cells: list[Cell] = []
    ) -> Object:
        self.objects[__id] = Object(__id, __vector, cells=cells)
        return Object(__id, __vector, cells=cells)
    
    def removeObject(
        self,
        __id: str
    ) -> Object:
        return self.objects.pop(__id)
    
def _pass(): pass