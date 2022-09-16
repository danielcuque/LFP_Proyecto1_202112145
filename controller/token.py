class Token():
    def __init__(self, row, column, lexeme, is_valid):
        self.row = row
        self.column = column
        self.lexeme = lexeme
        self.is_valid = is_valid

    def __str__(self):
        return f"({self.row}, {self.column}) {self.lexeme} {self.is_valid}"

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column

    def get_lexeme(self):
        return self.lexeme

    def get_type(self):
        return self.is_valid
