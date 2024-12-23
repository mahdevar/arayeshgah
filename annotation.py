__all__ = ['Any', 'Class', 'Dictionary', 'Number', 'String', 'TypeVar', 'Union']

from typing import Any, Callable, TypeVar, Union

Class = TypeVar('Class', bound=Callable)
Dictionary = dict
Number = float | int
String = str
