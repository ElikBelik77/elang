SECTION .text
global main
main:
push ebp
mov ebp, esp
sub esp, 116
lea edi, [ebp - 0]
mov [edi - 0], dword 5
mov [edi - 4], dword 4
push 5
push 1

lea edi, [ebp - 0]
push edi

pop edi
pop eax
mov ebx, [edi]
cmp eax, ebx
jb loc_0CACD1
mov eax, 0
mov ebx, 0
int 0x80
loc_0CACD1:
mov ecx, [edi - 4]
xor edx, edx
mul ecx
sub edi, 8
sub edi, eax
push edi
pop edi
pop eax
mov [edi], eax
lea edi, [ebp - 28]
mov [edi - 0], dword 4
mov [edi - 4], dword 20
mov [edi - 8], dword 3
mov [edi - 12], dword 4
mov [edi - 28], dword 3
mov [edi - 32], dword 4
mov [edi - 48], dword 3
mov [edi - 52], dword 4
mov [edi - 68], dword 3
mov [edi - 72], dword 4
push 6
push 2

push 0

lea edi, [ebp - 28]
push edi

pop edi
pop eax
mov ebx, [edi]
cmp eax, ebx
jb loc_E65F10
mov eax, 0
mov ebx, 0
int 0x80
loc_E65F10:
mov ecx, [edi - 4]
xor edx, edx
mul ecx
sub edi, 8
sub edi, eax
push edi

pop edi
pop eax
mov ebx, [edi]
cmp eax, ebx
jb loc_512AAF
mov eax, 0
mov ebx, 0
int 0x80
loc_512AAF:
mov ecx, [edi - 4]
xor edx, edx
mul ecx
sub edi, 8
sub edi, eax
push edi
pop edi
pop eax
mov [edi], eax
leave
ret

