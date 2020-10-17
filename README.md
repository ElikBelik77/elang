# ELANG
## Description
This hobby project is just a programming language I'm implementing. It's a C-like, imperative, statically typed langauge.
Currently, I only implemented IA32 instruction set, the compiler uses a naive stack based approach.
## List of features
- [x] Scopes
- [x] Recursive functions
- [x] Shunting yard expression parsing
- [x] Basic semantic checks
- [x] Arithmetic operators (*still no support for 64 bit multiplication on IA32)
- [x] Logical operators
- [ ] if/else
- [x] While loops
- [x] Arrays (and multi-dimensional arrays!)
- [ ] Strings
- [ ] Global variables
- [x] Assembling with NASM
- [ ] Support for IA64
- [ ] Interaction with the file system
## Prerequisites & Usage
The compiler relies on NASM and GCC to assemble and link the source file and object files, so make sure they are in your ```PATH```.
Produce an executable by running the command
```
python3 elang.py <source_file.elang> <destination_file>
```

## Examples of syntax and it's assembly compiled version
```
int main() {
    int i = 0;
    if (6 > 5) {
        i = 5;
    }
}
```
Compiling to IA32 using stack based approach will yield:
```
SECTION .text
global main
main:
push ebp
mov ebp, esp
sub esp, 4
push 0
lea edi, [ebp - 4]
pop eax
mov [edi], eax
push 6
push 5
pop ebx
pop eax
xor ecx, ecx
cmp eax, ebx
jbe loc_386BEE
mov ecx, 1
loc_386BEE:
push ecx
pop eax
test eax, eax
jz loc_A13E29
push 5
lea edi, [ebp - 4]
pop eax
mov [edi], eax
loc_A13E29:
leave
ret
```
