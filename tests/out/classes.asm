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
