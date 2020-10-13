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
jbe loc_1C7D66
mov ecx, 1
loc_1C7D66:
push ecx
pop eax
test eax, eax
jz loc_A698C8
push 5
lea edi, [ebp - 4]
pop eax
mov [edi], eax
loc_A698C8:
leave
ret

