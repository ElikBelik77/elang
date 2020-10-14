from typing import List

from compilation.models.base import Compilable
from compilation.type_system.arrays import Array


class ArrayInitializer(Compilable):
    def __init__(self, array: Array, variable_name):
        self.array = array
        self.variable_name = variable_name

    def get_mentions(self) -> List[str]:
        return []
