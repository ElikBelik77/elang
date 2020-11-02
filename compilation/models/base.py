from typing import List

from compilation.type_system.base import Type
from compilation.headers import CompileAsPointer
from compilation.models.modules import Export, Include


class Compilable:
    """
    Interface for unifying compilable models.
    """

    def get_mentions(self) -> List[str]:
        """
        This function returns the variable that are mentioned in the compilable.
        :return:
        """
        pass

    def convert_ptr_types(self, var_list):
        pass


class Scopeable(Compilable):
    """
    Interface for describing models that have their own scope
    """

    def __init__(self, scope: "Scope", body: List[Compilable]):
        self.scope = scope
        self.body = body
        self.convert_ptr_types()

    def get_mentions(self) -> List[str]:
        mentions = []
        for expression in self.body:
            mentions += expression.get_mentions()
        return mentions

    def convert_ptr_types(self, var_list=[]):
        pointer_variables = []
        for variable in self.scope.defined_variables:
            if issubclass(type(self.scope.defined_variables[variable]["type"]), CompileAsPointer):
                pointer_variables.append(variable)

        for statement in self.body:
            statement.convert_ptr_types(pointer_variables)


class Variable(Compilable):
    """
    Model for variable mentions
    """

    def __init__(self, name: str):
        self.name = name

    def is_constant(self):
        return False

    def get_mentions(self) -> List[str]:
        return [self.name]

    def to_ptr_type(self):
        return PointerVariable(self.name)

    def has_ptr_type(self):
        return False


class PointerVariable(Compilable):
    """
    Model for a variable that is a pointer type.
    """

    def __init__(self, name: str):
        self.name = name

    def is_constant(self):
        return False

    def get_mentions(self) -> List[str]:
        return [self.name]

    def has_ptr_type(self):
        return True


class UnaryOperator(Compilable):
    def __init__(self, obj: Compilable = None):
        self.obj = obj

    def get_precedence(self):
        pass

    def is_constant(self):
        pass

    def has_ptr_type(self):
        if isinstance(self.obj, PointerVariable):
            return True
        elif isinstance(self.obj, BinaryOperator) or isinstance(self.obj, UnaryOperator):
            return self.obj.has_ptr_type()
        return False


class BinaryOperator(Compilable):
    """
    Interface for unifying operators.
    """

    def __init__(self, left: Compilable = None, right: Compilable = None):
        self.left = left
        self.right = right

    def get_precedence(self):
        pass

    def is_constant(self):
        return self.left.is_constant() and self.right.is_constant()

    def convert_ptr_types(self, var_list):
        if isinstance(self.left, Variable) and self.left.name in var_list:
            self.left = self.left.to_ptr_type()
        elif isinstance(self.left, BinaryOperator) or isinstance(self.left, UnaryOperator):
            self.left.convert_ptr_types(var_list)
        if isinstance(self.right, Variable) and self.right.name in var_list:
            self.right = self.right.to_ptr_type()
        elif isinstance(self.right, BinaryOperator) or isinstance(self.right, UnaryOperator):
            self.right.convert_ptr_types(var_list)

    def has_ptr_type(self):
        if isinstance(self.left, PointerVariable) or isinstance(self.right, PointerVariable):
            return True
        elif (isinstance(self.left, BinaryOperator) or isinstance(self.left, UnaryOperator)
              and isinstance(self.right, BinaryOperator) or isinstance(self.right, UnaryOperator)):
            return self.right.has_ptr_type() or self.left.has_ptr_type()
        return False

    def get_mentions(self) -> List[str]:

        return self.left.get_mentions() + self.right.get_mentions()


