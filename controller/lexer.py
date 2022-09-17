from re import match

from controller.token import (
    Token,
    TokenType,
)


class Lexer:

    def __init__(self, source: str) -> None:
        self._source = source
        self._character: str = ""
        self._read_position: int = 0
        self._position: int = 0
        self._row: int = 0
        self._table_of_valid_tokens: list = []
        self._table_of_invalid_tokens: list = []
        
        self._read_character()

    def fill_table_of_tokens(self) -> None:
        while self._character != "":
            token = self.next_token()
            if token.is_valid:
                self._table_of_valid_tokens.append(token)
            else:
                self._table_of_invalid_tokens.append(token)

    def next_token(self) -> Token:
        self._skip_whitespace()

        if self._is_open_tag(self._character):
            literal: str = self._read_tag()

            if literal.count("/") > 1 or literal.count(">") > 1 or literal.count("<") > 1:
                return Token(TokenType.ILLEGAL, literal, self._position, self._row)

            if literal[1] == "/":
                return Token(TokenType.CLOSE_TAG, literal, self._position, self._row)

            if literal[-2] == "/":
                return Token(TokenType.AUTO_CLOSE_TAG, literal, self._position, self._row)

            return Token(TokenType.START_TAG, literal, self._position, self._row)

        elif self._is_letter(self._character):
            literal: str = self._read_letter()
            return Token(TokenType.TEXT, literal, self._position, self._row)

        elif self._is_number(self._character):
            literal: str = self._read_number()
            if literal.count(".") > 1:
                return Token(TokenType.ILLEGAL, literal, self._position, self._row)

            return Token(TokenType.NUMBER, literal, self._position, self._row)

        elif match(r'\n', self._character):
            self._row += 1
            self._read_character()
            return self.next_token()
        else:
            token = Token(TokenType.ILLEGAL,
                          self._character, self._position, self._row)

        self._read_character()
        return token

    def _is_letter(self, character: str) -> bool:
        return bool(match(r'^[a-záéíóúA-ZÁÉÍÓÚñÑ_]$', character))

    def _is_number(self, character: str) -> bool:
        return bool(match(r'^[0-9.]$', character))

    def _is_open_tag(self, character: str) -> bool:
        return bool(match(r'^<$', character))

    def _is_close_tag(self, character: str) -> bool:
        return bool(match(r'^>$', character))

    def _is_slash(self, character: str) -> bool:
        return bool(match(r'^/$', character))

    def _read_character(self) -> None:
        if self._read_position >= len(self._source):
            self._character = ""
        else:
            self._character = self._source[self._read_position]

        self._position = self._read_position
        self._read_position += 1

    def _read_letter(self) -> str:
        initial_position: int = self._position

        while self._is_letter(self._character):
            self._read_character()

        return self._source[initial_position:self._position]

    def _read_number(self) -> None:
        initial_position: int = self._position

        while self._is_number(self._character):
            self._read_character()

        return self._source[initial_position:self._position]

    def _read_tag(self) -> str:
        initial_position: int = self._position

        while not self._is_close_tag(self._character):
            self._read_character()

        self._read_character()
        return self._source[initial_position:self._position]

    def _skip_whitespace(self) -> None:
        while match(r'^\s$', self._character):
            self._read_character()

    def get_table_of_valid_tokens(self) -> list:
        return self._table_of_valid_tokens

    def get_table_of_invalid_tokens(self) -> list:
        return self._table_of_invalid_tokens
