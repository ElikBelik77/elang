from compilation.parsing import Parser
from semantic.semantic_check import *
from compilation.IA32.compiler import ProgramCompiler

p = Parser.create_default()
sc = SemanticChecker.create_default()
compiler = ProgramCompiler.create_default()
program = Program(p.parse_file("../tests/src/if.elang"))
sc.check(program)
compiler.compile(program, "../tests/out/if.asm")