class Scope:
    """
    Model for a scope
    """

    def __init__(self, name: str, parent_scope: "Scope"):
        self.parent_scope = parent_scope
        self.children: [Scope] = []
        if parent_scope is not None:
            self.parent_scope.children.append(self)
        self.defined_variables = {}
        self.defined_functions = {}
        self.name = name

    def get_children(self):
        """
        This function gets all of the children of the scope
        :return: list of all the child scopes of this scope
        """
        children = []
        for child in self.children:
            children += child.get_children()
        return children + self.children

    def get_global(self):
        if self.parent_scope is None:
            return self
        return self.parent_scope.get_global()

    def is_child_of(self, parent):
        """
        This function checks if this scope is a descendant of another scope.
        :param parent: the parent to check.
        :return: True if this scope is a descendant of the parent, false otherwise.
        """
        p = self.parent_scope
        while p is not None:
            if p == parent:
                return True
        return False

    def search_variable(self, name: str):
        if name in self.defined_variables:
            return self.defined_variables[name]
        if self.parent_scope is None:
            return None
        return self.parent_scope.search_variable(name)

    def search_function_scope(self, name: str):
        if name in self.defined_functions:
            return self
        if self.parent_scope is None:
            return None
        return self.parent_scope.search_function_scope(name)


class VariableDeclaration(Compilable):
    """
    Model for variable declaration
    """

    def __init__(self, name: str, var_type: Type):
        self.name = name
        self.var_type = var_type

    def get_mentions(self) -> List[str]:
        return [self.name]


class Function(Scopeable):
    """
    Model for functions
    """

    def __init__(self, scope: Scope, name: str, signature: str, return_type: str, body: List[Compilable],
                 arguments: List[VariableDeclaration]):
        super(Function, self).__init__(scope, body)
        self.name = name
        self.signature = signature
        self.return_type = return_type
        self.arguments = arguments


class ElangClass(Scopeable, CompileAsPointer, Type):
    """
    Class model for classes that are defined in a source code.
    """

    def __init__(self, name: str, scope: Scope, functions: List[Function], variables: List[VariableDeclaration],
                 variables_init: List[Compilable], sub_classes: List["ElangClass"]):
        super(ElangClass, self).__init__(scope, functions + variables)
        self.name = name
        self.functions = {}
        for function in functions:
            self.functions[function.name] = function

        self.constructor = None
        self.variables = {}
        for mv in variables:
            self.variables[mv.name] = mv.var_type
        self.variables_init = variables_init
        self.classes = {}
        for sub_class in sub_classes:
            self._add_class(sub_class)
        for f_name in self.functions:
            if f_name == "constructor":
                self.constructor = self.functions[f_name]
            self.functions[f_name].arguments.append(VariableDeclaration("this", self))
        scope.defined_variables["this"] = {"type": self}
        for mv in variables:
            scope.defined_variables[mv.name] = {"type": mv.var_type}
        for func in functions:
            scope.defined_functions[func.name] = func

    def _add_class(self, eclass: "ElangClass"):
        self.classes[eclass.name] = eclass
        for sub_class in eclass.classes:
            self._add_class(eclass.classes[sub_class])

    def get_size(self, size_bundle):
        return size_bundle["int"]

    def get_malloc_size(self, size_bundle):
        """
        This function returns the size of this class on the heap.
        :param size_bundle: the size bundle of the compiler.
        :return: the size of this class on heap allocation.
        """
        size = 0
        for mv in self.variables:
            size += self.variables[mv].get_size(size_bundle)
        return size

    def append_name(self, name):
        self.name = name + '.' + self.name
        for subclass in self.classes:
            self.classes[subclass].append_name(name)

    def update_names_for_prefix(self, prefix):
        self.name = prefix + '.' + self.name
        temp_classes = self.classes.copy()
        for sub_class in self.classes:
            self.classes[sub_class].update_names_for_prefix(prefix)
        self.classes = {}
        for t in temp_classes:
            self.classes[temp_classes[t].name] = temp_classes[t]


class Program(ElangClass):
    """
    Model for the entire program
    """

    def __init__(self, global_vars: List[VariableDeclaration], globals_init: List[Compilable],
                 functions: List[Function], classes: List[ElangClass],
                 exports: List[Export], includes: List[Include], name, global_scope):
        super(Program, self).__init__(name, global_scope, functions, global_vars, globals_init, classes)
        for eclass in classes:
            eclass.update_names_for_prefix(self.name)
        self.classes = {}
        for sub_class in classes:
            self._add_class(sub_class)
        self.exports = exports
        self.includes = includes
        self.convert_ptr_types()

    def resolve_exports(self) -> List[Compilable]:
        return [export.resolve(self) for export in self.exports]
