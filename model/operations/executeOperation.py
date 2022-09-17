from math import (
    sin,
    cos,
    tan
)

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


def execute_operation(table_of_tokens: list):
    position = 0
    res = ""
    position = 0
    for token in table_of_tokens:
        if token.get_type_name() == "START_TAG":
            if "operacion" in token.literal.lower():
                open_tag_index = token.literal.index("<")
                assing_index = token.literal.index("=")
                close_tag_index = token.literal.index(">")
                operation = token.literal[assing_index +
                                          1:close_tag_index].strip()
                execute_arithmetic_operation(
                    operation, table_of_tokens[position + 1:])
        position += 1
    return res


def execute_arithmetic_operation(operation: str, table_of_numbers):
    print(operation)
    for token in table_of_numbers:
        if token.get_type_name() == "CLOSE_TAG":
            break
        print(token)
