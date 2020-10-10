from compilation.parsing import Parser
from compilation.semantic_check import *
from compilation.IA32.compiler import ProgramCompiler
import os
import sys

if not len(sys.argv) == 3:
    print("Usage: python3 elang.py source_file.elang destination_file.out")

source_path = sys.argv[1]
destination_path = sys.argv[2]
p = Parser.create_default()
sc = SemanticChecker.create_default()
compiler = ProgramCompiler.create_default()
program = Program(p.parse_file(source_path))
sc.check(program)
compiler.compile(program, f"{source_path}.asm")
os.system("nasm -f elf {source_path}.asm -o {source_path}.o".format(source_path=source_path))
os.system("gcc -m32 {source_path}.o -o {destination_path}".format(source_path=source_path,
                                                                  destination_path=destination_path))
os.remove(f"{source_path}.asm")
os.remove(f"{source_path}.o")
