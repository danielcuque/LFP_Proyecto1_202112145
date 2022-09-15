from controller.operation import Operation
from controller.token import Token
from model.tokens.validCharacters import ValidCharacters


class Lexer:
    token_table: list[Token] = []
    row = 0
    column = 0
    prev_state = 0
    state = 0

    def scan(self, cadena: str, operation: Operation):
        open_tag = ""
        close_tag = ""
        token = ""
        operations = []
        closes = False
        valid_characters = ValidCharacters()

        while len(cadena) > 0:
            char = cadena[0]

            if char == "\n":
                self.row += 1
                self.column = 0
                cadena = cadena[1:]
                continue
            elif char == " ":
                self.column += 1
                cadena = cadena[1:]
                continue

            # verify current state
            if self.state == 0:
                if valid_characters.is_bracket_open(char):
                    self.save_token(char)
                    self.state = 1
                    self.prev_state = 0

            elif self.state == 1:
                if valid_characters.is_letter(char.lower()):
                    token += char

                    self.state = 1
                    self.prev_state = 1

                elif valid_characters.is_bracket_close(char):
                    self.save_token(token)
                    self.save_token(char)

                    if closes:
                        close_tag = token
                        closes = False

                        if close_tag.lower() == "operacion":
                            operation.operands = operations
                            return [cadena, operation]

                    if open_tag.lower() == "operacion":
                        op = Operation(token)
                        value = self.scan(cadena[1:], op)
                        cadena = value[0]
                        operations.append(value[1])

                    open_tag = token
                    token = ""

                    self.state = 2
                    self.prev_state = 1

                elif valid_characters.is_equal(char):
                    open_tag = token

                    self.save_token(token)
                    self.save_token(char)
                    token = ""

                    self.state = 3
                    self.prev_state = 1

                elif valid_characters.is_slash(char):
                    closes = True
                    self.save_token(char)

                    self.state = 5
                    self.prev_state = 1

            elif self.state == 2:
                if valid_characters.is_bracket_open:
                    self.save_token(char)

                    self.state = 1
                    self.prev_state = 2

                elif valid_characters.is_slash(char):
                    token += char

                    self.state = 4
                    self.prev_state = 2

            elif self.state == 3:
                if valid_characters.is_letter(char.lower()):
                    token += char

                    self.state = 1
                    self.prev_state = 3

            elif self.state == 4:
                if valid_characters.is_bracket_open(char.lower()):
                    if open_tag.lower() == "numero":
                        operations.append(int(token))

                    self.save_token(token)
                    self.save_token(char)
                    token = ""

                    self.state = 1
                    self.prev_state = 4

                elif valid_characters.is_number(char.lower()):
                    token += char

                    self.state = 4
                    self.prev_state = 4

            elif self.state == 5:
                if valid_characters.is_letter(char.lower()):
                    token += char

                    self.state = 1
                    self.prev_state = 5

            self.column += 1
            cadena = cadena[1:]

        operation.operands = operation
        return [cadena, operations]

    def save_token(self, token: str) -> None:
        self.token_table.append(Token(token, self.row, self.column))

    def imprimir_tokens(self):
        print('-'*31)
        print("| {:<4} | {:<7} | {:<10} |".format('Fila', 'Columna', 'Lexema'))
        print('-'*31)
        for token in self.token_table:
            print("| {:<4} | {:<7} | {:<10} |".format(
                token.row, token.column, token.lexeme))
