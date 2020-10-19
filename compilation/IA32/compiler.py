from typing import Tuple

from compilation.IA32.utils import produce_offset_table, produce_class_vtable
from compilation.IA32.template_factories import *
from compilation.models.classes import ElangClass
from compilation.type_system.primitives import Primitive


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

    def compile(self, program: Program, destination_file: str) -> None:
        """
        This function compiles a program.
        :param program: the program to compile.
        :param destination_file: the destination path to write the output to.
        :return: None.
        """
        assembly = ("SECTION .text\n"
                    "global main\n")
        vtables = {}
        for elang_class in program.classes:
            self.size_bundle[elang_class.name] = elang_class.get_size(self.size_bundle)
            vtables[elang_class] = produce_class_vtable(elang_class, self.size_bundle)
        for elang_class in program.classes:
            assembly += self.factories[ElangClass].produce(elang_class, self.factories,
                                                           {"parent": 'global', "size_bundle": self.size_bundle,
                                                            "classes": program.classes,
                                                            "vtables": vtables,
                                                            "verbose": self.verbose})

        for function in program.functions:
            assembly += self.compile_function(program.classes, function) + "\n"
        with open(destination_file, "w") as out:
            out.write(assembly)

    def compile_function(self, classes, function) -> str:
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
                                                 "classes": classes,
                                                 "verbose": self.verbose})
