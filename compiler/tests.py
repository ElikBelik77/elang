from compiler.parsing import Parser
p = Parser()
p.get_file_tokens('tests/basics.el')
p.parse("tests/functions.elang")