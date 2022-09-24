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
        self._column: int = 0
        self._table_of_valid_tokens: list = []
        self._table_of_invalid_tokens: list = []

        self._read_character()

    def fill_table_of_tokens(self) -> None:
        while self._character != "":
            token = self.next_token()
            if token.literal != "":
                if token.is_valid:
                    self._table_of_valid_tokens.append(token)
                else:
                    self._table_of_invalid_tokens.append(token)

    def next_token(self) -> Token:
        if self._is_open_tag(self._character):
            literal: str = self._read_tag()

            if literal.count("/") > 1 or literal.count(">") > 1 or literal.count(">") == 0 or literal.count("<") > 1 or literal.count("<") == 0:
                return Token(TokenType.ILLEGAL, literal, self._column, self._row, self._read_position)

            if literal[1] == "/":
                return Token(TokenType.CLOSE_TAG, literal, self._column, self._row, self._read_position)

            if literal[-2] == "/":
                return Token(TokenType.AUTO_CLOSE_TAG, literal, self._column, self._row, self._read_position)
            return Token(TokenType.START_TAG, literal, self._column, self._row, self._read_position)

        elif self._is_letter(self._character):
            literal: str = self._read_letter()
            return Token(TokenType.TEXT, literal, self._column, self._row, self._read_position)

        elif self._is_number(self._character):
            literal: str = self._read_number()
            if literal.count(".") > 1:
                return Token(TokenType.ILLEGAL, literal, self._column, self._row, self._read_position)

            return Token(TokenType.NUMBER, literal, self._column, self._row, self._read_position)

        elif match(r'\n', self._character):
            self._read_character()
            return self.next_token()

        elif match(r'\s', self._character):
            self._read_character()
            return self.next_token()
        else:
            token = Token(TokenType.ILLEGAL,
                          self._character, self._column, self._row, self._read_position)

        self._read_character()
        return token

    @staticmethod
    def _is_letter(character: str) -> bool:
        return bool(match(r'^[a-záéíóúA-ZÁÉÍÓÚñÑ_\[\]\(\)\*\+=\^√\/\-%:]$', character))

    @staticmethod
    def _is_number(character: str) -> bool:
        return bool(match(r'^[0-9.]$', character))

    @staticmethod
    def _is_open_tag(character: str) -> bool:
        return bool(match(r'^<$', character))

    @staticmethod
    def _is_close_tag(character: str) -> bool:
        return bool(match(r'^>$', character))

    @staticmethod
    def _is_slash(character: str) -> bool:
        return bool(match(r'^/$', character))

    def _read_character(self) -> None:
        if self._read_position >= len(self._source):
            self._character = ""
        else:
            self._character = self._source[self._read_position]

        if self._character == "\n":
            self._column = 0
            self._row += 1
        self._column += 1
        self._position = self._read_position
        self._read_position += 1

    def _read_letter(self) -> str:
        initial_position: int = self._position

        while self._is_letter(self._character):
            self._read_character()

        return self._source[initial_position:self._position]

    def _read_number(self) -> str:
        initial_position: int = self._position

        while self._is_number(self._character):
            self._read_character()

        return self._source[initial_position:self._position]

    def _read_tag(self) -> str:
        initial_position: int = self._position

        while not self._is_close_tag(self._character) and self._character != "\n":
            self._read_character()

        self._read_character()
        return self._source[initial_position:self._position]

    def get_table_of_valid_tokens(self) -> list:
        return self._table_of_valid_tokens

    def get_table_of_invalid_tokens(self) -> list:
        return self._table_of_invalid_tokens
