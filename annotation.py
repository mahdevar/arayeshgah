__all__ = ['Class', 'Dictionary', 'Number', 'String', 'TypeVar']

from typing import Callable, TypeVar

Class = TypeVar('Class', bound=Callable)
Dictionary = dict
Number = float
String = str
