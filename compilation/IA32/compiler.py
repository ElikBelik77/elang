from typing import Tuple

from compilation.IA32.template_factories import *
from type_system.primitives import Primitive


class ProgramCompiler:
    """
    Compiler for the ELANG language.
    """

    @staticmethod
    def create_default() -> "ProgramCompiler":
        """
        Creates a default compiler.
        :return: an elang compiler.
        """
        return ProgramCompiler({
            Function: FunctionTemplateFactory(),
            MultiplicationOperator: MultiplyTemplateFactory(),
            SubtractOperator: SubtractionTemplateFactory(),
            AdditionOperator: AdditionTemplateFactory(),
            DivisionOperator: DivisionTemplateFactory(),
            ArrayIndexer: ArrayIndexerTemplateFactory(),
            Assignment: AssignmentTemplateFactory(),
            DecimalConstantValue: DecimalConstantTemplateFactory(),
            Variable: VariableTemplateFactory(),
            PointerVariable: PointerVariableTemplateFactory(),
            Return: ReturnTemplateFactory(),
            FunctionCall: FunctionCallTemplateFactory(),
            Equal: LogicalEqualTemplateFactory(),
            LogicalGreater: LogicalGreaterTemplateFactory(),
            LogicalAnd: LogicalAndTemplateFactory(),
            LogicalOr: LogicalOrTemplateFactory(),
            If: IfTemplateFactory(),
            While: WhileTemplateFactory(),
            ArrayInitializer: ArrayInitializeTemplateFactory()
        })

    def __init__(self, factories: Dict[type, TemplateFactory], verbose: bool = True) -> None:
        self.factories = factories
        self.size_bundle = {
            "int": 4
        }
        self.verbose = True

    def compile(self, program: Program, destination_file: str) -> None:
        """
        This function compiles a program.
        :param program: the program to compile.
        :param destination_file: the destination path to write the output to.
        :return: None.
        """
        assembly = ("SECTION .text\n"
                    "global main\n")
        for function in program.functions:
            assembly += self.compile_function(function) + "\n"
        with open(destination_file, "w") as out:
            out.write(assembly)

    def compile_function(self, function) -> str:
        """
        This function compiles a single function.
        :param function: the function to compile.
        :param offset_table: the offset table of the function.
        :return: the assembly code of the function.
        """
        offset_table, stack_size = self.produce_offset_table(function)
        return self.factories[Function].produce(function, self.factories,
                                                {"stack_size": stack_size, "offset_table": offset_table,
                                                 "parent": 'global', "size_bundle": self.size_bundle,
                                                 "verbose": self.verbose})

    def produce_offset_table(self, scopeable: Scopeable) -> Tuple[Dict[str, int], int]:
        """
        This function produces an offset table for a scope.
        :param scopeable: the scope.
        :return: a dictionary that matches a variable (or argument) name, to it's offset in relation to ebp.
        """
        scope_table: Dict[str, int] = {}

        arguments_size = 12
        if isinstance(scopeable, Function):
            for idx, arg in enumerate(scopeable.arguments):
                if issubclass(type(arg.var_type), CompileAsPointer):
                    scope_table[arg.name] = arguments_size + idx * self.size_bundle["int"]
                    arguments_size += idx * self.size_bundle["int"]
                elif isinstance(type(arg.var_type), Primitive):
                    scope_table[arg.name] = arguments_size + idx * arg.var_type.get_size(self.size_bundle)
                    arguments_size += idx * self.size_bundle[arg.var_type.get_size(self.size_bundle)]

        scopes: List[Scopeable] = [scopeable]
        stack_size = 0
        while len(scopes) is not 0:
            current_scope = scopes.pop()
            for idx, key in enumerate(current_scope.scope.defined_variables):
                scope_table[key] = stack_size
                stack_size = scope_table[key] - current_scope.scope.defined_variables[key]["type"].get_size(
                    self.size_bundle)
            for compilable in current_scope.body:
                if issubclass(type(compilable), Scopeable):
                    scopes.append(compilable)
        return scope_table, abs(stack_size)
