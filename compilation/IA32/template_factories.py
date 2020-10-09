from typing import Dict
from models import *


class TemplateFactory:
    def produce(self, object: Compilable, factories: Dict[type, "TemplateFactory"], bundle: Dict):
        pass


class ReturnTemplateFactory(TemplateFactory):
    def produce(self, return_expression: Return, factories: Dict[type, TemplateFactory], bundle: Dict):
        pass

class FunctionTemplateFactory(TemplateFactory):
    def produce(self, function: Function, factories: Dict[type, TemplateFactory], bundle: Dict):
        body_assembly = ""
        for expression in function.body:
            if isinstance(expression, Return):
                pass
            else:
                body_assembly += factories[type(expression)].produce(expression, factories, bundle)
        function_assembly = ("{name}:"
                             "push ebp\n"
                             "mov ebp, esp\n"
                             "sub esp, {stack_size}\n"
                             "{function_body}\n"
                             "add esp, {stack_size}\n"
                             "mov esp, ebp\n"
                             "pop ebp\n"
                             "ret\n").format(name=function.name, stack_size=bundle["stack_size"],
                                             function_body=body_assembly)
        return function_assembly


class MultiplyTemplateFactory(TemplateFactory):
    def produce(self, mult_expression: Mult, factories: Dict[type, TemplateFactory], bundle: Dict):
        assembly = factories[type(mult_expression.right)].produce(mult_expression.right, factories, bundle) \
                   + factories[type(mult_expression.left)].produce(mult_expression.left, factories, bundle)
        assembly += (
            "pop eax\n"
            "pop ecx\n"
            "xor edx, edx\n"
            "mul ecx\n"
            "push eax\n"
        )
        return assembly


class PlusTemplateFactory(TemplateFactory):
    def produce(self, plus_expression: Plus, factories: Dict[type, TemplateFactory], bundle: Dict):
        assembly = factories[type(plus_expression.right)].produce(plus_expression.right, factories, bundle) \
                   + factories[type(plus_expression.left)].produce(plus_expression.left, factories, bundle)
        assembly += (
            "pop eax\n"
            "pop ebx\n"
            "add eax, ebx\n"
            "push eax\n"
        )
        return assembly


class MinusTemplateFactory(TemplateFactory):
    def produce(self, minus_expression: Minus, factories: Dict[type, TemplateFactory], bundle: Dict):
        assembly = factories[type(minus_expression.right)].produce(minus_expression.right, factories, bundle) \
                   + factories[type(minus_expression.left)].produce(minus_expression.left, factories, bundle)
        assembly += (
            "pop eax\n"
            "pop ebx\n"
            "sub eax, ebx\n"
            "push eax\n"
        )
        return assembly


class DivTemplateFactory(TemplateFactory):
    def produce(self, div_expression: Div, factories: Dict[type, TemplateFactory], bundle: Dict):
        assembly = factories[type(div_expression.right)].produce(div_expression.right, factories, bundle) \
                   + factories[type(div_expression.left)].produce(div_expression.left, factories, bundle)
        assembly += (
            "pop eax\n"
            "pop ecx\n"
            "xor edx, edx\n"
            "div ecx\n"
            "push eax"
        )
        return assembly


class AssignmentTemplateFactory(TemplateFactory):
    def produce(self, assigment_expression: Assignment, factories: Dict[type, TemplateFactory], bundle: Dict):
        assembly = factories[type(assigment_expression.right)].produce(assigment_expression.right, factories, bundle)
        assembly += (
            "lea edi, [ebp - {var_offset}]\n"
            "pop eax\n"
            "mov [edi], eax\n"
        ).format(var_offset=bundle["offset_table"][assigment_expression.left.name])
        return assembly


class DecimalConstantTemplateFactory(TemplateFactory):
    def produce(self, decimal_value_expression: DecimalConstantValue, factories: Dict[type, TemplateFactory],
                bundle: Dict):
        assembly = (
            "push {value}\n".format(value=decimal_value_expression.value)
        )
        return assembly


class VariableTemplateFactory(TemplateFactory):
    def produce(self, variable_expression: Variable, factories: Dict[type, TemplateFactory], bundle: Dict):
        assembly = (
            "lea edi, [ebp - {var_offset}]\n"
            "mov edi, [edi]\n"
            "push edi\n".format(var_offset=bundle["offset_table"][variable_expression.name])
        )
        return assembly
