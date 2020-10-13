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
jbe loc_A67794
mov ecx, 1
loc_A67794:
push ecx
pop eax
test eax, eax
jz loc_C1D17D
push 5
lea edi, [ebp - 4]
pop eax
mov [edi], eax
loc_C1D17D:
leave
ret

