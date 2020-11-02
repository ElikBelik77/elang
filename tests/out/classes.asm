section .data
a_global_foo: db 4 dup ?
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
classes_get_a_foo:
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
classes_main:
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
mov edi, a_global_foo
push edi
pop eax
mov eax, [eax]
push eax
call vt_Foo_get_bar
push eax
leave
ret
vt_get_a_foo:
jmp get_a_foo
vt_main:
jmp main
main:
call run