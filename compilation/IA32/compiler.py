from compilation.IA32.template_factories import *
from compilation.models import *


class ProgramCompiler:
    @staticmethod
    def create_default():
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
            FunctionCall: FunctionCallTemplateFactory()
        })

    def __init__(self, factories: Dict[type, TemplateFactory]):
        self.factories = factories
        pass

    def compile(self, program: Program, destination_file: str):
        assembly = ("SECTION .text\n"
                    "global main\n")
        for function in program.functions:
            offset_table = self.produce_offset_table(function)
            assembly += self.compile_function(function, offset_table)
        with open(destination_file, "w") as out:
            out.write(assembly)

    def compile_function(self, function, offset_table):
        if len(offset_table.keys()) == 0:
            stack_size = 0
        else:
            stack_size = abs(min(offset_table.values()))
        return self.factories[Function].produce(function, self.factories,
                                                {"stack_size": stack_size, "offset_table": offset_table,
                                                 "parent": 'global'})

    def produce_offset_table(self, scopeable: Scopeable):
        scope_table: Dict[str, int] = {}

        if isinstance(scopeable, Function):
            for idx, arg in enumerate(scopeable.arguments):
                scope_table[arg.name] = 12 + idx * 8
        scopes: List[Scopeable] = [scopeable]
        while len(scopes) is not 0:
            current_scope = scopes.pop()
            for idx, key in enumerate(current_scope.scope.defined_variables):
                scope_table[key] = -4 * (idx + 1)
            for compilable in current_scope.body:
                if issubclass(type(compilable), Scopeable):
                    scopes.append(compilable)
        return scope_table
