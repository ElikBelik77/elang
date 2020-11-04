section .data
exports: times 4 db 0
includes: times 4 db 0
section .text
extern malloc
global main
exports.Foo_check:
push ebp
mov ebp, esp
push 5
pop eax
leave
ret
vt_exports.Foo_check:
jmp exports.Foo_check
exports_check:
push ebp
mov ebp, esp
leave
ret
vt_exports_check:
jmp exports_check
includes_main:
push ebp
mov ebp, esp
sub esp, 8
mov edi, exports
push edi
pop eax
mov eax, [eax]
push eax
call vt_exports_check
push eax
lea edi, [ebp - 4]
pop eax
mov [edi], eax
push 0
call malloc
add esp, 4
push eax

lea edi, [ebp - 8]
push edi
pop edi
pop eax
mov [edi], eax
lea edi, [ebp - 8]
push edi
pop eax
mov eax, [eax]
push eax
call vt_exports.Foo_check
push eax
leave
ret
vt_includes_main:
jmp includes_main
main:
mov edi, includes
push 4
call malloc
add esp, 4
push eax

pop eax
mov [edi], eax
mov edi, exports
push 0
call malloc
add esp, 4
push eax

pop eax
mov [edi], eax
call includes_main
