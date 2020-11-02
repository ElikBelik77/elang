section .data
global_var: db 4 dup ?
section .text
extern malloc
global main
if_run:
push ebp
mov ebp, esp
sub esp, 4
push 0
lea edi, [ebp - 4]
pop eax
mov [edi], eax
push 5
mov edi, global_var
pop eax
mov DWORD [edi], eax
push 6
mov edi, DWORD [global_var]
push edi
pop ebx
pop eax
xor ecx, ecx
cmp eax, ebx
jbe loc_41173F
mov ecx, 1
loc_41173F:
push ecx
pop eax
test eax, eax
jz loc_9B820E
push 5
lea edi, [ebp - 4]
pop eax
mov [edi], eax
loc_9B820E:
leave
ret
vt_if_run:
jmp if_run
