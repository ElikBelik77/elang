import re
from factories import *
from compilation.parsing import Parser
from compilation.semantic_check import *
from compilation.IA32.compiler import ProgramCompiler



p = Parser.create_default()
sc = SemanticChecker().add_all()
compiler = ProgramCompiler.create_default()
program = Program(p.parse_file("tests/src/functions.elang"))
sc.check(program)
compiler.compile(program, "tests/out/functions.asm")
