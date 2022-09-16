from controller.operation import Operation
from controller.token import Token
from model.tokens.validCharacters import ValidCharacters


class Lexer:
    token_table = []
    row = 0
    column = 0
    prev_state = 0
    state = 0
    valid_characters = ValidCharacters()

    def scan(self, cadena: str, operation: Operation):
        open_tag = ""
        close_tag = ""
        token = ""
        operations = []
        closes = False

        while len(cadena) > 0:
            char = cadena[0]

            if char == "\n":
                self.row += 1
                self.column = 0
                cadena = cadena[1:]
                continue
            elif char == " ":
                self.column += 1
                if len(token) > 0:
                    self.save_token(token, "Correcto")
                    token = ""
                cadena = cadena[1:]
                continue

            elif self.valid_characters.is_letter(char) is None and self.valid_characters.is_number(char) is None and self.valid_characters.is_slash(char) is None and self.valid_characters.is_equal(char) is None and self.valid_characters.is_bracket_open(char) is None and self.valid_characters.is_bracket_close(char) is None and self.valid_characters.is_slash(char) is None:

                self.column += 1
                self.save_token(token, "Correcto")
                self.save_token(char, "Error")
                token = ""
                cadena = cadena[1:]
                continue

            # verify current state
            if self.state == 0:
                if self.valid_characters.is_bracket_open(char):
                    self.save_token(char, "Correcto")
                    self.state = 1
                    self.prev_state = 0

            elif self.state == 1:
                if self.valid_characters.is_letter(char.lower()):
                    token += char

                    self.state = 1
                    self.prev_state = 1

                elif self.valid_characters.is_bracket_close(char):
                    self.save_token(token, "Correcto")
                    self.save_token(char, "Correcto")

                    if closes:
                        close_tag = token
                        closes = False

                        if close_tag.lower() == "operacion":
                            operation.operands = operations
                            return [cadena, operation]

                    if open_tag.lower() == "operacion":
                        op = Operation(token)
                        value = self.scan(cadena[1:], op) # recursion
                        cadena = value[0]
                        operations.append(value[1])

                    open_tag = token = ""

                    self.state = 2
                    self.prev_state = 1

                elif self.valid_characters.is_equal(char):
                    open_tag = token

                    self.save_token(token, "Correcto")
                    self.save_token(char, "Correcto")
                    token = ""

                    self.state = 3
                    self.prev_state = 1

                elif self.valid_characters.is_slash(char):
                    closes = True
                    self.save_token(char, "Correcto")

                    self.state = 5
                    self.prev_state = 1

            elif self.state == 2:
                if self.valid_characters.is_bracket_open(char):
                    self.save_token(token, "Correcto")
                    self.save_token(char, "Correcto")

                    token = ""

                    self.state = 1
                    self.prev_state = 2

                elif self.valid_characters.is_number(char):
                    token += char

                    self.state = 4
                    self.prev_state = 2

                elif self.valid_characters.is_letter(char):
                    token += char

                    self.state = 2
                    self.prev_state = 2

            elif self.state == 3:
                if self.valid_characters.is_letter(char.lower()):
                    token += char

                    self.state = 1
                    self.prev_state = 3

            elif self.state == 4:
                if self.valid_characters.is_bracket_open(char.lower()):
                    if open_tag.lower() == "numero":
                        operations.append(int(token))

                    self.save_token(token, "Correcto")
                    self.save_token(char, "Correcto")
                    token = ""

                    self.state = 1
                    self.prev_state = 4

                elif self.valid_characters.is_number(char.lower()):
                    token += char

                    self.state = 4
                    self.prev_state = 4

            elif self.state == 5:
                if self.valid_characters.is_letter(char.lower()):
                    token += char

                    self.state = 1
                    self.prev_state = 5

            self.column += 1
            cadena = cadena[1:]

        operation.operands = operation
        return [cadena, operations]

    def save_token(self, token: str, is_valid: str) -> None:
        if token == "":
            return
        self.token_table.append(Token(self.row, self.column, token, is_valid))

    def imprimir_tokens(self):
        print('-'*31)
        print("| {:<4} | {:<7} | {:<10} | {:<12}".format('Fila', 'Columna', 'Lexema', "Tipo"))
        print('-'*31)
        for token in self.token_table:
            print("| {:<4} | {:<7} | {:<12} | {:<12} |".format(
                token.row, token.column, token.lexeme, token.is_valid))
