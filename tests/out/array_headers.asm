SECTION .text
global main
main:
push ebp
mov ebp, esp
sub esp, 408
mov edi, [ebp - 28]
mov [edi - 0], 5
mov [edi - 4], 4
mov edi, [ebp - 176]
mov [edi - 0], 5
mov [edi - 4], 28
mov [edi - 8], 5
mov [edi - 12], 4
mov [edi - 36], 5
mov [edi - 40], 4
mov [edi - 64], 5
mov [edi - 68], 4
mov [edi - 92], 5
mov [edi - 96], 4
mov [edi - 120], 5
mov [edi - 124], 4
mov edi, [ebp - 408]
mov [edi - 0], 4
mov [edi - 4], 56
mov [edi - 8], 3
mov [edi - 12], 16
mov [edi - 64], 3
mov [edi - 68], 16
mov [edi - 120], 3
mov [edi - 124], 16
mov [edi - 176], 3
mov [edi - 180], 16
mov [edi - 16], 2
mov [edi - 20], 4
mov [edi - 32], 2
mov [edi - 36], 4
mov [edi - 48], 2
mov [edi - 52], 4
mov [edi - 72], 2
mov [edi - 76], 4
mov [edi - 88], 2
mov [edi - 92], 4
mov [edi - 104], 2
mov [edi - 108], 4
mov [edi - 128], 2
mov [edi - 132], 4
mov [edi - 144], 2
mov [edi - 148], 4
mov [edi - 160], 2
mov [edi - 164], 4
mov [edi - 184], 2
mov [edi - 188], 4
mov [edi - 200], 2
mov [edi - 204], 4
mov [edi - 216], 2
mov [edi - 220], 4
leave
ret

