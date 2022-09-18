from math import (
    sin,
    cos,
    tan
)

from controller.token import Token

valid_operations = {
    "SUMA": "+",
    "RESTA": "-",
    "MULTIPLICACION": "*",
    "DIVISION": "/",
    "POTENCIA": "^",
    "RAIZ": "sqrt",
    "INVERSO": "1/",
    "SENO": "sin",
    "COSENO": "cos",
    "TANGENTE": "tan",
}


class ExecuteOperation:
    def __init__(self, table_of_tokens: list = []):
        self.table_of_tokens: list[Token] = table_of_tokens
        self.result_operations: list = []
        self.table_of_operations = []

        self._open_operation_tags = 0
        self._read_position = 0
        self._find_all_operations()

        #self._current_operation = ""
        #self._prev_operation = ""

    def _find_all_operations(self) -> None:
        open_tags = 0
        position = 0
        operandos = []

        while len(self.table_of_tokens) > position:
            token: Token = self.table_of_tokens[position]
            if self._is_start_tag_operation(token):
                open_tags += 1
                operandos.append(token)

            elif self._is_end_tag_operation(token):
                open_tags -= 1
                operandos.append(token)

            elif self._is_number_tag(token):
                operandos.append(token)

            if len(operandos) > 0 and open_tags == 0:
                self.table_of_operations.append(operandos)
                operandos = []

            position += 1
        self._execute_all_operations()

    def _execute_all_operations(self) -> None:
        for operators in self.table_of_operations:
            res = self._aritmetic_operation(operators)
            print("res", res)

    def _find_type_operation(self, token: Token) -> str:
        token_literal = token.literal.replace(" ", "")
        equals_index: int = token_literal.find("=")
        close_tag_index: int = token_literal.find(">")
        return token_literal[equals_index+1: close_tag_index]

    def _aritmetic_operation(self, table_of_operators: list):
        type_operation = self._find_type_operation(table_of_operators[0])
        position: int = 1
        res: str = ""

        while len(table_of_operators) > position:
            token: Token = table_of_operators[position]

            if self._is_start_tag_operation(token):
                type_operation = self._find_type_operation(table_of_operators[position])

                resp = self._aritmetic_operation(table_of_operators[position:])
                res += f'{resp[0]}{valid_operations[type_operation]}'
                position += resp[1]

            elif self._is_number_tag(token):
                if type_operation in valid_operations:
                    if self._is_special_operation(type_operation):
                        res += f'{valid_operations[type_operation]}({token.literal})'
                    else:
                        res += f'{token.literal}{valid_operations[type_operation]}'
            elif self._is_end_tag_operation(token):
                return [f'({res[:-1]})', position]
            position += 1
            print(res)

        return [f'({res[:-1]})', position]


    def _is_start_tag_operation(self, tag: Token) -> bool:
        return bool(tag.get_type_name() == "START_TAG" and "operacion" in tag.literal.lower())

    def _is_end_tag_operation(self, tag: Token) -> bool:
        return bool(tag.get_type_name() == "CLOSE_TAG" and "operacion" in tag.literal.lower())

    def _is_number_tag(self, tag: Token) -> bool:
        return bool(tag.get_type_name() == "NUMBER")

    def _is_special_operation(self, type_operation: str) -> bool:
        type_operation = type_operation.upper()
        return bool(type_operation == "SENO" or type_operation == "COSENO" or type_operation == "TANGENTE" or type_operation == "RAIZ")

    def _execute_operationsv2(self, operation: str):
        res = ""
        while len(self.table_of_tokens) > self._read_position:
            token: Token = self.table_of_tokens[self._read_position]
            if token.get_type_name() == "START_TAG":
                if "operacion" in token.literal.lower():
                    self._open_tags += 1
                    equals_index: int = token.literal.find("=")
                    close_tag: int = token.literal.find(">")
                    operation: str = token.literal.strip()[equals_index + 2: close_tag]
                    self._read_position += 1
                    res += "(" + self._execute_operations(operation)[:-1] + ") "
            elif token.get_type_name() == "NUMBER":
                if operation in valid_operations:
                    if operation.upper() == "SENO" or operation == "COSENO" or operation == "TANGENTE":
                        res += f"{valid_operations[operation]}({token.literal}) "
                    else:
                        res += f'{token.literal}{valid_operations[operation]}'
            elif token.get_type_name() == "CLOSE_TAG":
                if "operacion" in token.literal.lower():
                    self._open_tags -= 1
                    return res

            if self._open_tags == 0:
                if res != "":
                    self.result_operations.append(res[:-1])
                    res = ""
            self._read_position += 1





