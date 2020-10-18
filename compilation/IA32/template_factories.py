from typing import Dict
from compilation.models.values import *
from compilation.models.keywords import *
from compilation.models.operators import *
from compilation.IA32.utils import get_unique_id
from compilation.models.arrays import ArrayInitializer


class TemplateFactory:
    """
    Interface factory for object that create the assembly equivalent of compilable models.
    """

    def produce(self, object: Compilable, factories: Dict[type, "TemplateFactory"], bundle: Dict) -> str:
        """
        This function produces assembly code that executes the compilable models.
        :param object: the object to assemble.
        :param factories: the factories of the other compilabe objects.
        :param bundle: a bundle of extra information to use.
        :return: assembly code.
        """
        pass

    def add_verbose(self, bundle):
        if bundle["verbose"]:
            return f";{type(self).__name__}\n"
        return ""


class LogicalAndTemplateFactory(TemplateFactory):
    def produce(self, and_expression: LogicalAnd, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        end = get_unique_id()
        assembly = self.add_verbose(bundle)
        assembly += (
            f"{factories[type(and_expression.left)].produce(and_expression.left, factories, bundle)}"
            f"{factories[type(and_expression.right)].produce(and_expression.right, factories, bundle)}"
            "pop eax\n"
            "xor ebx, ebx\n"
            f"test eax, eax\n"
            f"jz loc_{end}\n"
            "pop eax\n"
            "test eax, eax\n"
            f"jz loc_{end}\n"
            "mov ebx, 1\n"
            f"loc_{end}:\n"
            "push ebx\n"
        )
        return assembly


class LogicalOrTemplateFactory(TemplateFactory):
    def produce(self, or_expression: LogicalOr, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        valid = get_unique_id()
        invalid = get_unique_id()
        assembly = self.add_verbose(bundle)
        assembly += (
            f"{factories[type(or_expression.left)].produce(or_expression.left, factories, bundle)}"
            f"{factories[type(or_expression.right)].produce(or_expression.right, factories, bundle)}"
            "pop eax\n"
            "pop ecx\n"
            "xor ebx, ebx\n"
            "test eax, eax\n"
            f"jnz loc_{valid}\n"
            "test ecx, ecx\n"
            f"jnz loc_{valid}\n"
            f"jmp loc_{invalid}\n"
            f"loc_{valid}:\n"
            "mov ebx, 1\n"
            f"loc_{invalid}:\n"
            "push ebx\n"
        )
        return assembly


class LogicalGreaterTemplateFactory(TemplateFactory):
    def produce(self, greater_expression: LogicalGreater, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        not_greater = get_unique_id()
        assembly = self.add_verbose(bundle)
        assembly += (
            f"{factories[type(greater_expression.left)].produce(greater_expression.left, factories, bundle)}"
            f"{factories[type(greater_expression.right)].produce(greater_expression.right, factories, bundle)}"
            "pop ebx\n"
            "pop eax\n"
            "xor ecx, ecx\n"
            "cmp eax, ebx\n"
            f"jbe loc_{not_greater}\n"
            "mov ecx, 1\n"
            f"loc_{not_greater}:\n"
            "push ecx\n"
        )
        return assembly


class LogicalEqualTemplateFactory(TemplateFactory):
    def produce(self, equal_expression: Equal, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        not_equal = get_unique_id()
        assembly = self.add_verbose(bundle)
        assembly += (
            f"{factories[type(equal_expression.left)].produce(equal_expression.left, factories, bundle)}"
            f"{factories[type(equal_expression.right)].produce(equal_expression.right, factories, bundle)}"
            "xor ecx, ecx\n"
            "pop eax\n"
            "pop ebx\n"
            "cmp eax, ebx\n"
            f"jne loc_{not_equal}\n"
            "mov ecx, 1\n"
            f"loc_{not_equal}:\n"
            "push ecx\n"
        )
        return assembly


class FunctionCallTemplateFactory(TemplateFactory):
    def produce(self, function_call: FunctionCall, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        argument_preparation = ""
        for arg in function_call.arguments[::-1]:
            arg_assembly = factories[type(arg)].produce(arg, factories, bundle)
            argument_preparation += (
                "{arg_assembly}"
            ).format(arg_assembly=arg_assembly)
        argument_clean_up_line = "add esp, {arguments_size}\n".format(
            arguments_size=len(function_call.arguments) * 4) if len(function_call.arguments) is not 0 else ""
        assembly = self.add_verbose(bundle)
        assembly += ("{argument_preparation}"
                     "call {function_name}\n"
                     "{argument_clean_up_line}"
                     "push eax\n").format(argument_preparation=argument_preparation,
                                          function_name=function_call.name,
                                          argument_clean_up_line=argument_clean_up_line)
        return assembly


class ReturnTemplateFactory(TemplateFactory):
    def produce(self, return_expression: Return, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        assembly = self.add_verbose(bundle)
        assembly += ("{return_expression}".format(
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
    def produce(self, function: Function, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        body_assembly = ""
        has_ret = False
        for expression in function.body:
            if isinstance(expression, Return):
                has_ret = True
            if not isinstance(expression, VariableDeclaration):
                body_assembly += factories[type(expression)].produce(expression, factories, bundle)
        stack_allocation_line = "sub esp, {stack_size}\n".format(stack_size=bundle["stack_size"]) if bundle[
                                                                                                         "stack_size"] is not 0 else ""
        function_assembly = (f"{self.add_verbose(bundle)}"
                             "{name}:\n"
                             "push ebp\n"
                             "mov ebp, esp\n"
                             "{stack_allocation_line}"
                             "{function_body}").format(
            name=function.name, stack_allocation_line=stack_allocation_line,
            function_body=body_assembly)
        if not has_ret:
            function_assembly += (
                "leave\n"
                "ret\n"
            )
        return function_assembly


class MultiplyTemplateFactory(TemplateFactory):
    def produce(self, mult_expression: MultiplicationOperator, factories: Dict[type, TemplateFactory],
                bundle: Dict) -> str:
        assembly = self.add_verbose(bundle)
        assembly += factories[type(mult_expression.right)].produce(mult_expression.right, factories, bundle) \
                    + factories[type(mult_expression.left)].produce(mult_expression.left, factories, bundle)
        assembly += (
            "pop eax\n"
            "pop ecx\n"
            "xor edx, edx\n"
            "mul ecx\n"
            "push eax\n"
        )
        return assembly


class AdditionTemplateFactory(TemplateFactory):
    def produce(self, plus_expression: AdditionOperator, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        assembly = self.add_verbose(bundle)
        assembly += factories[type(plus_expression.right)].produce(plus_expression.right, factories, bundle) \
                    + factories[type(plus_expression.left)].produce(plus_expression.left, factories, bundle)
        assembly += (
            "pop eax\n"
            "pop ebx\n"
            "add eax, ebx\n"
            "push eax\n"
        )
        return assembly


class SubtractionTemplateFactory(TemplateFactory):
    def produce(self, minus_expression: SubtractOperator, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        assembly = self.add_verbose(bundle)
        assembly += factories[type(minus_expression.right)].produce(minus_expression.right, factories, bundle) \
                    + factories[type(minus_expression.left)].produce(minus_expression.left, factories, bundle)
        assembly += (
            "pop eax\n"
            "pop ebx\n"
            "sub eax, ebx\n"
            "push eax\n"
        )
        return assembly


class DivisionTemplateFactory(TemplateFactory):
    def produce(self, div_expression: DivisionOperator, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        assembly = self.add_verbose(bundle)
        assembly += factories[type(div_expression.right)].produce(div_expression.right, factories, bundle) \
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
    def produce(self, assigment_expression: Assignment, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        assembly = self.add_verbose(bundle)
        assembly += factories[type(assigment_expression.right)].produce(assigment_expression.right, factories, bundle)
        # TODO: check if left produces a POINTER TYPE, instead of array indexer for the future
        if isinstance(assigment_expression.left, ArrayIndexer):
            assembly += (
                f"{factories[type(assigment_expression.left)].produce(assigment_expression.left, factories, bundle)}"
                "pop edi\n"
                "pop eax\n"
                "mov [edi], eax\n"
            )
        elif bundle["offset_table"][assigment_expression.left.name] > 0:
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
                bundle: Dict) -> str:
        assembly = self.add_verbose(bundle)
        assembly += (
            "push {value}\n".format(value=decimal_value_expression.value)
        )
        return assembly


class VariableTemplateFactory(TemplateFactory):
    def produce(self, variable_expression: Variable, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        assembly = self.add_verbose(bundle)
        if bundle["offset_table"][variable_expression.name] > 0:
            assembly += (
                "lea edi, [ebp + {var_offset}]\n"
                "mov edi, [edi]\n"
                "push edi\n".format(var_offset=bundle["offset_table"][variable_expression.name])
            )
        else:
            assembly += (
                "lea edi, [ebp - {var_offset}]\n"
                "mov edi, [edi]\n"
                "push edi\n".format(var_offset=-bundle["offset_table"][variable_expression.name])
            )
        return assembly


class IfTemplateFactory(TemplateFactory):
    def produce(self, if_expression: If, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        skip_if_id = get_unique_id()
        body_assembly = ""
        for expression in if_expression.body:
            if not isinstance(expression, VariableDeclaration):
                body_assembly += factories[type(expression)].produce(expression, factories, bundle)
        assembly = self.add_verbose(bundle)
        assembly += (
            f"{factories[type(if_expression.condition)].produce(if_expression.condition, factories, bundle)}"
            "pop eax\n"
            "test eax, eax\n"
            f"jz loc_{skip_if_id}\n"
            f"{body_assembly}"
            f"loc_{skip_if_id}:\n"
        )
        return assembly


class WhileTemplateFactory(TemplateFactory):
    def produce(self, while_expression: While, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:

        loop_start = get_unique_id()
        loop_end = get_unique_id()
        body_assembly = ""
        for expression in while_expression.body:
            if not isinstance(expression, VariableDeclaration):
                body_assembly += factories[type(expression)].produce(expression, factories, bundle)
        assembly = (
            f"{self.add_verbose(bundle)}"
            f"loc_{loop_start}:\n"
            f"{factories[type(while_expression.condition)].produce(while_expression.condition, factories, bundle)}"
            "pop eax\n"
            "test eax, eax\n"
            f"jz loc_{loop_end}\n"
            f"{body_assembly}"
            f"jmp loc_{loop_start}\n"
            f"loc_{loop_end}:\n"
        )
        return assembly


class ArrayInitializeTemplateFactory(TemplateFactory):
    def produce(self, array: ArrayInitializer, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        array_start_offset = bundle["offset_table"][array.variable_name]
        arrays_metadata = array.array.get_metadata(bundle["size_bundle"])
        assembly = self.add_verbose(bundle)
        assembly += (
            f"lea edi, [ebp - {-array_start_offset}]\n"
        )
        for metadata in arrays_metadata:
            for offset in metadata["offsets"]:
                assembly += (
                    f"mov [edi - {offset}], dword {metadata['array_size']}\n"
                    f"mov [edi - {offset + bundle['size_bundle']['int']}], dword {metadata['cell_size']}\n"
                )
        return assembly


class ArrayIndexerTemplateFactory(TemplateFactory):
    def produce(self, indexer_expression: ArrayIndexer, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        passed_boundary_check = get_unique_id()
        assembly = self.add_verbose(bundle)
        assembly += (
            f"{factories[type(indexer_expression.right)].produce(indexer_expression.right, factories, bundle)}\n"
            f"{factories[type(indexer_expression.left)].produce(indexer_expression.left, factories, bundle)}\n"
            "pop edi\n"
            "pop eax\n"
            "mov ebx, [edi]\n"
            "cmp eax, ebx\n"  # Check if index is of bounds
            f"jb loc_{passed_boundary_check}\n"
            "mov eax, 0\n"
            "mov ebx, 0\n"
            "int 0x80\n"
            f"loc_{passed_boundary_check}:\n"
            "mov ecx, [edi - 4]\n"
            "xor edx, edx\n"
            "mul ecx\n"
            "sub edi, 8\n"
            "sub edi, eax\n"
            "push edi\n"

        )
        return assembly


class PointerVariableTemplateFactory(TemplateFactory):
    def produce(self, variable_expression: Variable, factories: Dict[type, TemplateFactory], bundle: Dict) -> str:
        assembly = self.add_verbose(bundle)
        if bundle["offset_table"][variable_expression.name] > 0:
            assembly += (
                "lea edi, [ebp + {var_offset}]\n"
                "push edi\n".format(var_offset=bundle["offset_table"][variable_expression.name])
            )
        else:
            assembly += (
                "lea edi, [ebp - {var_offset}]\n"
                "push edi\n".format(var_offset=-bundle["offset_table"][variable_expression.name])
            )
        return assembly