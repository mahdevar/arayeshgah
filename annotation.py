__all__ = ['Any', 'Class', 'Dictionary', 'Number', 'Serializable', 'String', 'TypeVar', 'Union']

from typing import Any, Callable, TypeVar, Union

Class = TypeVar('Class', bound=Callable)
Dictionary = dict
Number = float | int
Serializable = dict | float | int | str
String = str
