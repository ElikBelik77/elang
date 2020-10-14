from typing import List, Dict


class Layer:
    def get_size(self) -> int:
        pass


class HeapLayer(Layer):
    def get_size(self):
        return 4


class StackLayer(Layer):
    def __init__(self, size_expression):
        self.size_expression = size_expression
        if not size_expression.is_constant():
            raise Exception("Array stack declarations must have constant size")
        self.size = self.size_expression.evaluate()

    def get_size(self):
        return self.size


class Array:
    def __init__(self, underlying_type, layers: List[Layer]):
        self.underlying_type = underlying_type
        self.layers = layers

    def get_size(self, bundle: Dict):
        base_size = self.layers[-1].get_size() * bundle[self.underlying_type.name] + 2 * bundle["int"]
        stack_size = base_size
        for idx, layer in enumerate(self.layers[:-1][::-1]):
            if not isinstance(layer, StackLayer):
                continue
            stack_size = bundle["int"] * 2 + layer.size * stack_size
        return stack_size

    def get_metadata(self, bundle: Dict):
        metadata = [
            {"array_size": self.layers[-1].get_size(), "cell_size": bundle[self.underlying_type.name], "offsets": [0]}]
        base_size = self.layers[-1].get_size() * bundle[self.underlying_type.name] + 2 * bundle["int"]
        stack_size = base_size
        for idx, layer in enumerate(self.layers[:-1][::-1]):
            if not isinstance(layer, StackLayer):
                continue
            metadata.append({"array_size": layer.get_size(), "cell_size": stack_size})
            stack_size = bundle["int"] * 2 + layer.size * stack_size
        metadata = metadata[::-1]
        metadata[0]["offsets"] = [0]
        for idx, layer in enumerate(self.layers[1::]):
            header_size = 2 * bundle["int"]
            metadata[idx + 1]["offsets"] = []  # current metadata, attention enumerate starts from second element.
            for offset in metadata[idx]["offsets"]:
                for cell in range(0, metadata[idx]["array_size"]):
                    metadata[idx + 1]["offsets"].append(offset + header_size + cell * metadata[idx]["cell_size"])
        return metadata