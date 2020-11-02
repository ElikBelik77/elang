SECTION .data
db 4 dup ?
SECTION .text
extern malloc
global start
;FunctionTemplateFactory
main:
push ebp
mov ebp, esp
sub esp, 4
;AssignmentTemplateFactory
;DecimalConstantTemplateFactory
push 0
lea edi, [ebp - 4]
pop eax
mov [edi], eax
;IfTemplateFactory
;LogicalGreaterTemplateFactory
;DecimalConstantTemplateFactory
push 6
;DecimalConstantTemplateFactory
push 5
pop ebx
pop eax
xor ecx, ecx
cmp eax, ebx
jbe loc_B3CC8A
mov ecx, 1
loc_B3CC8A:
push ecx
pop eax
test eax, eax
jz loc_37F5B3
;AssignmentTemplateFactory
;DecimalConstantTemplateFactory
push 5
lea edi, [ebp - 4]
pop eax
mov [edi], eax
loc_37F5B3:
leave
ret

start:
;AssignmentTemplateFactory
;DecimalConstantTemplateFactory
push 5
mov edi, global
pop eax
mov DWORD PTR [edi], eax
call main