import re


class ValidCharacters:
    def __init__(self) -> None:
        self.letters = re.compile(r'[a-zA-Z\[\]]')
        self.numbers = re.compile(r'[0-9.]')
        self.brackets_open = re.compile(r'[<]')
        self.brackets_close = re.compile(r'[>]')
        self.slash = re.compile(r'[/]')
        self.equal = re.compile(r'[=]')

    def is_letter(self, character):
        return self.letters.match(character)

    def is_number(self, character):
        return self.numbers.match(character)

    def is_bracket_open(self, character):
        return self.brackets_open.match(character)

    def is_bracket_close(self, character):
        return self.brackets_close.match(character)

    def is_slash(self, character):
        return self.slash.match(character)

    def is_equal(self, character):
        return self.equal.match(character)
