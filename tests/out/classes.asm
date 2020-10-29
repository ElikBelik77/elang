SECTION .text
extern malloc
global main
;ElangClassTemplateFactory
;FunctionTemplateFactory
Bar_Hi:
push ebp
mov ebp, esp
;ReturnTemplateFactory
;DecimalConstantTemplateFactory
push 5
pop eax
leave
ret
vt_Bar_Hi:
jmp Bar_Hi
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
pop eax
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
;FunctionTemplateFactory
Foo_get_a_bar:
push ebp
mov ebp, esp
;ReturnTemplateFactory
;NewOperatorTemplateFactory
push 4
call malloc
add esp, 4
push eax

pop eax
leave
ret
init_Foo:
push ebp
mov ebp, esp
lea edi, [ebp + 12]
push edi
;ArrayInitializeTemplateFactory
pop eax
lea edi, [eax + 8]
mov [edi + 0], dword 5
mov [edi + 4], dword 4
leave
ret
vt_Foo_constructor:
jmp Foo_constructor
vt_Foo_get_a_bar:
jmp Foo_get_a_bar
;ElangClassTemplateFactory
;FunctionTemplateFactory
get_a_foo:
push ebp
mov ebp, esp
sub esp, 4
;AssignmentTemplateFactory
;NewOperatorTemplateFactory
push 40
call malloc
add esp, 4
push eax
push eax
call init_Foo
push eax
call vt_Foo_constructor
add esp, 4

;PointerVariableTemplateFactory
lea edi, [ebp - 4]
push edi
pop edi
pop eax
mov [edi], eax
;ReturnTemplateFactory
;VariableTemplateFactory
lea edi, [ebp - 4]
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
call get_a_foo
push eax
;PointerVariableTemplateFactory
lea edi, [ebp - 4]
push edi
pop edi
pop eax
mov [edi], eax
;AssignmentTemplateFactory
;DecimalConstantTemplateFactory
push 5
;DotOperatorTemplateFactory
;PointerVariableTemplateFactory
lea edi, [ebp - 4]
push edi
pop eax
mov eax, [eax]
push eax
pop eax
add eax, 4
mov eax, [eax]
push eax
pop eax
add eax, 0
push eax
pop edi
pop eax
mov [edi], eax
;AssignmentTemplateFactory
;DecimalConstantTemplateFactory
push 5
;DotOperatorTemplateFactory
;FunctionCallTemplateFactory
call get_a_foo
push eax
pop eax
add eax, 4
mov eax, [eax]
push eax
pop eax
add eax, 0
push eax
pop edi
pop eax
mov [edi], eax
;DotOperatorTemplateFactory
;FunctionCallTemplateFactory
call get_a_foo
push eax
;DotOperatorTemplateFactory
call vt_Foo_get_a_bar
push eax
;DotOperatorTemplateFactory
call vt_Bar_Hi
push eax
leave
ret

