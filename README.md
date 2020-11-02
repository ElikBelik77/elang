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
- [x] if/else (only 'if' statements for the time being.)
- [x] While loops
- [x] Arrays (and multi-dimensional arrays!)
- [ ] Include/Export
- [ ] Strings
- [ ] Global variables
- [x] Assembling with NASM
- [x] Classes
- [x] Sub classes
- [ ] Support for IA64
- [ ] Interaction with the file system
## Prerequisites & Usage
The compiler relies on NASM and GCC to assemble and link the source file and object files, so make sure they are in your ```PATH```.
Produce an executable by running the command
```
python3 elang.py <source_file.elang> <destination_file>
```

## Examples of syntax and it's assembly compiled version
#### Simple main program
```
int global_var = 5;
int run() {
    int i = 0;
    if (6 > global_var) {
        i = 5;
    }
}
```
Compiling to IA32 using stack based approach will yield:
```
section .data
db 4 dup ?
section .text
extern malloc
global main
run:
push ebp
mov ebp, esp
sub esp, 4
push 0
lea edi, [ebp - 4]
pop eax
mov [edi], eax
push 6
mov edi, DWORD [global_var]
push edi
pop ebx
pop eax
xor ecx, ecx
cmp eax, ebx
jbe loc_6132D6
mov ecx, 1
loc_6132D6:
push ecx
pop eax
test eax, eax
jz loc_47D88A
push 5
lea edi, [ebp - 4]
pop eax
mov [edi], eax
loc_47D88A:
leave
ret

main:
push 5
mov edi, global_var
pop eax
mov DWORD [edi], eax
call run
```
#### A more complex code snippet
```
class Bar {
    int my_bar;
    int Bar_Func() {
        return 5;
    }
}

class Foo {

    class SubFoo {
        Bar get_bar() {
            return new Bar();
        }
    }
    int a;
    Bar b;
    int[5] arr;
    Foo.SubFoo sub_foo;
    int constructor() {
        this.b = new Bar();
    }

    Bar get_bar() {
        return new Bar();
    }

}

Foo get_a_foo() {
    Foo my_foo = new Foo();
    return my_foo;
}

int run() {
    Foo foo = get_a_foo();
    foo.sub_foo = new Foo.SubFoo();
    foo.sub_foo.get_bar().Bar_Func();
    a_global_foo.get_bar();
}


Foo a_global_foo = new Foo();
```
Will compile to
```
section .data
db 4 dup ?
section .text
extern malloc
global main
Bar_Bar_Func:
push ebp
mov ebp, esp
push 5
pop eax
leave
ret
vt_Bar_Func:
jmp Bar_Func
Foo_constructor:
push ebp
mov ebp, esp
push 4
call malloc
add esp, 4
push eax

lea edi, [ebp + 12]
push edi
pop eax
mov eax, [eax]
push eax
pop eax
add eax, 4
push eax
pop edi
pop eax
mov [edi], eax
leave
ret
Foo_get_bar:
push ebp
mov ebp, esp
push 4
call malloc
add esp, 4
push eax

pop eax
leave
ret
init_Foo:
push ebp
mov ebp, esp
lea edi, [ebp + 12]
push edi
pop eax
lea edi, [eax + 8]
mov [edi + 0], dword 5
mov [edi + 4], dword 4
leave
ret
vt_constructor:
jmp constructor
vt_get_bar:
jmp get_bar
Foo.SubFoo_get_bar:
push ebp
mov ebp, esp
push 4
call malloc
add esp, 4
push eax

pop eax
leave
ret
vt_get_bar:
jmp get_bar
get_a_foo:
push ebp
mov ebp, esp
sub esp, 4
push 40
call malloc
add esp, 4
push eax
push eax
call init_Foo
push eax
call vt_Foo_constructor
add esp, 4

lea edi, [ebp - 4]
push edi
pop edi
pop eax
mov [edi], eax
lea edi, [ebp - 4]
mov edi, [edi]
push edi
pop eax
leave
ret

run:
push ebp
mov ebp, esp
sub esp, 4
call get_a_foo
push eax
lea edi, [ebp - 4]
push edi
pop edi
pop eax
mov [edi], eax
push 0
call malloc
add esp, 4
push eax

lea edi, [ebp - 4]
push edi
pop eax
mov eax, [eax]
push eax
pop eax
add eax, 36
push eax
pop edi
pop eax
mov [edi], eax
lea edi, [ebp - 4]
push edi
pop eax
mov eax, [eax]
push eax
pop eax
add eax, 36
mov eax, [eax]
push eax
call vt_Foo.SubFoo_get_bar
push eax
call vt_Bar_Bar_Func
push eax
mov edi, a_global_foo
push edi
pop eax
mov eax, [eax]
push eax
call vt_Foo_get_bar
push eax
leave
ret

main:
push 40
call malloc
add esp, 4
push eax
push eax
call init_Foo
push eax
call vt_Foo_constructor
add esp, 4

mov edi, a_global_foo
pop eax
mov DWORD [edi], eax
call run
```
