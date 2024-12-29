__all__ = ['Any', 'Bool', 'Class', 'Dictionary', 'List', 'Number', 'Parameter', 'Serializable', 'String', 'TypeVar']

from typing import Any, Callable, TypeVar

from click import Parameter

Bool = bool
Class = TypeVar('Class', bound=Callable)
Dictionary = dict
List = list
Number = float | int
Parameter = list | tuple | None
Serializable = dict | float | int | str
String = str
