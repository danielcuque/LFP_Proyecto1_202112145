from math import (
    sin,
    cos,
    tan
)

from controller.token import Token

from typing import Tuple

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

        self._open_tags = 0
        self._read_position = 0
        self._execute_operations("")

    def _execute_operations(self, operation: str):
        res = ""
        while len(self.table_of_tokens) > self._read_position:
            token: Token = self.table_of_tokens[self._read_position]
            if token.get_type_name() == "START_TAG":
                if "operacion" in token.literal.lower():
                    self._open_tags += 1
                    equals_index: int = token.literal.find("=")
                    close_tag: int = token.literal.find(">")
                    operation: str = token.literal.strip()[equals_index+2: close_tag]
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
