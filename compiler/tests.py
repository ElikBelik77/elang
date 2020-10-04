from compiler.parsing import Parser
from compiler.syntex_convertion import SyntaxConverter
from compiler.semantic_check import SemanticChecker, VariableDeclarationCheck

p = Parser()
s = SyntaxConverter()
sc = SemanticChecker([VariableDeclarationCheck()])
p.get_file_tokens('tests/basics.el')
functions = p.parse("tests/simple_return.elang")
for function in functions:
    s.convert_function(function)
    sc.check_function(function)
