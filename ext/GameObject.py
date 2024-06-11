from ext.Vector import Vector2, Cell
from ext.Event import Bindable, Event, Events
from typing import *

V = TypeVar("V", int, int) # Coords type

class Object(Generic[V], Bindable):
    def __init__(
        self,
        __id: V,
        __vector: Vector2,
        cells: list[Cell] = []
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
        # Init events
        self.bindedEvents = {event.name:event for event in [
            Event(Events.ON_BUTTON_PRESSED, _pass)
        ]}

    def move(
        self,
        __vector: Vector2
    ) -> None:
        # Cheack type
        if not isinstance(__vector, Vector2):
            raise TypeError("Type {0} not excepted for __vector".format(type(__vector)))
        # Change object vector
        self.vector = self.vector + __vector
        # Change cells vectors
        index = 0
        for cell in self.cells:
            cell: Cell = cell
            self.cells[index].vector = cell.vector + __vector
            index += 1

    def goto(
        self,
        __vector: Vector2
    ) -> None:
        # Cheack type
        if not isinstance(__vector, Vector2):
            raise TypeError("Type {0} not excepted for __vector".format(type(__vector)))
        # Change object vector
        self.vector = __vector
        # Change cells vectors
        index = 0
        for cell in self.cells:
            cell: Cell = cell
            self.cells[index].vector = __vector
            index += 1

def _pass(): pass