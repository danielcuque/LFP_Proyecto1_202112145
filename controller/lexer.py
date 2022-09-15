from controller.operation import Operation


class Lexer:
    token_table = []
    row = 0
    column = 0
    prev_state = 0
    state = 0

    def scan(self, cadena: str, operation: Operation) -> list:
        open_tag = ""
        close_tag = ""
        token = ""
        operations = []
        closes = False

        while len(cadena) > 0:
            char = cadena[0]

            if char == "\n":
                self.fila += 1
                self.columna = 0
                cadena = cadena[1:]
                continue
            elif char == " ":
                self.columna += 1
                cadena = cadena[1:]
                continue

            # verify current state
            if self.state == 0:
                pass

            elif self.state == 1:
                pass

            elif self.state == 2:
                pass

            elif self.state == 3:
                pass

            elif self.state == 4:
                pass

            elif self.state == 5:
                pass
