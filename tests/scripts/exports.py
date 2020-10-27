from compilation.parsing import Parser
from semantic.semantic_check import *
from compilation.IA32.compiler import ProgramCompiler

p = Parser.create_default()
sc = SemanticChecker.create_default()
compiler = ProgramCompiler.create_default()
program = p.parse_file("../src/exports.elang")
sc.check(program)
compiler.compile(program, "../out/exports.asm")
