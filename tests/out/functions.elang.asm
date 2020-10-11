SECTION .text
global main
logical_operators:
push ebp
mov ebp, esp
push 5
push 6
push 6
xor ecx, ecx
pop eax
pop ebx
cmp eax, ebx
jne CE3AD2
mov ecx, 1
CE3AD2:
push ecx
push 0
pop ebx
pop eax
xor ecx, ecx
cmp eax, ebx
jbe EEC1A5
mov ecx, 1
EEC1A5:
push ecx
push 1
pop eax
xor ebx, ebx
test eax, eax
jnz 133226
pop eax
test eax, eax
jnz 133226
jmp 7C4E5B
133226:
mov ebx, 1
7C4E5B:
push ebx
pop eax
xor ebx, ebx
test eax, eax
jnz 70223B
pop eax
test eax, eax
jnz 70223B
mov ebx, 1
70223B:
push ebx
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
call return_i_plus_j
push eax
pop eax
leave
ret

main:
push ebp
mov ebp, esp
sub esp, 12
call logical_operators
push eax
lea edi, [ebp - 4]
pop eax
mov [edi], eax
call return_i_plus_j
push eax
lea edi, [ebp - 8]
pop eax
mov [edi], eax
call this_function_calls_i_plus_j
push eax
lea edi, [ebp - 12]
pop eax
mov [edi], eax
push 1
pop eax
leave
ret

