SECTION .text
global main
main:
push ebp
mov ebp, esp
sub esp, 408
lea edi, [ebp - 0]
mov [edi - 0], dword 5
mov [edi - 4], dword 4
lea edi, [ebp - 28]
mov [edi - 0], dword 5
mov [edi - 4], dword 28
mov [edi - 8], dword 5
mov [edi - 12], dword 4
mov [edi - 36], dword 5
mov [edi - 40], dword 4
mov [edi - 64], dword 5
mov [edi - 68], dword 4
mov [edi - 92], dword 5
mov [edi - 96], dword 4
mov [edi - 120], dword 5
mov [edi - 124], dword 4
lea edi, [ebp - 176]
mov [edi - 0], dword 4
mov [edi - 4], dword 56
mov [edi - 8], dword 3
mov [edi - 12], dword 16
mov [edi - 64], dword 3
mov [edi - 68], dword 16
mov [edi - 120], dword 3
mov [edi - 124], dword 16
mov [edi - 176], dword 3
mov [edi - 180], dword 16
mov [edi - 16], dword 2
mov [edi - 20], dword 4
mov [edi - 32], dword 2
mov [edi - 36], dword 4
mov [edi - 48], dword 2
mov [edi - 52], dword 4
mov [edi - 72], dword 2
mov [edi - 76], dword 4
mov [edi - 88], dword 2
mov [edi - 92], dword 4
mov [edi - 104], dword 2
mov [edi - 108], dword 4
mov [edi - 128], dword 2
mov [edi - 132], dword 4
mov [edi - 144], dword 2
mov [edi - 148], dword 4
mov [edi - 160], dword 2
mov [edi - 164], dword 4
mov [edi - 184], dword 2
mov [edi - 188], dword 4
mov [edi - 200], dword 2
mov [edi - 204], dword 4
mov [edi - 216], dword 2
mov [edi - 220], dword 4
leave
ret

