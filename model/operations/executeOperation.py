from typing import List

from controller.token import Token

from math import (
    sin,
    cos,
    tan,
    pow,
)

from model.helpers.items import valid_operations


class ExecuteOperation:
    def __init__(self, table_of_tokens: list):
        self.table_of_tokens: List[Token] = table_of_tokens
        self.table_of_operations = []
        self.result_operations: list = []

        self._open_operation_tags = 0
        self._read_position = 0
        self._find_all_operations()

    def _find_all_operations(self) -> None:
        open_tags = 0
        position = 0
        operands = []

        while len(self.table_of_tokens) > position:
            token: Token = self.table_of_tokens[position]
            if self._is_start_tag_operation(token):
                open_tags += 1
                operands.append(token)

            elif self._is_end_tag_operation(token):
                open_tags -= 1
                operands.append(token)

            elif self._is_number_tag(token) and open_tags > 0:
                operands.append(token)

            if len(operands) > 0 and open_tags == 0:
                self.table_of_operations.append(operands)
                operands = []

            position += 1
        self._execute_all_operations()

    def _execute_all_operations(self) -> None:
        for operators in self.table_of_operations:
            res = self._arithmetic_operation(operators)
            type_operation = self._find_operation(operators)
            self.result_operations.append({
                "TIPO": type_operation,
                "OPERACION": res[0],
                "RESULTADO": eval(res[0])
            })

    @staticmethod
    def _find_type_operation(token: Token) -> str:
        token_literal = token.literal.replace(" ", "")
        equals_index: int = token_literal.find("=")
        close_tag_index: int = token_literal.find(">")
        return token_literal[equals_index + 1: close_tag_index].upper()

    def _arithmetic_operation(self, table_of_operators: list, prev_operation: str = ""):
        current_operation = self._find_type_operation(table_of_operators[0])
        position: int = 1
        res: str = ""

        while len(table_of_operators) > position:
            token: Token = table_of_operators[position]

            if self._is_start_tag_operation(token):
                resp = self._arithmetic_operation(
                    table_of_operators[position:], current_operation)
                current_operation = resp[2]
                if current_operation == "INVERSO":
                    res += f'{resp[0]}'
                else:
                    res += f'{resp[0]}{valid_operations[current_operation]}'

                position += resp[1]

            elif self._is_number_tag(token):
                current_operation = current_operation.upper()
                if current_operation in valid_operations:
                    if self._is_special_operation(current_operation):
                        res += f'{valid_operations[current_operation]}({token.literal}) '
                    elif current_operation == "POTENCIA":
                        res += f'{token.literal}{valid_operations[current_operation]}'
                    elif current_operation == "INVERSO":
                        res += f'{token.literal}'
                    elif current_operation == "RAIZ":
                        res += f'(1/{token.literal})**'
                    else:
                        res += f'{token.literal}{valid_operations[current_operation]}'
            elif self._is_end_tag_operation(token):
                if current_operation == "POTENCIA":
                    return [f'({res[:-2]})', position, prev_operation]
                elif current_operation == "RAIZ":
                    return [f'({res[3:-2]}', position, prev_operation]
                elif current_operation == "INVERSO":
                    return [f'(1/{res})', position, prev_operation]
                return [f'({res[:-1]})', position, prev_operation]
            position += 1

        return [f'({res})', position, prev_operation]

    def _find_operation(self, table_of_operators: list) -> str:
        open_tags = 0

        for token in table_of_operators:
            if self._is_start_tag_operation(token):
                open_tags += 1
            if open_tags > 1:
                return "COMPLEJA"
        return self._find_type_operation(table_of_operators[0])

    @staticmethod
    def _is_start_tag_operation(tag: Token) -> bool:
        return bool(tag.get_type_name() == "START_TAG" and "operacion" in tag.literal.lower())

    @staticmethod
    def _is_end_tag_operation(tag: Token) -> bool:
        return bool(tag.get_type_name() == "CLOSE_TAG" and "operacion" in tag.literal.lower())

    @staticmethod
    def _is_number_tag(tag: Token) -> bool:
        return bool(tag.get_type_name() == "NUMBER")

    @staticmethod
    def _is_special_operation(type_operation: str) -> bool:
        type_operation = type_operation.upper()
        return bool(type_operation == "SENO" or type_operation == "COSENO" or type_operation == "TANGENTE")

    def get_result_operations(self) -> list:
        return self.result_operations
