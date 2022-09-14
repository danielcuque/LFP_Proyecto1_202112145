class Operation:
    def __init__(self, operation, *args):
        self.operation = operation
        self.args = args

    def __call__(self):
        return self.operation(*self.args)
