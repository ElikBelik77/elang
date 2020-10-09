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
