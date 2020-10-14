from typing import List


class Layer:
    pass


class HeapLayer(Layer):
    pass


class StackLayer(Layer):
    def __init__(self, size_expression):
        self.size_expression = size_expression


class Array:
    def __init__(self, underlying_type, layers: List[Layer]):
        self.underlying_type = underlying_type
        self.layers = layers
