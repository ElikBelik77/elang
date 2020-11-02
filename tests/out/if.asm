section .data
db 4 dup (?)
section .text
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
;VariableTemplateFactory
mov edi, DWORD PTR [global]
pop ebx
pop eax
xor ecx, ecx
cmp eax, ebx
jbe loc_02A707
mov ecx, 1
loc_02A707:
push ecx
pop eax
test eax, eax
jz loc_22FA57
;AssignmentTemplateFactory
;DecimalConstantTemplateFactory
push 5
lea edi, [ebp - 4]
pop eax
mov [edi], eax
loc_22FA57:
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