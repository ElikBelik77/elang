from compiler.parsing import Parser
from compiler.syntex_convertion import SyntaxConverter

p = Parser()
s = SyntaxConverter()
p.get_file_tokens('tests/basics.el')
functions = p.parse("tests/simple_return.elang")
for function in functions:
    for statements in function.body:
        print("> tests:", statements)
        b = [x for x in s.convert_statements(function, statements)]
