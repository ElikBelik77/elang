import uuid
from typing import Tuple, Dict, List

from compilation.headers import CompileAsPointer
from compilation.models.base import Scopeable, Function, BinaryOperator, ElangClass
from compilation.type_system.primitives import Primitive
from compilation.models.operators import DotOperator


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
            scope_table[key] = stack_size - current_scope.scope.defined_variables[key]["type"].get_size(size_bundle)
            stack_size = scope_table[key]
        for compilable in current_scope.body:
            if issubclass(type(compilable), Scopeable):
                scopes.append(compilable)
    return scope_table, abs(stack_size)


def produce_class_vtable(elang_class: ElangClass, size_bundle: Dict) -> Dict:
    """
    This function produces a vtable for a class.
    :param elang_class: the class.
    :param size_bundle: the size bundle of the compiler.
    :return: a vtable for the class.
    """
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
    """
    This function produces a member variable offset table for a given elang class.
    :param elang_class: the elang class.
    :param size_bundle: the size bundle of the compiler.
    :return: a member variable offset table.
    """
    vtable_current_size = 0
    vtable: Dict = {}
    for variable in elang_class.member_variables:
        vtable[variable.name] = vtable_current_size
        vtable_current_size += variable.var_type.get_size(size_bundle)
    for functions in elang_class.functions:
        pass
    return vtable


def unpack_dot_operator(expression: BinaryOperator):
    """
    This function unpacks a dot ('.') operator. the innermost (rightest) dot is returned first, the last (leftmost) dot is returned first
    :param expression: the dot expression to unpack.
    :return: yields the dot operators by the order described above.
    """
    current = expression
    produced = None
    first = True
    q = []
    while len(q) is not 0 or first:
        if isinstance(current, DotOperator):
            q.append((current.left, current))
            current = current.left
            first = False
        else:
            previous_left, previous = q.pop()
            yield previous
