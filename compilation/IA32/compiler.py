from compilation.IA32.template_factories import *
from models import *


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
            Variable: VariableTemplateFactory()
        })

    def __init__(self, factories: Dict[type, TemplateFactory]):
        self.factories = factories
        pass

    def compile(self, program: Program, destination_file: str):
        assembly = ""
        for function in program.functions:
            offset_table = self.produce_offset_table(function)
            assembly += self.compile_function(function, offset_table)

        with open(destination_file, "w") as out:
            out.write(assembly)

    def compile_function(self, function, offset_table):
        stack_size = max(offset_table.values())
        return self.factories[Function].produce(function, self.factories,
                                                {"stack_size": stack_size, "offset_table": offset_table})

    def produce_offset_table(self, scopeable: Scopeable):
        scope_table = {}
        scope_table[scopeable]: Dict[str, int] = {}

        if isinstance(scopeable, Function):
            for idx, arg in enumerate(scopeable.arguments):
                scope_table[scopeable][arg.name] = 12 + idx * 8
        scopes: List[Scopeable] = [scopeable]
        while len(scopes) is not 0:
            current_scope = scopes.pop()
            if current_scope not in scope_table:
                scope_table[current_scope]: Dict[str, int] = {}
            for idx, key in enumerate(current_scope.scope.defined_variables):
                scope_table[current_scope][key] = -4 * (idx + 1)
            for compilable in current_scope.body:
                if issubclass(type(compilable), Scopeable):
                    scopes.append(compilable)
        return scope_table
