from typing import Dict


class Type:
    def __init__(self, name):
        self.name = name

    def get_size(self, size_bundle: Dict):
        pass


class PointerType(Type):
    """
    Interface for identifying a pointer type.
    """
    pass
