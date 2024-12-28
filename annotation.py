__all__ = ['Any', 'Bool', 'Class', 'Dictionary', 'List', 'Number', 'Serializable', 'String', 'TypeVar']

from typing import Any, Callable, TypeVar

Bool = bool
Class = TypeVar('Class', bound=Callable)
Dictionary = dict
List = list
Number = float | int
Serializable = dict | float | int | str
String = str
