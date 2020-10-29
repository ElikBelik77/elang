SECTION .data
includes dw ?
exports dw ?
SECTION .text
extern malloc
global main
;FunctionTemplateFactory
includes_module_init:
push ebp
mov ebp, esp
;AssignmentTemplateFactory
;NewOperatorTemplateFactory
push 0
call malloc
add esp, 4
push eax

mov edi, includes
pop eax
mov edi, eax
;FunctionCallTemplateFactory
call exports_module_init
push eax
leave
ret
;ElangClassTemplateFactory
;FunctionTemplateFactory
includes_main:
push ebp
mov ebp, esp
sub esp, 4
;AssignmentTemplateFactory
;DotOperatorTemplateFactory
;PointerVariableTemplateFactory
mov edi, exports
push edi
pop eax
mov eax, [eax]
push eax
;DotOperatorTemplateFactory
push eax
call vt_exports_check
push eax
lea edi, [ebp - 4]
pop eax
mov [edi], eax
leave
ret
vt_includes_main:
jmp includes_main
;FunctionTemplateFactory
exports_module_init:
push ebp
mov ebp, esp
;AssignmentTemplateFactory
;NewOperatorTemplateFactory
push 0
call malloc
add esp, 4
push eax

mov edi, exports
pop eax
mov edi, eax
leave
ret
;ElangClassTemplateFactory
;FunctionTemplateFactory
exports_main:
push ebp
mov ebp, esp
leave
ret
;FunctionTemplateFactory
exports_check:
push ebp
mov ebp, esp
;ReturnTemplateFactory
;DecimalConstantTemplateFactory
push 5
pop eax
leave
ret
vt_exports_main:
jmp exports_main
vt_exports_check:
jmp exports_check
;ElangClassTemplateFactory
start:
call includes_module_init
push includes
call vt_includes_main
ret
