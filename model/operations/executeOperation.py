from math import (
    sin,
    cos,
    tan
)

from typing import Tuple

valid_operations = {
    "SUMA": "+",
    "RESTA": "-",
    "MULTIPLICACION": "*",
    "DIVISION": "/",
    "POTENCIA": "^",
    "RAIZ": "sqrt",
    "INVERSO": "1/",
    "SENO": "seno",
    "COSENO": "coseno",
    "TANGENTE": "tangente",
}


def execute_operation(operation: str = "", table_of_tokens: list = []) -> Tuple:
    res = "("
    position = 0
    for token in table_of_tokens:
        if token.get_type_name() == "START_TAG":
            if "operacion" in token.literal.lower():
                equals_index = token.literal.index("=")
                close_tag_index = token.literal.index(">")
                operation = token.literal.strip()[equals_index + 2:close_tag_index]
                res += execute_arithmetic_operation(operation, table_of_tokens[position + 1:])
                position = token.get_position()
        elif token.get_type_name() == "NUMBER":
            res += token.literal + " " + valid_operations[operation] + " "
        elif token.get_type_name() == "TEXT":
            res += valid_operations[token.literal]
        elif token.get_type_name() == "CLOSE_TAG":
            if "operacion" in token.literal.lower():
                res = res[:-3] + ")"
                return res
        position += 1
    res = res[:-3] + ")"
    return res


def execute_arithmetic_operation(operation: str, table_of_numbers) -> str:
    position = 0
    res = "("
    for token in table_of_numbers:
        if token.get_type_name() == "START_TAG":
            if "operacion" in token.literal.lower():
                assing_index = token.literal.index("=")
                close_tag_index = token.literal.index(">")
                operation = token.literal[assing_index +
                                          1:close_tag_index].strip()
                res += execute_arithmetic_operation(
                    operation, table_of_numbers[position + 1:])
        elif token.get_type_name() == "NUMBER":
            res += token.literal + " " + valid_operations[operation] + " "
        elif token.get_type_name() == "TEXT":
            res += valid_operations[token.literal]
        elif token.get_type_name() == "CLOSE_TAG":
            if "operacion" in token.literal.lower():
                res = res[:-3] + ")"
                return res
        position += 1
    res = res[:-3] + ")"
    return res
