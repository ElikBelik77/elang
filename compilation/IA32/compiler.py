from typing import Tuple

from compilation.IA32.utils import produce_offset_table, produce_class_vtable
from compilation.IA32.template_factories import *
from compilation.type_system.primitives import Primitive
from parsing import Parser


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
            NewOperator: NewOperatorTemplateFactory(),
            If: IfTemplateFactory(),
            While: WhileTemplateFactory(),
            ArrayInitializer: ArrayInitializeTemplateFactory(),
            ElangClass: ElangClassTemplateFactory(),
            DotOperator: DotOperatorTemplateFactory()
        })

    def __init__(self, factories: Dict[type, TemplateFactory], verbose: bool = True) -> None:
        self.factories = factories
        self.size_bundle = {
            "int": 4
        }
        self.verbose = True

    def compile_dependency(self, dependency):
        parser = Parser.create_default()
        dp_program = parser.parse_file(dependency)

    def _compile_to_str(self, program: Program) -> str:
        """
        This function compiles a program.
        :param program: the program to compile.
        :return: None.
        `"""
        assembly = ""
        for dp in program.includes:
            assembly += self.compile_dependency(dp)
        vtables = {}
        for elang_class in program.classes.keys():
            self.size_bundle[elang_class] = program.classes[elang_class].get_size(self.size_bundle)
            vtables[elang_class] = produce_class_vtable(program.classes[elang_class], self.size_bundle)
        for elang_class in program.classes.keys():
            assembly += self.factories[ElangClass].produce(program.classes[elang_class], self.factories,
                                                           {"parent": 'global', "size_bundle": self.size_bundle,
                                                            "program": program,
                                                            "vtables": vtables,
                                                            "verbose": self.verbose})

        for f_name in program.functions:
            assembly += self.compile_function(program, program.functions[f_name]) + "\n"
        return assembly

    def compile(self, program: Program, destination_file: str) -> None:
        """
        This function compiles a program.
        :param program: the program to compile.
        :param destination_file: the destination path to write the output to.
        :return: None.
        """
        assembly = ("SECTION .text\n"
                    "extern malloc\n"
                    "global main\n")
        assembly += self._compile_to_str(program)
        with open(destination_file, "w") as out:
            out.write(assembly)

    def compile_function(self, program, function) -> str:
        """
        This function compiles a single function.
        :param function: the function to compile.
        :param offset_table: the offset table of the function.
        :return: the assembly code of the function.
        """
        offset_table, stack_size = produce_offset_table(function, self.size_bundle)
        return self.factories[Function].produce(function, self.factories,
                                                {"stack_size": stack_size, "offset_table": offset_table,
                                                 "scope": function.scope, "size_bundle": self.size_bundle,
                                                 "program": program,
                                                 "verbose": self.verbose})
