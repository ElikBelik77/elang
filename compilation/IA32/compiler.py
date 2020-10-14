from typing import Tuple

from compilation.IA32.template_factories import *


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
        self.primitive_bundle = {
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
                                                 "parent": 'global', "primitive_bundle": self.primitive_bundle,
                                                 "verbose": self.verbose})

    def produce_offset_table(self, scopeable: Scopeable) -> Tuple[Dict[str, int], int]:
        """
        This function produces an offset table for a scope.
        :param scopeable: the scope.
        :return: a dictionary that matches a variable (or argument) name, to it's offset in relation to ebp.
        """
        scope_table: Dict[str, int] = {}

        if isinstance(scopeable, Function):
            for idx, arg in enumerate(scopeable.arguments):
                scope_table[arg.name] = 12 + idx * 4
        scopes: List[Scopeable] = [scopeable]
        stack_size = 0
        while len(scopes) is not 0:
            current_scope = scopes.pop()
            for idx, key in enumerate(current_scope.scope.defined_variables):
                scope_table[key] = stack_size
                stack_size = scope_table[key] - current_scope.scope.defined_variables[key]["type"].get_size(
                    self.primitive_bundle)
            for compilable in current_scope.body:
                if issubclass(type(compilable), Scopeable):
                    scopes.append(compilable)
        return scope_table, abs(stack_size)
