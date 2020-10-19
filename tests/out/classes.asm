SECTION .text
extern malloc
global main
;ElangClassTemplateFactory
;ElangClassTemplateFactory
;FunctionTemplateFactory
Foo_Bar:
push ebp
mov ebp, esp
leave
ret
;FunctionTemplateFactory
Foo_constructor:
push ebp
mov ebp, esp
leave
ret
vt_Foo_Bar:
jmp Foo_Bar
vt_Foo_constructor:
jmp Foo_constructor
;FunctionTemplateFactory
main:
push ebp
mov ebp, esp
sub esp, 4
;AssignmentTemplateFactory
;NewOperatorTemplateFactory
push 36
call malloc
add esp, 4
push eax
push eax
call vt_Foo_Foo_constructor
add esp, 4

;PointerVariableTemplateFactory
lea edi, [ebp - 0]
push edi
pop edi
pop eax
mov [edi], eax
;AssignmentTemplateFactory
;DecimalConstantTemplateFactory
push 5
;DotOperatorTemplateFactory
;PointerVariableTemplateFactory
lea edi, [ebp - 0]
push edi
pop eax
mov eax, [eax]
add eax, 8
mov eax, [eax]
push eax
pop eax
add eax, 4
push eax
pop edi
pop eax
mov [edi], eax
leave
ret

