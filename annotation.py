__all__ = ['Any', 'Class', 'Dictionary', 'Number', 'String', 'TypeVar']

from typing import Any, Callable, TypeVar

Class = TypeVar('Class', bound=Callable)
Dictionary = dict
Number = float | int
String = str
