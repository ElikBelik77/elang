from typing import List


class Layer:
    pass


class HeapLayer(Layer):
    pass


class StackLayer(Layer):
    def __init__(self, size_expression):
        self.size_expression = size_expression
        if not size_expression.is_constant():
            raise Exception("Array stack declarations must have constant size")
        self.size = self.size_expression.evaluate()


class Array:
    def __init__(self, underlying_type, layers: List[Layer]):
        self.underlying_type = underlying_type
        self.layers = layers
