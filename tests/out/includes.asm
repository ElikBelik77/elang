section .data
exports: times 4 db 0
includes: times 4 db 0
section .text
extern malloc
global main
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
sub esp, 4
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
