import uuid
from typing import Tuple, Dict, List

from compilation.headers import CompileAsPointer
from compilation.models.base import Scopeable, Function
from compilation.models.classes import ElangClass
from compilation.type_system.primitives import Primitive


def get_unique_id() -> str:
    """
    This function returns a unique id for loc jumping.
    :return: a unique string id
    """
    return uuid.uuid4().hex[:6].upper()


def produce_offset_table(scopeable: Scopeable, size_bundle: Dict) -> Tuple[Dict[str, int], int]:
    """
    This function produces an offset table for a scope.
    :param size_bundle: the bundle of type sizes.
    :param scopeable: the scope.
    :return: a dictionary that matches a variable (or argument) name, to it's offset in relation to ebp.
    """
    scope_table: Dict[str, int] = {}

    arguments_size = 12
    if isinstance(scopeable, Function):
        for idx, arg in enumerate(scopeable.arguments):
            if issubclass(type(arg.var_type), CompileAsPointer):
                scope_table[arg.name] = arguments_size + idx * size_bundle["int"]
                arguments_size += idx * size_bundle["int"]
            elif isinstance(type(arg.var_type), Primitive):
                scope_table[arg.name] = arguments_size + idx * arg.var_type.get_size(size_bundle)
                arguments_size += idx * size_bundle[arg.var_type.get_size(size_bundle)]

    scopes: List[Scopeable] = [scopeable]
    stack_size = 0
    while len(scopes) is not 0:
        current_scope = scopes.pop()
        for idx, key in enumerate(current_scope.scope.defined_variables):
            scope_table[key] = stack_size
            stack_size = scope_table[key] - current_scope.scope.defined_variables[key]["type"].get_size(size_bundle)
        for compilable in current_scope.body:
            if issubclass(type(compilable), Scopeable):
                scopes.append(compilable)
    return scope_table, abs(stack_size)


def produce_class_vtable(elang_class: ElangClass, size_bundle: Dict) -> Dict:
    table_size = size_bundle["int"] * (len(elang_class.member_variables) + len(elang_class.functions))
    vtable = {"table_size": table_size}
    vtable_current_size = size_bundle["int"]
    for variable in elang_class.member_variables:
        vtable[variable.name] = vtable_current_size
        vtable_current_size += variable.var_type.get_size(size_bundle)
    for functions in elang_class.functions:
        pass
    return vtable


def produce_class_member_offset_table(elang_class: ElangClass, size_bundle: Dict) -> Dict[str, int]:
    table_size = size_bundle["int"] * (len(elang_class.member_variables) + len(elang_class.functions))
    vtable_current_size = 0
    vtable: Dict = {}
    for variable in elang_class.member_variables:
        vtable[variable.name] = vtable_current_size
        vtable_current_size += variable.var_type.get_size(size_bundle)
    for functions in elang_class.functions:
        pass
    return vtable
