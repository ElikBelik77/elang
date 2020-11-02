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