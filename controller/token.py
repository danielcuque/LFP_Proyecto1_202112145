class Token():
    def __init__(self, row, column, lexeme):
        self.row = row
        self.column = column
        self.lexeme = lexeme

    def __str__(self):
        return f"({self.row}, {self.column}) {self.lexeme}"

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column

    def get_lexeme(self):
        return self.lexeme
