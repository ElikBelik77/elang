from compilation.IA32.template_factories import *
from compilation.models import *


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
            Mult: MultiplyTemplateFactory(),
            Minus: MinusTemplateFactory(),
            Plus: PlusTemplateFactory(),
            Div: DivTemplateFactory(),
            Assignment: AssignmentTemplateFactory(),
            DecimalConstantValue: DecimalConstantTemplateFactory(),
            Variable: VariableTemplateFactory(),
            Return: ReturnTemplateFactory(),
            FunctionCall: FunctionCallTemplateFactory(),
            Equal: LogicalEqualTemplateFactory(),
            LogicalGreater: LogicalGreaterTemplateFactory(),
            LogicalAnd: LogicalAndTemplateFactory(),
            LogicalOr: LogicalOrTemplateFactory(),
            If: IfTemplateFactory()
        })

    def __init__(self, factories: Dict[type, TemplateFactory]) -> None:
        self.factories = factories
        pass

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
            offset_table = self.produce_offset_table(function)
            assembly += self.compile_function(function, offset_table) + "\n"
        with open(destination_file, "w") as out:
            out.write(assembly)

    def compile_function(self, function, offset_table) -> str:
        """
        This function compiles a single function.
        :param function: the function to compile.
        :param offset_table: the offset table of the function.
        :return: the assembly code of the function.
        """
        if len(offset_table.keys()) == 0:
            stack_size = 0
        else:
            stack_size = abs(min(offset_table.values()))
        return self.factories[Function].produce(function, self.factories,
                                                {"stack_size": stack_size, "offset_table": offset_table,
                                                 "parent": 'global'})

    def produce_offset_table(self, scopeable: Scopeable) -> Dict[str, int]:
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
        while len(scopes) is not 0:
            current_scope = scopes.pop()
            for idx, key in enumerate(current_scope.scope.defined_variables):
                scope_table[key] = -4 * (idx + 1)
            for compilable in current_scope.body:
                if issubclass(type(compilable), Scopeable):
                    scopes.append(compilable)
        return scope_table
