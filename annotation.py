__all__ = ['Any', 'Bool', 'Class', 'Dictionary', 'Generator', 'Number', 'Serializable', 'String', 'TypeVar', 'Union']

from typing import Any, Callable, Generator, TypeVar, Union

Bool = bool
Class = TypeVar('Class', bound=Callable)
Dictionary = dict
Number = float | int
Serializable = dict | float | int | str
String = str
