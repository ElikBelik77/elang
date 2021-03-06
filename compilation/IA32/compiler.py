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
        self.verbose = False

    def compile_dependency(self, dependency):
        parser = Parser.create_default()
        dp_program = parser.parse_file(dependency)

    def compile_program(self, program: Program, compilation_bundle) -> Tuple[str, str, str]:
        """
        This function compiles a program.
        :param program: the program to compile.
        :return: None.
        """
        text_segment, data_segment, init_segment = "", "", ""
        for init_statement in program.variables_init:
            init_segment += self.factories[type(init_statement)].produce(init_statement, self.factories,
                                                                         compilation_bundle)
        init_segment += (f"mov edi, {program.name}\n"
                         f"{self.factories[NewOperator].produce(NewOperator(FunctionCall(program.name, [], program)), self.factories, compilation_bundle)}"
                         "pop eax\n"
                         "mov [edi], eax\n"
                         )
        for dependency in program.includes:
            compilation_bundle["program"] = program.includes[dependency].program
            dp_text, dp_data, dp_init = self.compile_program(program.includes[dependency].program, compilation_bundle)
            text_segment += dp_text
            data_segment += dp_data
            init_segment += dp_init
        compilation_bundle["program"] = program
        vtables = {}
        for elang_class in program.classes.keys():
            self.size_bundle[elang_class] = program.classes[elang_class].get_size(self.size_bundle)
            vtables[elang_class] = produce_class_vtable(program.classes[elang_class], self.size_bundle)
        vtables[program] = produce_class_vtable(program, self.size_bundle)
        compilation_bundle["vtables"] = vtables
        for elang_class in program.classes.keys():
            text_segment += self.factories[ElangClass].produce(program.classes[elang_class], self.factories,
                                                               compilation_bundle)

        # for f_name in program.functions:
        #     text_segment += self.compile_function(program, program.functions[f_name]) + "\n"
        for var in program.variables.keys():
            if var not in program.includes:
                data_segment += f"{var}: times {program.variables[var].get_size(self.size_bundle)} db 0\n"
        for include in program.includes:
            data_segment += f"{include}: times {self.size_bundle['int']} db 0\n"
        return text_segment, data_segment, init_segment

    def compile(self, program: Program, destination_file: str) -> None:
        """
        This function compiles a program.
        :param program: the program to compile.
        :param destination_file: the destination path to write the output to.
        :return: None.
        """
        compilation_bundle = {"scope": program.scope, "size_bundle": self.size_bundle,
                              "program": program,
                              "verbose": self.verbose}
        text_segment, data_segment, init_statements = self.compile_program(program, compilation_bundle)
        text_segment += ("main:\n"
                         f"{init_statements}"
                         f"call {program.name}_main\n")
        data_segment += f"{program.name}: times 4 db 0\n"
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
