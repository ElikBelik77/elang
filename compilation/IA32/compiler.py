from typing import Tuple

from compilation.IA32.utils import produce_offset_table, produce_class_vtable
from compilation.IA32.template_factories import *
from compilation.type_system.primitives import Primitive
from compilation.parsing import Parser


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

    def compile_program(self, program: Program) -> Tuple[str, str]:
        """
        This function compiles a program.
        :param program: the program to compile.
        :return: None.
        `"""
        text_segment, data_segment = "", ""
        for dp in program.includes:
            text_segment += self.compile_dependency(dp)
        vtables = {}
        for elang_class in program.classes.keys():
            self.size_bundle[elang_class] = program.classes[elang_class].get_size(self.size_bundle)
            vtables[elang_class] = produce_class_vtable(program.classes[elang_class], self.size_bundle)
        compilation_bundle = {"parent": 'global', "size_bundle": self.size_bundle,
                              "program": program,
                              "vtables": vtables,
                              "verbose": self.verbose}
        for elang_class in program.classes.keys():
            text_segment += self.factories[ElangClass].produce(program.classes[elang_class], self.factories,
                                                               compilation_bundle)

        for f_name in program.functions:
            text_segment += self.compile_function(program, program.functions[f_name]) + "\n"
        for var in program.global_vars.keys():
            data_segment += f"db {program.global_vars[var].get_size(self.size_bundle)} dup ?\n"
        init_global_variables = ""
        for init_statement in program.globals_init:
            init_global_variables += self.factories[type(init_statement)].produce(init_statement, self.factories,
                                                                                  compilation_bundle)
        text_segment += ("start:\n"
                         f"{init_global_variables}"
                         "call main")
        return text_segment, data_segment

    def compile(self, program: Program, destination_file: str) -> None:
        """
        This function compiles a program.
        :param program: the program to compile.
        :param destination_file: the destination path to write the output to.
        :return: None.
        """
        text_segment, data_segment = self.compile_program(program)
        assembly = ""
        if len(data_segment) is not 0:
            assembly += ("section .data\n"
                         f"{data_segment}")
        assembly += ("section .text\n"
                     "extern malloc\n"
                     "global main\n"
                     f"{text_segment}")

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
