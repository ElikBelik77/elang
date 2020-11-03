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
- [x] Global variables
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
#### Compiling ```Classes.elang```
A simple example that shows most of the features the language has to offer.
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

int main() {
    this.a_global_foo = get_a_foo();
}

Foo a_global_foo;
```
Compiling to IA32 using stack based approach will yield:
```
section .data
a_global_foo: times 4 db 0
classes: times 4 db 0
section .text
extern malloc
global main
classes.Bar_Bar_Func:
push ebp
mov ebp, esp
push 5
pop eax
leave
ret

vt_classes.Bar_Bar_Func:
jmp classes.Bar_Bar_Func

classes.Foo_constructor:
push ebp
mov ebp, esp
push 4
call malloc
add esp, 4
push eax
lea edi, [ebp + 8]
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

classes.Foo_get_bar:
push ebp
mov ebp, esp
push 4
call malloc
add esp, 4
push eax
pop eax
leave
ret

init_classes.Foo:
push ebp
mov ebp, esp
lea edi, [ebp + 8]
mov edi, [edi]
push edi
pop eax
lea edi, [eax + 8]
mov [edi + 0], dword 5
mov [edi + 4], dword 4
leave
ret

vt_classes.Foo_constructor:
jmp classes.Foo_constructor

vt_classes.Foo_get_bar:
jmp classes.Foo_get_bar

classes.Foo.SubFoo_get_bar:
push ebp
mov ebp, esp
push 4
call malloc
add esp, 4
push eax
pop eax
leave
ret

vt_classes.Foo.SubFoo_get_bar:
jmp classes.Foo.SubFoo_get_bar

classes_get_a_foo:
push ebp
mov ebp, esp
sub esp, 4
push 40
call malloc
add esp, 4
push eax
push eax
call init_classes.Foo
push eax
call vt_classes.Foo_constructor
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

classes_main:
push ebp
mov ebp, esp
call classes_get_a_foo
push eax
lea edi, [ebp + 8]
push edi
pop eax
mov eax, [eax]
push eax
pop eax
add eax, 0
push eax
pop edi
pop eax
mov [edi], eax
leave
ret

vt_classes_get_a_foo:
jmp classes_get_a_foo
vt_classes_main:
jmp classes_main
main:
mov edi, classes
push 4
call malloc
add esp, 4
push eax
call classes_main

```