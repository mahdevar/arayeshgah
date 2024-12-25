__all__ = ['Any', 'Bool', 'Class', 'Dictionary', 'Generator', 'List', 'Number', 'Serializable', 'String', 'TypeVar']

from typing import Any, Callable, Generator, TypeVar

Bool = bool
Class = TypeVar('Class', bound=Callable)
Dictionary = dict
List = list
Number = float | int
Serializable = dict | float | int | str
String = str
