class Operation:
    def __init__(self, type_operation):
        self.type_operation = type_operation
        self.operands = []

    def operate(self):
        res = ""
        if self.type_operation.lower() == 'suma':
            for operando in self.operands:
                if type(operando) is not Operation:
                    res += operando + ' + '
                else:
                    res += "(" + operando.operate() + ") + "

        return res[0:-3]
