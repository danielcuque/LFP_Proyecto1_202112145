import re

class ValidCharacters:
    def __init__(self) -> None:
        self.letters = re.compile(r'[a-zA-Z]')
        self.numbers = re.compile(r'[0-9.]')
        self.brackets = re.compile(r'[<>/]')
    
    def is_letter(self, character):
        return self.letters.match(character)
    
    def is_number(self, character):
        return self.numbers.match(character)
    
    def is_bracket(self, character):
        return self.brackets.match(character)


