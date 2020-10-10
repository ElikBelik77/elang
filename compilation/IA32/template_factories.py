from typing import Dict
from compilation.models import *
from compilation.IA32.utils import get_unqiue_id


class TemplateFactory:
    """
    Interface factory for object that create the assembly equivalent of compilable models.
    """

    def produce(self, object: Compilable, factories: Dict[type, "TemplateFactory"], bundle: Dict):
        """
        This function produces assembly code that executes the compilable models.
        :param object: the object to assemble.
        :param factories: the factories of the other compilabe objects.
        :param bundle: a bundle of extra information to use.
        :return: assembly code.
        """
        pass


class LogicalAndTemplateFactory(TemplateFactory):
    def produce(self, and_expression: LogicalAnd, factories: Dict[type, TemplateFactory], bundle: Dict):
        end = get_unqiue_id()
        assembly = (
            f"{factories[type(and_expression.left)].produce(and_expression.left, factories, bundle)}"
            f"{factories[type(and_expression.right)].produce(and_expression.right, factories, bundle)}"
            "pop eax"
            "xor ebx, ebx"
            f"test eax, eax"
            f"jnz {end}"
            "pop eax"
            "test eax, eax"
            f"jnz {end}"
            "mov ebx, 1"
            f"{end}:"
            "push ebx"
        )
        return assembly


class LogicalOrTemplateFactory(TemplateFactory):
    def produce(self, or_expression: LogicalOr, factories: Dict[type, TemplateFactory], bundle: Dict):
        valid = get_unqiue_id()
        invalid = get_unqiue_id()
        assembly = (
            f"{factories[type(or_expression.left)].produce(or_expression.left, factories, bundle)}"
            f"{factories[type(or_expression.right)].produce(or_expression.right, factories, bundle)}"
            "pop eax"
            "xor ebx, ebx"
            "test eax, eax"
            f"jnz {valid}"
            "pop eax"
            "test eax, eax"
            f"jnz {valid}"
            f"jmp {invalid}"
            f"{valid}:"
            "mov ebx, 1"
            f"{invalid}"
            "push ebx"
        )
        return assembly


class LogicalGreaterTemplateFactory(TemplateFactory):
    def produce(self, greater_expression: LogicalGreater, factories: Dict[type, TemplateFactory], bundle: Dict):
        not_greater = get_unqiue_id()
        assembly = (
            f"{factories[type(greater_expression.left)].produce(greater_expression.left, factories, bundle)}"
            f"{factories[type(greater_expression.right)].produce(greater_expression.right, factories, bundle)}"
            "pop ebx"
            "pop eax"
            "xor ecx, ecx"
            "cmp eax, ebx"
            f"jbe {not_greater}"
            "mov ecx, 1"
            f"{not_greater}:"
            "push ecx"
        )


class LogicalEqualTemplateFactory(TemplateFactory):
    def produce(self, equal_expression: Equal, factories: Dict[type, TemplateFactory], bundle: Dict):
        not_equal = get_unqiue_id()
        assembly = (
            f"{factories[type(equal_expression.left)].produce(equal_expression.left, factories, bundle)}"
            f"{factories[type(equal_expression.right)].produce(equal_expression.right, factories, bundle)}"
            "xor ecx, ecx"
            "pop eax"
            "pop ebx"
            "cmp eax, ebx"
            f"jne {not_equal}"
            "mov ecx, 1"
            f"{not_equal}:"
            "push ecx"
        )


class FunctionCallTemplateFactory(TemplateFactory):
    def produce(self, function_call: FunctionCall, factories: Dict[type, TemplateFactory], bundle: Dict):
        argument_preparation = ""
        for arg in function_call.arguments[::-1]:
            arg_assembly = factories[type(arg)].produce(arg, factories, bundle)
            argument_preparation += (
                "{arg_assembly}"
            ).format(arg_assembly=arg_assembly)

        assembly = ("{argument_preparation}"
                    "call {function_name}\n"
                    "add esp, {arguments_size}\n"
                    "push eax\n").format(argument_preparation=argument_preparation,
                                         function_name=function_call.name,
                                         arguments_size=len(function_call.arguments) * 4)
        return assembly


class ReturnTemplateFactory(TemplateFactory):
    def produce(self, return_expression: Return, factories: Dict[type, TemplateFactory], bundle: Dict):
        assembly = ("{return_expression}".format(
            return_expression=factories[type(return_expression.expression)].produce(return_expression.expression,
                                                                                    factories,
                                                                                    bundle)))
        assembly += (
            "pop eax\n"
            "leave\n"
            "ret\n"
        )
        return assembly


class FunctionTemplateFactory(TemplateFactory):
    def produce(self, function: Function, factories: Dict[type, TemplateFactory], bundle: Dict):
        body_assembly = ""
        has_ret = False
        for expression in function.body:
            if isinstance(expression, Return):
                has_ret = True
            if not isinstance(expression, VariableDeclaration):
                body_assembly += factories[type(expression)].produce(expression, factories, bundle)
        function_assembly = ("{name}:\n"
                             "push ebp\n"
                             "mov ebp, esp\n"
                             "sub esp, {stack_size}\n"
                             "{function_body}").format(
            name=function.name, stack_size=bundle["stack_size"],
            function_body=body_assembly)
        if not has_ret:
            function_assembly += (
                "leave\n"
                "ret\n"
            )
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
            "push eax\n"
        )
        return assembly


class AssignmentTemplateFactory(TemplateFactory):
    def produce(self, assigment_expression: Assignment, factories: Dict[type, TemplateFactory], bundle: Dict):
        assembly = factories[type(assigment_expression.right)].produce(assigment_expression.right, factories, bundle)
        if bundle["offset_table"][assigment_expression.left.name] > 0:
            assembly += (
                "lea edi, [ebp + {var_offset}]\n"
                "pop eax\n"
                "mov [edi], eax\n"
            ).format(var_offset=bundle["offset_table"][assigment_expression.left.name])
        else:
            assembly += (
                "lea edi, [ebp - {var_offset}]\n"
                "pop eax\n"
                "mov [edi], eax\n"
            ).format(var_offset=-bundle["offset_table"][assigment_expression.left.name])
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
        if bundle["offset_table"][variable_expression.name] > 0:
            assembly = (
                "lea edi, [ebp + {var_offset}]\n"
                "mov edi, [edi]\n"
                "push edi\n".format(var_offset=bundle["offset_table"][variable_expression.name])
            )
        else:
            assembly = (
                "lea edi, [ebp - {var_offset}]\n"
                "mov edi, [edi]\n"
                "push edi\n".format(var_offset=-bundle["offset_table"][variable_expression.name])
            )
        return assembly
