from typing import Callable

class Events():
    ON_BUTTON_PRESSED = "ON_BUTTON_PRESSED"

class Event():
    def __init__(
        self,
        eventName: str,
        func: callable
    ) -> None:
        if not isinstance(eventName, str):
            raise TypeError("Type {0} not excepted".format(type(eventName)))
        if not isinstance(func, Callable):
            raise TypeError("Type {0} not excepted".format(type(func)))
        
        self.name = eventName
        self.func = func

class Bindable():
    def bindEvent(
        self,
        eventName: str,
        func: callable
    ) -> Event:
        self.bindedEvents[eventName] = Event(eventName, func)