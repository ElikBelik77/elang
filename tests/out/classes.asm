SECTION .text
extern malloc
global main
;ElangClassTemplateFactory
;ElangClassTemplateFactory
;FunctionTemplateFactory
Foo_constructor:
push ebp
mov ebp, esp
;AssignmentTemplateFactory
;NewOperatorTemplateFactory
push 4
call malloc
add esp, 4
push eax

;DotOperatorTemplateFactory
;PointerVariableTemplateFactory
lea edi, [ebp + 12]
push edi
mov eax, [eax]
add eax, 4
pop edi
pop eax
mov [edi], eax
leave
ret
vt_Foo_constructor:
jmp Foo_constructor
;FunctionTemplateFactory
get_my_foo:
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
call vt_Foo_constructor
add esp, 4

;PointerVariableTemplateFactory
lea edi, [ebp - 0]
push edi
pop edi
pop eax
mov [edi], eax
;ReturnTemplateFactory
;VariableTemplateFactory
lea edi, [ebp - 0]
mov edi, [edi]
push edi
pop eax
leave
ret

;FunctionTemplateFactory
main:
push ebp
mov ebp, esp
sub esp, 4
;AssignmentTemplateFactory
;FunctionCallTemplateFactory
call get_my_foo
push eax
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
mov eax, [eax]
add eax, 4
mov eax, [eax]
add eax, 0
pop edi
pop eax
mov [edi], eax
;AssignmentTemplateFactory
;DecimalConstantTemplateFactory
push 5
;DotOperatorTemplateFactory
;FunctionCallTemplateFactory
call get_my_foo
push eax
mov eax, [eax]
add eax, 4
mov eax, [eax]
add eax, 0
pop edi
pop eax
mov [edi], eax
leave
ret

