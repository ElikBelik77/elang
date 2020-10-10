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
- [ ] Logical operators
- [ ] if/else
- [ ] Loops
- [x] Assembling with NASM
- [ ] Support for IA64
- [ ] Interaction with the file system

## Examples of syntax and it's assembly compiled version
```
int return_five() {
    return 5;
}


int return_i_plus_j() {
    int i = 5;
    int j = 6;
    return i+j;
}

int this_function_calls_i_plus_j() {
    return return_i_plus_j();
}
```
Compiling to IA32 using stack based approach will yield:
```
return_five:
push ebp
mov ebp, esp
sub esp, 0
push 5
pop eax
leave
ret
return_i_plus_j:
push ebp
mov ebp, esp
sub esp, 8
push 5
lea edi, [ebp - 4]
pop eax
mov [edi], eax
push 6
lea edi, [ebp - 8]
pop eax
mov [edi], eax
lea edi, [ebp - 8]
mov edi, [edi]
push edi
lea edi, [ebp - 4]
mov edi, [edi]
push edi
pop eax
pop ebx
add eax, ebx
push eax
pop eax
leave
ret
this_function_calls_i_plus_j:
push ebp
mov ebp, esp
sub esp, 0
call return_i_plus_j
add esp, 0
push eax
pop eax
leave
ret
```
